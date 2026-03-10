#!/usr/bin/env python3
"""
Run PERSONAGE evaluation: send utterances to Big5Loop, collect detected OCEAN.
Compare with ground_truth_ocean (all 5 traits per sample).

PERSONAGE has full OCEAN ratings — best for evaluation.
Output: personage/processed/personage_eval_results.jsonl

Usage modes:
  # Via Next.js app (default, uses big5loop-turn workflow):
  python3 scripts/run_personage_eval.py --url http://localhost:3000

  # Directly to N8N PERSONAGE Benchmark workflow (recommended):
  python3 scripts/run_personage_eval.py \
    --n8n-webhook http://localhost:5678/webhook/big5loop-turn-personage-benchmark

  # Against production server via SSH tunnel:
  #   ssh -i ~/.ssh/boyig.pem -L 5678:127.0.0.1:5678 root@47.108.85.216
  python3 scripts/run_personage_eval.py \
    --n8n-webhook http://localhost:5678/webhook/big5loop-turn-personage-benchmark

Requires: Big5Loop N8N running (or use --n8n-webhook to call directly)
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
PERSONAGE_PROCESSED = EVAL_DIR / "personage" / "processed"


def run_eval(input_path, base_url="http://localhost:3000", n8n_webhook=None,
             limit=None, delay_sec=0.5, output_file=None):
    rows = []
    with open(input_path) as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            rows.append(json.loads(line))

    # Determine endpoint: direct N8N webhook or via Next.js /api/chat
    if n8n_webhook:
        endpoint = n8n_webhook.rstrip("/")
        mode_label = f"N8N direct → {endpoint}"
    else:
        endpoint = f"{base_url.rstrip('/')}/api/chat"
        mode_label = f"Next.js API → {endpoint}"
    print(f"  Endpoint: {mode_label}\n", flush=True)

    results = []
    total = len(rows)
    for idx, row in enumerate(rows):
        print(f"  [{idx + 1}/{total}] Sending...", flush=True)
        session_id = str(uuid.uuid4())
        msg = row["input"]
        url = endpoint
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
            r = {
                **row,
                "detected_ocean": None,
                "response": None,
                "error": str(e),
            }
            results.append(r)
            if output_file:
                output_file.write(json.dumps(r, ensure_ascii=False) + "\n")
                output_file.flush()
                os.fsync(output_file.fileno())
            print(f"  [{idx + 1}/{total}] Error: {e}", flush=True)
            continue

        ocean = None
        if data.get("personality_state", {}).get("ocean"):
            ocean = data["personality_state"]["ocean"]
        elif data.get("personality_state"):
            ocean = data["personality_state"].get("ocean")

        r = {
            **row,
            "detected_ocean": ocean,
            "response": data.get("message", {}).get("content") if data.get("message") else None,
            "error": None,
        }
        results.append(r)
        if output_file:
            output_file.write(json.dumps(r, ensure_ascii=False) + "\n")
            output_file.flush()
            os.fsync(output_file.fileno())
        print(f"  [{idx + 1}/{total}] OK", flush=True)

        if delay_sec > 0:
            time.sleep(delay_sec)

    return results


def main():
    p = argparse.ArgumentParser(
        description="PERSONAGE evaluation via Big5Loop (Next.js or N8N direct)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Via Next.js (default):
  python3 scripts/run_personage_eval.py

  # Direct to N8N PERSONAGE Benchmark workflow (local):
  python3 scripts/run_personage_eval.py \\
    --n8n-webhook http://localhost:5678/webhook/big5loop-turn-personage-benchmark

  # Production via SSH tunnel:
  #   ssh -i ~/.ssh/boyig.pem -L 5678:127.0.0.1:5678 root@47.108.85.216
  python3 scripts/run_personage_eval.py \\
    --n8n-webhook http://localhost:5678/webhook/big5loop-turn-personage-benchmark
""",
    )
    p.add_argument("--input", default=str(PERSONAGE_PROCESSED / "personage_eval.jsonl"))
    p.add_argument("--url", default=os.environ.get("NEXT_PUBLIC_APP_URL", "http://localhost:3000"),
                   help="Base URL of Next.js app (used when --n8n-webhook is not set)")
    p.add_argument("--n8n-webhook", default=None,
                   help="Call N8N webhook directly, bypassing Next.js. "
                        "E.g. http://localhost:5678/webhook/big5loop-turn-personage-benchmark")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--delay", type=float, default=0.5)
    p.add_argument("-o", "--output", default=str(PERSONAGE_PROCESSED / "personage_eval_results.jsonl"))
    args = p.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Missing: {input_path}. Run preprocess_personage.py first.")

    print("=== PERSONAGE Evaluation (full OCEAN) ===\n")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        results = run_eval(
            input_path=input_path,
            base_url=args.url,
            n8n_webhook=args.n8n_webhook,
            limit=args.limit,
            delay_sec=args.delay,
            output_file=f,
        )

    ok = sum(1 for r in results if r.get("detected_ocean"))
    print(f"Completed: {ok}/{len(results)}")
    print(f"Output: {out}")
    print("\nNext: python scripts/visualize_personage.py")


if __name__ == "__main__":
    main()
