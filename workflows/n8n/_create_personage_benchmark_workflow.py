#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import re
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_WORKFLOW = ROOT / "workflows" / "n8n" / "big5loop-phase1-2-postgres-mvp-v2.json"
OUTPUT_WORKFLOW = ROOT / "workflows" / "n8n" / "big5loop-phase1-2-postgres-mvp-v2-personage-benchmark.json"
PROMPT_BANK_PATH = ROOT / "evaluation_data" / "personage" / "isolated" / "prompt_bank.py"
PERSONAGE_DATASET = ROOT / "evaluation_data" / "personage" / "processed" / "personage_eval.jsonl"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def js_quote(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def build_detection_block(prompt_bank, dataset_rows: list[dict]) -> str:
    rows_by_id = {row["id"]: row for row in dataset_rows}
    missing = [row_id for row_id in prompt_bank.EXEMPLAR_IDS if row_id not in rows_by_id]
    if missing:
        raise ValueError(f"Missing exemplar ids: {missing}")

    variant_items = []
    for name, system in prompt_bank.SYSTEM_PROMPTS.items():
        variant_items.append(f"{{name:{js_quote(name)},system:{js_quote(system)}}}")
    variants_js = "[" + ",".join(variant_items) + "]"

    fewshot_items = []
    for row_id in prompt_bank.EXEMPLAR_IDS:
        row = rows_by_id[row_id]
        fewshot_items.append(
            "{u:%s,a:%s}" % (
                js_quote(row["input"]),
                js_quote(json.dumps(row["ground_truth_ocean"], ensure_ascii=False)),
            )
        )
    fewshot_js = "[" + ",".join(fewshot_items) + "]"

    return f"""if (apiKey && apiKey.length > 10) {{
    const promptVariants = {variants_js};
    const fewShot = {fewshot_js};
    const parseOcean = (raw) => {{
      const m = String(raw || '').match(/\\{{[^}}]+\\}}/);
      if (!m) return null;
      const p = JSON.parse(m[0]);
      if (typeof p.O !== 'number') return null;
      return {{
        O: clamp(p.O, -1, 1),
        C: clamp(p.C || 0, -1, 1),
        E: clamp(p.E || 0, -1, 1),
        A: clamp(p.A || 0, -1, 1),
        N: clamp(p.N || 0, -1, 1)
      }};
    }};

    const variantOutputs = [];
    for (const variant of promptVariants) {{
      const msgs = [{{ role: 'system', content: variant.system }}];
      for (const ex of fewShot) {{
        msgs.push({{ role: 'user', content: `Utterance: "${{ex.u}}"` }});
        msgs.push({{ role: 'assistant', content: ex.a }});
      }}
      msgs.push({{ role: 'user', content: `Utterance: "${{userText.slice(0, 600)}}"` }});

      try {{
        const body = await this.helpers.httpRequest({{
          url: apiUrl,
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json', 'Authorization': `Bearer ${{apiKey}}` }},
          body: {{ model, messages: msgs, temperature: 0.1, max_tokens: 140 }},
          timeout: 45000,
          json: true
        }});
        const raw = body?.choices?.[0]?.message?.content || '';
        const parsed = parseOcean(raw);
        variantOutputs.push({{ name: variant.name, raw, ocean: parsed }});
      }} catch (variantErr) {{
        variantOutputs.push({{ name: variant.name, raw: null, ocean: null, error: variantErr.message || String(variantErr) }});
      }}
    }}

    const valid = variantOutputs.filter(v => v.ocean);
    if (valid.length > 0) {{
      ocean = {{ O: 0, C: 0, E: 0, A: 0, N: 0 }};
      for (const item of valid) {{
        for (const trait of ['O', 'C', 'E', 'A', 'N']) {{
          ocean[trait] += Number(item.ocean[trait] || 0);
        }}
      }}
      for (const trait of ['O', 'C', 'E', 'A', 'N']) {{
        ocean[trait] = clamp(ocean[trait] / valid.length, -1, 1);
      }}
      confidence = {{ O:0.85, C:0.85, E:0.85, A:0.85, N:0.85 }};
      apiStatus = 'nvidia_ensemble';
      formatUsed = 'api-ensemble';
    }} else {{
      apiError = 'No valid JSON across benchmark variants';
    }}
  }} else {{ apiError = `No API key (len=${{apiKey.length}})`; }}"""


def update_detection_js(js_code: str, detection_block: str) -> str:
    pattern = re.compile(
        r"if \(apiKey && apiKey\.length > 10\) \{.*?\} else \{ apiError = `No API key \(len=\$\{apiKey\.length\}\)`; \}",
        re.DOTALL,
    )
    updated = pattern.sub(lambda _match: detection_block, js_code, count=1)
    if updated == js_code:
        raise RuntimeError("Failed to replace detection API block in workflow jsCode")
    updated = updated.replace("apiStatus = 'nvidia'; formatUsed = 'api';", "apiStatus = 'nvidia_ensemble'; formatUsed = 'api-ensemble';")
    updated = updated.replace(
        "status: apiStatus === 'nvidia' ? 'ok' : 'fallback',",
        "status: String(apiStatus).startsWith('nvidia') ? 'ok' : 'fallback',",
    )
    return updated


def main() -> None:
    prompt_bank = load_module(PROMPT_BANK_PATH, "prompt_bank")
    dataset_rows = prompt_bank.load_jsonl(PERSONAGE_DATASET)

    raw = json.loads(SOURCE_WORKFLOW.read_text(encoding="utf-8"))
    is_list = isinstance(raw, list)
    workflow = copy.deepcopy(raw[0] if is_list else raw)

    workflow.pop("id", None)
    workflow.pop("createdAt", None)
    workflow.pop("updatedAt", None)
    workflow["name"] = "Big5Loop Phase1-2 PostgreSQL V2 PERSONAGE Benchmark (Ensemble)"
    workflow["active"] = False

    new_webhook_id = str(uuid.uuid4())
    detection_block = build_detection_block(prompt_bank, dataset_rows)

    for node in workflow.get("nodes", []):
        node["id"] = str(uuid.uuid4())
        if node.get("name") == "Webhook Trigger (POST Zurich)":
            params = node.setdefault("parameters", {})
            params["path"] = "big5loop-turn-personage-benchmark"
            node["webhookId"] = new_webhook_id
        if node.get("name") == "Zurich Model Detection (EMA)":
            params = node.setdefault("parameters", {})
            params["jsCode"] = update_detection_js(params.get("jsCode", ""), detection_block)

    output = [workflow] if is_list else workflow
    OUTPUT_WORKFLOW.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {OUTPUT_WORKFLOW}")


if __name__ == "__main__":
    main()
