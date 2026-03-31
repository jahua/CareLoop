#!/usr/bin/env python3
"""
Run PANDORA evaluation by sending processed test rows to Big5Loop /api/chat.

Input:  evaluation_data/pandora/processed/pandora_eval_test.jsonl
Output: evaluation_data/pandora/processed/pandora_eval_results_*.jsonl
"""

import argparse
import json
import time
import uuid
from pathlib import Path

import requests

EVAL_DIR = Path(__file__).resolve().parent.parent
IN_PATH = EVAL_DIR / "pandora" / "processed" / "pandora_eval_test.jsonl"
OUT_DIR = EVAL_DIR / "pandora" / "processed"


def run_eval(
    base_url: str,
    limit: int | None,
    delay: float,
    timeout: int,
    workflow: str | None,
    disable_env_proxy: bool,
):
    rows = []
    with open(IN_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            rows.append(json.loads(line))

    results = []
    session = requests.Session()
    if disable_env_proxy:
        # Avoid local proxy envs intercepting localhost calls during evaluation.
        session.trust_env = False
    for i, row in enumerate(rows, start=1):
        payload = {
            "session_id": str(uuid.uuid4()),
            "turn_index": 1,
            "message": row["input"],
            "evaluation_mode": True,
            "pandora_sample_id": row.get("sample_id"),
            "ground_truth_ocean": row.get("ground_truth_ocean"),
            "context": {"language": "en", "canton": "ZH"},
        }
        if workflow:
            payload["workflow"] = workflow

        url = f"{base_url.rstrip('/')}/api/chat"
        rec = {
            "sample_id": row.get("sample_id"),
            "input": row.get("input"),
            "ground_truth_ocean": row.get("ground_truth_ocean"),
            "detected_ocean": None,
            "coaching_mode": None,
            "detector_status": None,
            "detector_error": None,
            "stage_timings": None,
            "error": None,
            "status_code": None,
        }

        try:
            resp = session.post(url, json=payload, timeout=timeout)
            rec["status_code"] = resp.status_code
            data = resp.json()
            if resp.ok and isinstance(data, dict):
                rec["detected_ocean"] = (data.get("personality_state") or {}).get("ocean")
                rec["coaching_mode"] = data.get("coaching_mode")
                rec["detector_status"] = (data.get("pipeline_status") or {}).get("detector")
                rec["detector_error"] = (data.get("debug") or {}).get("detection_error")
                rec["stage_timings"] = data.get("stage_timings")
            else:
                rec["error"] = data.get("error", data) if isinstance(data, dict) else str(data)
        except Exception as e:
            rec["error"] = str(e)

        results.append(rec)
        if i % 25 == 0:
            ok = sum(1 for r in results if r.get("detected_ocean"))
            print(f"Progress {i}/{len(rows)} (ok={ok})")
        if delay > 0:
            time.sleep(delay)

    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://localhost:3000", help="Big5Loop base URL")
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--delay", type=float, default=0.1)
    p.add_argument("--timeout", type=int, default=90)
    p.add_argument("--workflow", default=None, help="Optional /api/chat workflow override")
    p.add_argument(
        "--use-env-proxy",
        action="store_true",
        help="Use HTTP(S)_PROXY from environment (default: disabled for localhost reliability)",
    )
    p.add_argument("--output", default=None)
    args = p.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.output:
        out_path = Path(args.output)
    else:
        suffix = f"sample{args.limit}" if args.limit else "full"
        out_path = OUT_DIR / f"pandora_eval_results_{suffix}.jsonl"

    results = run_eval(
        args.url,
        args.limit,
        args.delay,
        args.timeout,
        args.workflow,
        disable_env_proxy=not args.use_env_proxy,
    )

    with open(out_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    ok = sum(1 for r in results if r.get("detected_ocean"))
    print(f"Saved: {out_path}")
    print(f"Completed: {ok}/{len(results)} with detected_ocean")


if __name__ == "__main__":
    main()
