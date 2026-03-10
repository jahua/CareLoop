#!/usr/bin/env python3
"""
Run BIG5-CHAT evaluation: send inputs to Big5Loop, collect detected OCEAN.
Output: processed/eval_results.jsonl for visualize_agreement.py.

Requires: Big5Loop app running (NEXT_PUBLIC_APP_URL or http://localhost:3000)

Modes:
  - Default: reads big5_eval_sessions.jsonl (needs create_eval_sessions.py + DB migration)
  - --api-only: reads big5_chat_eval.jsonl, generates session_ids on the fly (no DB needed)
"""
import argparse
import json
import os
import time
import uuid
from pathlib import Path
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request

EVAL_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = EVAL_DIR / "processed"

TRAIT_TO_OCEAN = {
    "openness": "O",
    "conscientiousness": "C",
    "extraversion": "E",
    "agreeableness": "A",
    "neuroticism": "N",
}


def run_eval(sessions_path, base_url="http://localhost:3000", limit=None, delay_sec=0.5, api_only=False):
    rows = []
    with open(sessions_path) as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            rows.append(json.loads(line))

    results = []
    for i, row in enumerate(rows):
        if api_only:
            session_id = str(uuid.uuid4())
            msg = row["input"]
            row = {"session_id": session_id, "input": row["input"], "expected_output": row["expected_output"],
                   "trait": row["trait"], "level": row["level"], "ground_truth": row["ground_truth"]}
        else:
            session_id = row["session_id"]
            msg = row["input"]
        url = f"{base_url.rstrip('/')}/api/chat"
        payload = {
            "session_id": session_id,
            "turn_index": 1,
            "message": msg,
            "context": {"language": "en", "canton": "ZH"},
        }

        try:
            if HAS_REQUESTS:
                resp = requests.post(url, json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
            else:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode())
        except Exception as e:
            results.append({
                **row,
                "detected_ocean": None,
                "response": None,
                "error": str(e),
            })
            continue

        ocean = None
        if data.get("personality_state", {}).get("ocean"):
            ocean = data["personality_state"]["ocean"]
        elif data.get("personality_state"):
            ocean = data["personality_state"].get("ocean")

        results.append({
            **row,
            "detected_ocean": ocean,
            "response": data.get("message", {}).get("content") if data.get("message") else None,
            "error": None,
        })

        if delay_sec > 0:
            time.sleep(delay_sec)

    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sessions", default=str(PROCESSED_DIR / "big5_eval_sessions.jsonl"))
    p.add_argument("--api-only", action="store_true",
                   help="Read from big5_chat_eval.jsonl, generate session_ids on the fly (no DB needed)")
    p.add_argument("--url", default=os.environ.get("NEXT_PUBLIC_APP_URL", "http://localhost:3000"))
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--delay", type=float, default=0.5)
    p.add_argument("-o", "--output", default=str(PROCESSED_DIR / "eval_results.jsonl"))
    args = p.parse_args()

    if args.api_only:
        sessions_path = PROCESSED_DIR / "big5_chat_eval.jsonl"
    else:
        sessions_path = Path(args.sessions)

    if not sessions_path.exists():
        if args.api_only:
            raise SystemExit(f"Missing: {sessions_path}. Run preprocess_big5_chat.py first.")
        raise SystemExit(f"Missing: {sessions_path}. Run create_eval_sessions.py first.")

    print("=== BIG5-CHAT Evaluation ===\n")
    if args.api_only:
        print("Mode: API-only (no DB migration required)\n")
    results = run_eval(
        sessions_path=sessions_path,
        base_url=args.url,
        limit=args.limit,
        delay_sec=args.delay,
        api_only=args.api_only,
    )

    out = Path(args.output)
    with open(out, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    ok = sum(1 for r in results if r.get("detected_ocean"))
    print(f"Completed: {ok}/{len(results)}")
    print(f"Output: {out}")
    print("\nNext: python scripts/visualize_agreement.py")


if __name__ == "__main__":
    main()
