#!/usr/bin/env python3
"""
Multi-Agent OCEAN Detector - 5 Specialized Trait Agents

Creates 5 specialized agents (O, C, E, A, N), each focused on detecting
one Big Five trait with its own optimized prompt and few-shot examples.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import sys
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from quick_llama31_5shot_eval import (
    clamp, parse_ocean, build_messages, call_nvidia,
    load_workflow_prompts_and_fewshot, select_balanced_fewshots,
    TRAITS, resolve_api_key
)

# Define what we need locally
TRAIT_LABELS = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism"
}
DEFAULT_MODEL = "meta/llama-3.1-70b-instruct"

class TraitAgent:
    """Specialized agent for detecting one Big Five trait."""

    def __init__(self, trait: str, system_prompt: str):
        self.trait = trait
        self.system_prompt = system_prompt
        self.name = f"{trait}-Agent"

    def get_system_prompt(self) -> str:
        """Return the specialized system prompt for this trait."""
        return self.system_prompt


def create_trait_specialized_prompts() -> Dict[str, str]:
    """Create 5 specialized system prompts, one for each trait."""
    prompts = {}

    prompts["O"] = """You are an Openness detection specialist. Analyze the linguistic style of this Reddit-style message for Openness ONLY.

Focus on: abstract thinking, novelty-seeking, intellectual curiosity, unconventional framing, exploration of ideas vs concrete, literal, repetitive, or rigid thinking patterns.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly abstract, philosophical, curious, novel thinking
- +0.3 to +0.7 = moderately open, some intellectual curiosity
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = highly concrete, literal, repetitive, rigid thinking

Output ONLY a JSON with key "O" containing a float from -1.0 to 1.0.
Be decisive. Look for strong linguistic evidence of cognitive style."""

    prompts["C"] = """You are a Conscientiousness detection specialist. Analyze the linguistic style of this Reddit-style message for Conscientiousness ONLY.

Focus on: structured, planful, disciplined, organized language vs impulsive, disorganized, inconsistent, or scattered expression.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly structured, planful, disciplined, organized communication
- +0.3 to +0.7 = moderately conscientious, some self-regulation
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = highly impulsive, disorganized, inconsistent, scattered

Output ONLY a JSON with key "C" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic evidence of self-regulation and structure."""

    prompts["E"] = """You are an Extraversion detection specialist. Analyze the linguistic style of this Reddit-style message for Extraversion ONLY.

Focus on: energetic, assertive, socially engaging, outgoing style vs restrained, withdrawn, low-energy, or avoidant communication.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly energetic, assertive, socially engaging, outgoing style
- +0.3 to +0.7 = moderately extraverted, some social energy
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = restrained, withdrawn, low-energy, avoidant communication

Output ONLY a JSON with key "E" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic markers of social activation and energy."""

    prompts["A"] = """You are an Agreeableness detection specialist. Analyze the linguistic style of this Reddit-style message for Agreeableness ONLY.

Focus on: empathetic, cooperative, warm, tactful stance vs hostile, contemptuous, combative, or self-centered tone.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly empathetic, cooperative, warm, tactful communication
- +0.3 to +0.7 = moderately agreeable, some warmth
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = hostile, contemptuous, combative, self-centered tone

Output ONLY a JSON with key "A" containing a float from -1.0 to 1.0.
Be decisive. Focus on interpersonal stance and emotional tone."""

    prompts["N"] = """You are a Neuroticism detection specialist. Analyze the linguistic style of this Reddit-style message for Neuroticism ONLY.

Focus on: anxious, reactive, ruminative, emotionally volatile language vs calm, regulated, steady, emotionally stable expression.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = high emotional volatility, rumination, anxiety markers
- +0.3 to +0.7 = moderately emotionally reactive
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = calm, regulated, steady, emotionally stable communication

Output ONLY a JSON with key "N" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic markers of emotional regulation."""

    return prompts


def _extract_single_trait_score(raw: str, trait: str) -> float | None:
    """Extract a single trait score from API response like '{"O": -0.5}'."""
    if not raw:
        return None
    s = raw.strip()
    m = re.search(rf'"{trait}"\s*:\s*(-?[0-9]+\.?[0-9]*)', s)
    if m:
        return float(m.group(1))
    try:
        brace_start = s.find("{")
        brace_end = s.rfind("}")
        if brace_start >= 0 and brace_end > brace_start:
            obj = json.loads(s[brace_start:brace_end + 1])
            v = obj.get(trait) or obj.get(trait.lower())
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return float(v)
    except (json.JSONDecodeError, ValueError):
        pass
    return None


class MultiAgentOceanDetector:
    """5 specialized agents working together to detect OCEAN traits."""

    def __init__(self, model: str = DEFAULT_MODEL, api_url: str = None):
        self.model = model
        self.api_url = api_url or os.environ.get(
            "NVIDIA_API_URL",
            "https://integrate.api.nvidia.com/v1/chat/completions"
        )
        self.agents = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Create the 5 specialized trait agents."""
        prompts = create_trait_specialized_prompts()
        for trait in TRAITS:
            self.agents[trait] = TraitAgent(trait, prompts[trait])

    def _detect_single_trait(self, trait: str, text: str, few_shots: List[Tuple[str, str]],
                             n_shots: int, temperature: float, max_tokens: int,
                             timeout: int, api_key: str) -> Dict[str, Any]:
        """Call the NVIDIA API for a single trait (thread-safe)."""
        agent = self.agents[trait]
        trait_fewshots = few_shots[:n_shots]

        messages = [{"role": "system", "content": agent.get_system_prompt()}]
        for user_text, assistant_response in trait_fewshots:
            messages.append({"role": "user", "content": f'Utterance: "{user_text}"'})
            messages.append({"role": "assistant", "content": assistant_response})
        messages.append({"role": "user", "content": f'Utterance: "{text[:500]}"'})

        session = requests.Session()
        try:
            raw, err = call_nvidia(
                session, self.api_url, api_key, self.model,
                messages, timeout, 3, 2.0, 30.0
            )
            score = _extract_single_trait_score(raw, trait) if raw else None
            if score is not None:
                return {"trait": trait, "score": clamp(score), "raw": raw[:200] if raw else None,
                        "error": None, "success": True}
            else:
                return {"trait": trait, "score": 0.0, "raw": raw[:200] if raw else None,
                        "error": err or "no_score_returned", "success": False}
        except Exception as e:
            return {"trait": trait, "score": 0.0, "raw": None,
                    "error": str(e), "success": False}

    def detect(self, text: str, few_shots: List[Tuple[str, str]], n_shots: int = 5,
               temperature: float = 0.3, max_tokens: int = 120, timeout: int = 45,
               api_key: str = None) -> Dict[str, Any]:
        """
        Use 5 specialized agents to detect OCEAN traits concurrently.

        All 5 trait API calls run in parallel via ThreadPoolExecutor.
        """
        if not api_key:
            api_key, _ = resolve_api_key(Path(__file__).resolve().parent.parent)

        results = {
            "predicted_ocean": {},
            "agent_details": {},
            "model": self.model,
            "n_shots": n_shots,
            "temperature": temperature,
            "success": True,
            "method": "multi_agent",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {
                pool.submit(self._detect_single_trait, trait, text, few_shots,
                            n_shots, temperature, max_tokens, timeout, api_key): trait
                for trait in TRAITS
            }
            for future in as_completed(futures):
                r = future.result()
                trait = r["trait"]
                results["predicted_ocean"][trait] = r["score"]
                results["agent_details"][trait] = {
                    "score": r["score"],
                    "raw": r.get("raw"),
                    "error": r["error"],
                    "success": r["success"]
                }
                if not r["success"]:
                    results["success"] = False

        return results


def main() -> None:
    """Command line interface for multi-agent OCEAN detection."""
    root = Path(__file__).resolve().parent  # multi_agent/
    offline_dir = root.parent               # offline_nv_detection/
    eval_data = offline_dir.parent.parent   # evaluation_data/
    big5loop = eval_data.parent             # big5loop/

    ap = argparse.ArgumentParser(
        description="Multi-Agent OCEAN Detector with 5 specialized trait agents"
    )
    ap.add_argument("--workflow", default=str(big5loop / "workflows" / "n8n" / "big5loop-pandora-eval-v4.json"))
    ap.add_argument("--input", default=str(eval_data / "pandora" / "processed" / "pandora_eval_results_v4_20260327.jsonl"))
    ap.add_argument("--limit", type=int, default=20, help="Number of samples to evaluate")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--n-shots", type=int, default=5, help="Few-shot count per agent")
    ap.add_argument("--temperature", type=float, default=0.3, help="Temperature for each agent")
    ap.add_argument("--timeout", type=int, default=45, help="API timeout in seconds")
    ap.add_argument("--output", default=None, help="JSONL output path")
    ap.add_argument("--api-key", default=None, help="NVIDIA API key override")

    args = ap.parse_args()

    print(f"Multi-Agent OCEAN Detector")
    print(f"   {args.limit} samples, {args.n_shots} few-shots per agent")
    print("="*70)

    wf_path = Path(args.workflow)
    if not wf_path.exists():
        print(f"Workflow file not found: {wf_path}")
        return

    variants, few_all = load_workflow_prompts_and_fewshot(wf_path)
    print(f"Loaded {len(few_all)} few-shot examples and {len(variants)} prompt variants")

    samples: list[dict[str, Any]] = []
    try:
        with open(args.input, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= args.limit:
                    break
                samples.append(json.loads(line))
        print(f"Loaded {len(samples)} samples for evaluation")
    except Exception as e:
        print(f"Failed to load input: {e}")
        return

    detector = MultiAgentOceanDetector(model=args.model)
    print("Initialized 5 specialized trait agents:")
    for trait in TRAITS:
        print(f"   {trait}-Agent: {TRAIT_LABELS[trait]} specialist")

    api_key, key_src = resolve_api_key(root, cli_key=args.api_key)
    if not api_key or len(api_key) < 10:
        print("NVIDIA_API_KEY missing. Set NVIDIA_API_KEY environment variable or use --api-key.")
        return

    print(f"API key loaded from: {key_src}")
    print(f"Running multi-agent detection with {args.n_shots} shots per agent...")

    results = []
    for i, sample in enumerate(samples):
        text = str(sample.get("input") or sample.get("text") or "")
        gt = sample.get("ground_truth_ocean") or {}

        result = detector.detect(
            text=text,
            few_shots=few_all,
            n_shots=args.n_shots,
            temperature=args.temperature,
            api_key=api_key
        )

        result["sample_id"] = sample.get("sample_id")
        result["ground_truth_ocean"] = gt
        results.append(result)

        status = "ok" if result["success"] else "FAIL"
        if not result["success"]:
            errs = [f"{t}:{d.get('error','?')}" for t,d in result.get("agent_details",{}).items() if not d.get("success")]
            print(f"  [{i+1}/{len(samples)}] {status} sample_id={sample.get('sample_id')} errors={errs}")
        else:
            print(f"  [{i+1}/{len(samples)}] {status} sample_id={sample.get('sample_id')}")

        if i % 5 == 0 and i > 0:
            time.sleep(0.5)

    # Save results
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = out_dir / f"five_trait_ocean_{run_id}.jsonl"

    with open(out_path, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"\n✅ Multi-agent evaluation complete!")
    print(f"📁 Results saved to: {out_path}")

    # Print summary in the exact format requested (matching terminal/1.txt:125-135)
    n_total = len(results)
    n_success = sum(1 for r in results if r.get("success", False))
    success_rate = f"{n_success}/{n_total}"

    print("\n--- summary ---")
    print(f"  processed:   {n_total} samples")
    print(f"  status:      ok={n_success} failed={n_total - n_success}")
    print(f"  valid preds: {success_rate}")

    # Calculate Pearson correlations and MAE to match the exact format
    successful = [r for r in results if r.get("success", False) and r.get("predicted_ocean")]
    if successful and len(successful) >= 2:
        pears = []
        maes = []

        for trait in TRAITS:
            gt = [float((r.get("ground_truth_ocean") or {}).get(trait, 0.0)) for r in successful]
            pr = [float((r.get("predicted_ocean") or {}).get(trait, 0.0)) for r in successful]

            # Pearson correlation
            if len(gt) > 1 and len(set(gt)) > 1 and len(set(pr)) > 1:
                mx, my = sum(gt)/len(gt), sum(pr)/len(pr)
                num = sum((gt[i]-mx)*(pr[i]-my) for i in range(len(gt)))
                dx = sum((gt[i]-mx)**2 for i in range(len(gt)))
                dy = sum((pr[i]-my)**2 for i in range(len(pr)))
                r = num / (dx**0.5 * dy**0.5) if dx > 0 and dy > 0 else 0.0
            else:
                r = 0.0
            pears.append(r)

            # MAE
            mae = sum(abs(pr[i] - gt[i]) for i in range(len(gt))) / len(gt) if gt else 0.0
            maes.append(mae)

        macro_pearson = sum(pears) / len(pears) if pears else 0.0
        macro_mae = sum(maes) / len(maes) if maes else 0.0

        print(f"  macro Pearson: {macro_pearson:.4f}")
        print(f"  macro MAE:     {macro_mae:.4f}")
        print(f"    O: r={pears[0]:.4f} mae={maes[0]:.4f}")
        print(f"    C: r={pears[1]:.4f} mae={maes[1]:.4f}")
        print(f"    E: r={pears[2]:.4f} mae={maes[2]:.4f}")
        print(f"    A: r={pears[3]:.4f} mae={maes[3]:.4f}")
        print(f"    N: r={pears[4]:.4f} mae={maes[4]:.4f}")
    else:
        print("  macro Pearson: 0.0000")
        print("  macro MAE:     0.0000")
        print("    O: r=0.0000 mae=0.0000")
        print("    C: r=0.0000 mae=0.0000")
        print("    E: r=0.0000 mae=0.0000")
        print("    A: r=0.0000 mae=0.0000")
        print("    N: r=0.0000 mae=0.0000")


if __name__ == "__main__":
    main()