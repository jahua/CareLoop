#!/usr/bin/env python3
"""
Direct PERSONAGE evaluation: call NVIDIA API directly (no Big5Loop/N8N needed).
Allows fast iteration on model, temperature, and prompt for OCEAN personality detection.

Usage:
  # Default: llama-3.3-70b, temp=0.1, few-shot PERSONAGE-calibrated prompt
  python3 scripts/run_personage_eval_direct.py --limit 30

  # Compare prompts (few-shot vs zero-shot vs generic)
  python3 scripts/run_personage_eval_direct.py --prompt personage_fewshot --limit 30
  python3 scripts/run_personage_eval_direct.py --prompt personage --limit 30
  python3 scripts/run_personage_eval_direct.py --prompt generic --limit 30

  # Full run (all 320 samples)
  python3 scripts/run_personage_eval_direct.py

Requires: NVIDIA_API_KEY env var (get from build.nvidia.com)
"""
import argparse
import json
import os
import re
import time
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request

EVAL_DIR = Path(__file__).resolve().parent.parent
PERSONAGE_PROCESSED = EVAL_DIR / "personage" / "processed"

MODELS = {
    "llama70b": "meta/llama-3.3-70b-instruct",
    "llama8b": "meta/llama-3.1-8b-instruct",
    "gemma": "google/gemma-3n-e4b-it",
    "mistral": "mistralai/mistral-7b-instruct-v0.3",
}

FEWSHOT_SYSTEM = (
    "You are a personality psychologist rating Big Five (OCEAN) traits from restaurant recommendation utterances.\n\n"
    "CRITICAL calibration rules:\n"
    "- Rate the SPEAKER's personality from their STYLE. Not the restaurant quality.\n"
    "- Each trait is INDEPENDENT. A friendly speaker (high A) can have any N, C, E, or O value.\n\n"
    "TRAIT GUIDE:\n"
    "O (Openness): HIGH = varied vocabulary ('satisfying', 'dainty', 'phenomenal', 'unspeakable'), creative phrasing. "
    "LOW = repetitive, simple words ('like', 'basically', 'actually'), filler-heavy.\n\n"
    "C (Conscientiousness): HIGH = formal register ('eating house', 'eating place', 'I see, well', 'I suppose', 'It seems to me'), "
    "structured comparison with clear details. "
    "LOW = disorganized ('Err...', 'Mmhm...'), repetition ('it's a cafe place, it's a cafe place'), "
    "'I might be wrong', scattered information, informal register.\n\n"
    "E (Extraversion): HIGH = warm, enthusiastic ('outstanding!', 'phenomenal!', 'love it', 'favourite'), "
    "exclamatory, engaging the listener. "
    "LOW = flat, withdrawn ('I don't know', 'there could be worse'), monotone factual delivery.\n\n"
    "A (Agreeableness): HIGH = polite, collaborative ('would suggest', 'would appreciate', 'you would like', 'buddy', 'pal'). "
    "LOW = profane ('bloody', 'damn'), blunt ('rude', 'nasty', 'isn't as bad', 'the only place that is any good').\n\n"
    "N (Neuroticism): HIGH = stuttering ('re-re-recommend', 'it-it-italian'), genuine anxiety "
    "('I don't know!', 'I am not sure!', 'I might be wrong!' with exclamation), "
    "repetitive corrections, emotional volatility. "
    "LOW = calm, assured ('I imagine', 'I believe', 'I think that', 'It seems to me'), "
    "measured delivery. MODERATE = 'you know', 'okay?', 'alright?' are NEUTRAL filler, not neurotic.\n\n"
    "Return ONLY valid JSON: {\"O\":float,\"C\":float,\"E\":float,\"A\":float,\"N\":float}\n"
    "Each value in [-1.0, 1.0]. No explanation."
)

FEWSHOT_EXAMPLES = [
    {
        "input": "Did you say Kin Khao and Tossed? Oh yeah, I would suggest them, wouldn't you? Kin Khao offers quite satisfactory food. I guess Tossed, however, has sort of acceptable food.",
        "output": '{"O":-0.2,"C":0.4,"E":0.0,"A":0.6,"N":-0.3}'
    },
    {
        "input": "Even if Tossed doesn't have nasty food, actually, the service is damn unmannered. I mean, basically, Kin Khao offers like, rude staff.",
        "output": '{"O":-0.3,"C":0.1,"E":0.2,"A":-0.4,"N":-0.2}'
    },
    {
        "input": "You want to know more about Scopa and Shabu-Tatsu? I see, well, they're quite outstanding eating places. I suppose Scopa is an italian and new american eating house with satisfying service. Shabu-Tatsu, which provides sort of satisfactory service, however, is a japanese restaurant.",
        "output": '{"O":0.7,"C":0.7,"E":0.3,"A":0.5,"N":-0.7}'
    },
    {
        "input": "I might be darn wrong. Scopa provides kind of bad ambiance! Err... even if Shabu-Tatsu doesn't have unfriendly waiters, it offers like, poor ambience, bad atmosphere.",
        "output": '{"O":-0.7,"C":-0.4,"E":0.2,"A":-0.6,"N":0.5}'
    },
    {
        "input": "I don't know. I might re-re-recommend Sc-Sc-Scopa and Shabu-Tatsu! Scopa has... it provides bad atmosphere, but it features like, nice service, though. It's an it-it-italian and new american place. I mean, Shabu-Tatsu is a japanese place. Even if the service is damn nice, it offers re-re-really bad atmosphere.",
        "output": '{"O":-0.2,"C":-0.3,"E":-0.3,"A":0.4,"N":0.4}'
    },
    {
        "input": "Let's see, Le Rivage and Pintaile's Pizza... I see, well, they're rather outstanding eating houses. Even if Pintaile's Pizza provides quite unspeakable atmosphere, it's sort of inexpensive. On the other hand, Le Rivage is in Manhattan, also its price is 40 dollars.",
        "output": '{"O":0.3,"C":0.3,"E":0.4,"A":0.4,"N":-0.6}'
    },
    {
        "input": "I thought everybody knew that Pepolino is the only place that is any good. Actually, this restaurant is in TriBeCa/SoHo. Basically, this restaurant, which doesn't provide good ambiance, is damn pricy.",
        "output": '{"O":-0.6,"C":0.1,"E":0.1,"A":-0.8,"N":0.7}'
    },
    {
        "input": "You want to know more about Chimichurri Grill? I guess you would like it buddy because this restaurant, which is in Midtown West, is a latin american place with rather nice food and quite nice waiters, you know, okay?",
        "output": '{"O":0.4,"C":0.8,"E":0.8,"A":0.6,"N":-0.7}'
    },
    {
        "input": "Basically, Flor De Mayo isn't as bad as the others. Obviously, it isn't expensive. I mean, actually, its price is 18 dollars.",
        "output": '{"O":-0.3,"C":0.3,"E":0.0,"A":-0.1,"N":-0.7}'
    },
    {
        "input": "I don't know. I might ap-ap-approve Le Rivage and Pintaile's Pizza. Even if Pintaile's Pizza is cheap, it features like, bad atmosphere. Le Rivage is in Manhattan! Err... actually, it provides really bad atmosphere. Its price is 40 do-do-dollars.",
        "output": '{"O":-0.5,"C":-0.3,"E":0.0,"A":-0.1,"N":0.6}'
    },
]

PROMPTS = {
    "personage_fewshot": None,
    "personage": (
        "You are a personality psychologist analyzing a speaker's Big Five (OCEAN) traits "
        "from a single written utterance about restaurants.\n\n"
        "Focus on LINGUISTIC STYLE, not topic:\n"
        "- Openness (O): Varied/rich vocabulary vs simple/repetitive wording\n"
        "- Conscientiousness (C): Structured, detailed, precise vs vague, disorganized, hedging\n"
        "- Extraversion (E): Warm, enthusiastic, assertive vs hesitant, flat, withdrawn "
        '("err", "I might be wrong", "I don\'t know")\n'
        "- Agreeableness (A): Polite, accommodating, collaborative "
        '("would suggest", "you would like") vs blunt, profane ("bloody", "damn", "rude")\n'
        "- Neuroticism (N): Anxious, hedging, uncertain "
        '("I am not sure", "I might be wrong", filler words) vs calm, assured\n\n'
        "Return ONLY valid JSON: "
        '{"O":float,"C":float,"E":float,"A":float,"N":float}\n'
        "Each value in [-1.0, 1.0]. No explanation.\n\n"
        'Utterance: "{text}"'
    ),
    "generic": (
        "Analyze this text for Big Five (OCEAN) personality traits. "
        "Return ONLY JSON: "
        '{"O":float,"C":float,"E":float,"A":float,"N":float} '
        "(each -1.0 to 1.0).\n"
        'Text: "{text}"'
    ),
    "personage_cot": (
        "You are a personality psychologist. Analyze the speaker's Big Five personality "
        "from this restaurant recommendation utterance.\n\n"
        "Step 1: Note stylistic cues:\n"
        "- Hedging/uncertainty markers (\"err\", \"I mean\", \"basically\", \"I might be wrong\")\n"
        "- Politeness markers (\"would suggest\", \"would appreciate\", \"you would like\")\n"
        "- Profanity/bluntness (\"bloody\", \"damn\", \"rude\", \"nasty\")\n"
        "- Enthusiasm/energy (\"outstanding\", \"phenomenal\", \"favourite\")\n"
        "- Vocabulary richness and sentence structure\n\n"
        "Step 2: Rate each trait in [-1.0, 1.0]:\n"
        "O=Openness, C=Conscientiousness, E=Extraversion, A=Agreeableness, N=Neuroticism\n\n"
        "Return ONLY the final JSON on the last line: "
        '{"O":float,"C":float,"E":float,"A":float,"N":float}\n\n'
        'Utterance: "{text}"'
    ),
}


def build_fewshot_messages(text):
    messages = [{"role": "system", "content": FEWSHOT_SYSTEM}]
    for ex in FEWSHOT_EXAMPLES:
        messages.append({"role": "user", "content": f'Utterance: "{ex["input"]}"'})
        messages.append({"role": "assistant", "content": ex["output"]})
    messages.append({"role": "user", "content": f'Utterance: "{text[:600]}"'})
    return messages


def call_nvidia_api(text, api_key, api_url, model, temperature, prompt_template, max_tokens=150, timeout=60):
    if prompt_template is None:
        messages = build_fewshot_messages(text)
    else:
        prompt = prompt_template.replace("{text}", text[:600])
        messages = [{"role": "user", "content": prompt}]
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    if HAS_REQUESTS:
        resp = requests.post(api_url, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        body = resp.json()
    else:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode())

    raw_content = body.get("choices", [{}])[0].get("message", {}).get("content", "")
    match = re.search(r"\{[^}]+\}", raw_content)
    if not match:
        return None, raw_content

    parsed = json.loads(match.group())
    if not isinstance(parsed.get("O"), (int, float)):
        return None, raw_content

    def clamp(v):
        return max(-1.0, min(1.0, float(v)))

    ocean = {
        "O": clamp(parsed.get("O", 0)),
        "C": clamp(parsed.get("C", 0)),
        "E": clamp(parsed.get("E", 0)),
        "A": clamp(parsed.get("A", 0)),
        "N": clamp(parsed.get("N", 0)),
    }
    return ocean, raw_content


def run_eval(input_path, api_key, api_url, model, temperature, prompt_template,
             limit=None, delay_sec=0.3, output_file=None, timeout=30):
    rows = []
    with open(input_path) as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            rows.append(json.loads(line))

    results = []
    total = len(rows)
    ok_count = 0
    err_count = 0

    for idx, row in enumerate(rows):
        print(f"  [{idx + 1}/{total}] {row.get('id', '?')[:50]}...", end=" ", flush=True)
        text = row["input"]

        try:
            ocean, raw = call_nvidia_api(
                text, api_key, api_url, model, temperature, prompt_template, timeout=timeout,
            )
        except Exception as e:
            r = {**row, "detected_ocean": None, "raw_api": None, "error": str(e)}
            results.append(r)
            err_count += 1
            if output_file:
                output_file.write(json.dumps(r, ensure_ascii=False) + "\n")
                output_file.flush()
            print(f"ERR: {e}", flush=True)
            if delay_sec > 0:
                time.sleep(delay_sec)
            continue

        r = {**row, "detected_ocean": ocean, "raw_api": raw, "error": None}
        results.append(r)
        if ocean:
            ok_count += 1
            vals = " ".join(f"{k}={ocean[k]:+.2f}" for k in "OCEAN")
            print(f"OK  {vals}", flush=True)
        else:
            err_count += 1
            print(f"PARSE_FAIL: {raw[:80]}", flush=True)

        if output_file:
            output_file.write(json.dumps(r, ensure_ascii=False) + "\n")
            output_file.flush()

        if delay_sec > 0:
            time.sleep(delay_sec)

    return results, ok_count, err_count


def main():
    p = argparse.ArgumentParser(
        description="Direct NVIDIA API PERSONAGE eval (no Big5Loop needed)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Models shortcuts: " + ", ".join(f"{k}={v}" for k, v in MODELS.items()),
    )
    p.add_argument("--input", default=str(PERSONAGE_PROCESSED / "personage_eval.jsonl"))
    p.add_argument("--model", default="meta/llama-3.3-70b-instruct",
                    help="NVIDIA model name or shortcut (llama70b, gemma, etc)")
    p.add_argument("--temperature", type=float, default=0.1,
                    help="Sampling temperature (default: 0.1 for deterministic scoring)")
    p.add_argument("--prompt", choices=list(PROMPTS.keys()), default="personage_fewshot",
                    help="Prompt template (default: personage_fewshot)")
    p.add_argument("--api-url", default="https://integrate.api.nvidia.com/v1/chat/completions")
    p.add_argument("--limit", type=int, default=None, help="Max samples to eval")
    p.add_argument("--delay", type=float, default=0.3, help="Delay between API calls (seconds)")
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("-o", "--output", default=None, help="Output JSONL path (auto-generated if not set)")
    args = p.parse_args()

    api_key = os.environ.get("NVIDIA_API_KEY", "")
    if not api_key or len(api_key) < 10:
        raise SystemExit(
            "NVIDIA_API_KEY not set. Get one from https://build.nvidia.com\n"
            "  export NVIDIA_API_KEY=nvapi-..."
        )

    model = MODELS.get(args.model, args.model)
    prompt_template = PROMPTS[args.prompt]

    if args.output:
        out_path = Path(args.output)
    else:
        model_short = model.split("/")[-1].replace("-", "_")[:30]
        temp_str = f"t{args.temperature:.1f}".replace(".", "")
        out_path = PERSONAGE_PROCESSED / f"personage_results_{model_short}_{args.prompt}_{temp_str}.jsonl"

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Missing: {input_path}. Run preprocess_personage.py first.")

    print("=" * 60)
    print("  PERSONAGE Direct API Evaluation")
    print("=" * 60)
    print(f"  Model:       {model}")
    print(f"  Temperature: {args.temperature}")
    print(f"  Prompt:      {args.prompt}")
    print(f"  Input:       {input_path}")
    print(f"  Output:      {out_path}")
    print(f"  Limit:       {args.limit or 'all'}")
    print("=" * 60 + "\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        results, ok, err = run_eval(
            input_path=input_path,
            api_key=api_key,
            api_url=args.api_url,
            model=model,
            temperature=args.temperature,
            prompt_template=prompt_template,
            limit=args.limit,
            delay_sec=args.delay,
            output_file=f,
            timeout=args.timeout,
        )

    print(f"\n{'=' * 60}")
    print(f"  Done: {ok} OK, {err} errors, {len(results)} total")
    print(f"  Output: {out_path}")
    print(f"\n  Visualize:")
    print(f"    python scripts/visualize_personage.py --input {out_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
