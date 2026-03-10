"use client";

import { motion } from "framer-motion";
import type { AgentInfo } from "./types";

const STATUS_COLORS: Record<AgentInfo["status"], string> = {
  active: "#10b981",
  idle: "#9ca3af",
  processing: "#f59e0b",
  error: "#ef4444",
};

type AgentsDashboardProps = {
  agents: AgentInfo[];
};

export default function AgentsDashboard({ agents }: AgentsDashboardProps) {
  const activeCount = agents.filter((a) => a.status === "active" || a.status === "processing").length;
  const avgTime = (() => {
    const withMetrics = agents.filter((a) => a.metrics?.avg_time_ms != null);
    if (withMetrics.length === 0) return null;
    const total = withMetrics.reduce((s, a) => s + (a.metrics!.avg_time_ms ?? 0), 0);
    return Math.round(total / withMetrics.length);
  })();

  return (
    <div className="big5loop-agents">
      {/* Overview */}
      <div className="big5loop-agents__overview">
        <div className="big5loop-agents__stat">
          <span className="big5loop-agents__stat-value">{agents.length}</span>
          <span className="big5loop-agents__stat-label">Total agents</span>
        </div>
        <div className="big5loop-agents__stat">
          <span className="big5loop-agents__stat-value">{activeCount}</span>
          <span className="big5loop-agents__stat-label">Active</span>
        </div>
        {avgTime != null && (
          <div className="big5loop-agents__stat">
            <span className="big5loop-agents__stat-value">{avgTime}ms</span>
            <span className="big5loop-agents__stat-label">Avg time</span>
          </div>
        )}
      </div>

      {/* Agent cards */}
      <div className="big5loop-agents__grid">
        {agents.map((agent, i) => (
          <motion.div
            key={agent.name}
            className="big5loop-agents__card"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06 }}
          >
            <div className="big5loop-agents__card-header">
              <span
                className="big5loop-agents__dot"
                style={{ background: STATUS_COLORS[agent.status] }}
              />
              <span className="big5loop-agents__name">{agent.name}</span>
              <span
                className={`big5loop-badge big5loop-badge--${agent.status === "active" ? "stable" : agent.status === "error" ? "error" : "learning"}`}
              >
                {agent.status}
              </span>
            </div>
            <p className="big5loop-agents__role">{agent.role}</p>
            {agent.metrics && (
              <div className="big5loop-agents__metrics">
                {agent.metrics.success_rate != null && (
                  <span>{Math.round(agent.metrics.success_rate * 100)}% success</span>
                )}
                {agent.metrics.avg_time_ms != null && (
                  <span>{agent.metrics.avg_time_ms}ms avg</span>
                )}
                {agent.metrics.processed != null && (
                  <span>{agent.metrics.processed} processed</span>
                )}
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
