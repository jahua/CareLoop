#!/usr/bin/env python3
"""
Create User and Sessions for BIG5-CHAT simulation evaluation.

When run, creates:
- Eval user (big5_eval@big5loop.ch) if missing — marks simulation, not real person
- Sessions linked to that user — all saved in DB for review
- Output: jsonl or csv of session_id + input + ground_truth

Classification: Sessions with user_id = eval user are simulation evaluations.
Exclude from real-user analytics; use for evaluation review only.

Requires: DATABASE_URL or AUDIT_DATABASE_URL, psycopg2-binary
"""
import argparse
import csv
import json
import os
import uuid
from pathlib import Path
from typing import List, Optional, Tuple

EVAL_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = EVAL_DIR / "processed"
EVAL_USER_EMAIL = "big5_eval@big5loop.ch"
EVAL_USER_DISPLAY = "BIG5-CHAT Simulation (not real person)"


def get_db_url() -> str:
    url = os.environ.get("DATABASE_URL") or os.environ.get("AUDIT_DATABASE_URL") or ""
    return url.strip()


def ensure_eval_table(cur) -> None:
    """Create eval_session_metadata table if not exists."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eval_session_metadata (
          session_id   UUID PRIMARY KEY REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
          eval_run_id  TEXT NOT NULL,
          ground_truth JSONB NOT NULL,
          created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_eval_metadata_run ON eval_session_metadata(eval_run_id)"
    )


def ensure_eval_user(cur) -> str:
    """Ensure eval user exists; return user_id."""
    cur.execute("SELECT id FROM users WHERE email = %s", (EVAL_USER_EMAIL,))
    row = cur.fetchone()
    if row:
        return str(row[0])
    # Create user (same hash as migration: big5loop123)
    user_id = str(uuid.uuid4())
    cur.execute(
        """
        INSERT INTO users (id, email, password_hash, display_name, locale, canton)
        VALUES (%s::uuid, %s, %s, %s, 'en', 'ZH')
        """,
        (
            user_id,
            EVAL_USER_EMAIL,
            "$2a$10$BrS0H/n/.MEfEIUfQS7.0u33SSK2Ja197qOrKg9Kng5r77qPk3zdu",
            EVAL_USER_DISPLAY,
        ),
    )
    return user_id


def create_eval_sessions(
    input_path: Path,
    run_id: Optional[str] = None,
    limit: Optional[int] = None,
    output_format: str = "jsonl",
    output_path: Optional[Path] = None,
) -> Tuple[List[dict], Path]:
    try:
        import psycopg2
    except ImportError:
        raise SystemExit("Install: pip install psycopg2-binary")

    db_url = get_db_url()
    if not db_url:
        raise SystemExit("Set DATABASE_URL or AUDIT_DATABASE_URL")

    run_id = run_id or f"big5_{uuid.uuid4().hex[:8]}"
    rows = []
    with open(input_path) as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            rows.append(json.loads(line))

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    ensure_eval_table(cur)
    user_id = ensure_eval_user(cur)

    created = []
    for row in rows:
        session_id = str(uuid.uuid4())
        ground_truth = {
            "trait": row["trait"],
            "level": row["level"],
            "ground_truth": row["ground_truth"],
            "expected_output": row["expected_output"],
        }

        cur.execute(
            """
            INSERT INTO chat_sessions (session_id, user_id, status, locale, canton)
            VALUES (%s::uuid, %s::uuid, 'active', 'en', 'ZH')
            ON CONFLICT (session_id) DO UPDATE SET user_id = EXCLUDED.user_id
            """,
            (session_id, user_id),
        )

        cur.execute(
            """
            INSERT INTO eval_session_metadata (session_id, eval_run_id, ground_truth)
            VALUES (%s::uuid, %s, %s::jsonb)
            ON CONFLICT (session_id) DO UPDATE SET eval_run_id = EXCLUDED.eval_run_id, ground_truth = EXCLUDED.ground_truth
            """,
            (session_id, run_id, json.dumps(ground_truth)),
        )

        created.append({
            "session_id": session_id,
            "input": row["input"],
            "expected_output": row["expected_output"],
            "trait": row["trait"],
            "level": row["level"],
            "ground_truth": row["ground_truth"],
        })

    conn.commit()

    # Write output (jsonl or csv)
    out_path = output_path or (PROCESSED_DIR / f"big5_eval_sessions.{output_format}")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "csv":
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=created[0].keys())
            w.writeheader()
            w.writerows(created)
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            for c in created:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

    cur.close()
    conn.close()

    return created, out_path


def main():
    p = argparse.ArgumentParser(
        description="Create eval user + sessions for BIG5-CHAT simulation (saved in DB)"
    )
    p.add_argument("--limit", type=int, default=None, help="Limit sessions")
    p.add_argument("--run-id", type=str, default=None, help="Run ID")
    p.add_argument("-f", "--format", choices=["jsonl", "csv"], default="jsonl")
    p.add_argument("-o", "--output", type=str, default=None)
    args = p.parse_args()

    input_path = PROCESSED_DIR / "big5_chat_eval.jsonl"
    if not input_path.exists():
        raise SystemExit(f"Run preprocess first: python scripts/preprocess_big5_chat.py --sample 100")

    print("=== BIG5-CHAT Simulation Evaluation Setup ===\n")
    created, out_path = create_eval_sessions(
        input_path=input_path,
        run_id=args.run_id,
        limit=args.limit,
        output_format=args.format,
        output_path=Path(args.output) if args.output else None,
    )

    print(f"Saved to DB: {len(created)} sessions")
    print(f"User: {EVAL_USER_EMAIL} (simulation, not real person)")
    print(f"Login: big5_eval@big5loop.ch / big5loop123")
    print(f"Output: {out_path}")
    print("\nClassification: user_id = eval user → simulation evaluation")


if __name__ == "__main__":
    main()
