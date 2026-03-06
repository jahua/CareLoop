-- CareLoop Phase 3 monitoring query pack
-- Scope: audit_log + performance_metrics
-- Usage: run in PostgreSQL (psql, Grafana PostgreSQL datasource, or BI tool).

-- 1) End-to-end latency p50/p95/p99 (from audit_log.turn_latency_ms)
SELECT
  COUNT(*) AS samples,
  ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY turn_latency_ms)::numeric, 1) AS p50_ms,
  ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY turn_latency_ms)::numeric, 1) AS p95_ms,
  ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY turn_latency_ms)::numeric, 1) AS p99_ms
FROM audit_log
WHERE created_at >= NOW() - INTERVAL '1 hour'
  AND turn_latency_ms IS NOT NULL;

-- 2) Stage latency p95 by stage (from performance_metrics.duration_ms)
SELECT
  stage,
  COUNT(*) AS samples,
  ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_ms)::numeric, 1) AS p95_ms
FROM performance_metrics
WHERE created_at >= NOW() - INTERVAL '1 hour'
  AND duration_ms IS NOT NULL
GROUP BY stage
ORDER BY stage;

-- 3) Stage hard-failure rate by stage (exclude normal degraded paths)
-- Treat these statuses as non-failure for alerting:
--   ok, passed_with_warnings, skipped, fallback
-- Rationale: fallback is an intentional safe path in this stack.
SELECT
  stage,
  COUNT(*) AS samples,
  SUM(CASE WHEN status NOT IN ('ok', 'passed_with_warnings', 'skipped', 'fallback') THEN 1 ELSE 0 END) AS fail_count,
  ROUND(
    100.0 * SUM(CASE WHEN status NOT IN ('ok', 'passed_with_warnings', 'skipped', 'fallback') THEN 1 ELSE 0 END)
    / NULLIF(COUNT(*), 0),
    2
  ) AS fail_rate_pct
FROM performance_metrics
WHERE created_at >= NOW() - INTERVAL '1 hour'
GROUP BY stage
ORDER BY fail_rate_pct DESC, stage;

-- 3b) Fallback rate by stage (informational/degradation trend)
SELECT
  stage,
  COUNT(*) AS samples,
  SUM(CASE WHEN status = 'fallback' THEN 1 ELSE 0 END) AS fallback_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'fallback' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS fallback_rate_pct
FROM performance_metrics
WHERE created_at >= NOW() - INTERVAL '1 hour'
GROUP BY stage
ORDER BY fallback_rate_pct DESC, stage;

-- 4) Retrieval timeout breach count (> 2000ms target)
SELECT
  COUNT(*) AS retrieval_samples,
  SUM(CASE WHEN duration_ms > 2000 THEN 1 ELSE 0 END) AS breaches,
  ROUND(100.0 * SUM(CASE WHEN duration_ms > 2000 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS breach_rate_pct
FROM performance_metrics
WHERE stage = 'retrieval'
  AND created_at >= NOW() - INTERVAL '1 hour'
  AND duration_ms IS NOT NULL;

-- 5) Verification timeout breach count (> 1500ms target)
SELECT
  COUNT(*) AS verification_samples,
  SUM(CASE WHEN duration_ms > 1500 THEN 1 ELSE 0 END) AS breaches,
  ROUND(100.0 * SUM(CASE WHEN duration_ms > 1500 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS breach_rate_pct
FROM performance_metrics
WHERE stage = 'verification'
  AND created_at >= NOW() - INTERVAL '1 hour'
  AND duration_ms IS NOT NULL;

-- 6) Policy citation coverage (policy_navigation + mixed)
SELECT
  COUNT(*) FILTER (WHERE coaching_mode IN ('policy_navigation', 'mixed')) AS policy_turns,
  COUNT(*) FILTER (WHERE coaching_mode IN ('policy_navigation', 'mixed') AND COALESCE(citation_count, 0) > 0) AS policy_turns_with_citation,
  ROUND(
    100.0 * COUNT(*) FILTER (WHERE coaching_mode IN ('policy_navigation', 'mixed') AND COALESCE(citation_count, 0) > 0)
    / NULLIF(COUNT(*) FILTER (WHERE coaching_mode IN ('policy_navigation', 'mixed')), 0),
    2
  ) AS citation_coverage_pct
FROM audit_log
WHERE created_at >= NOW() - INTERVAL '1 hour';

-- 7) Top stage errors (last 1h)
SELECT
  stage,
  COALESCE(error_code, 'none') AS error_code,
  COUNT(*) AS hits
FROM performance_metrics
WHERE created_at >= NOW() - INTERVAL '1 hour'
  AND (error_code IS NOT NULL OR status NOT IN ('ok', 'passed_with_warnings', 'skipped'))
GROUP BY stage, COALESCE(error_code, 'none')
ORDER BY hits DESC, stage, error_code;
