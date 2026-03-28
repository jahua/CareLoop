#!/usr/bin/env python3
"""Build big5loop-pandora-eval-v4-five-detectors.json from pandora eval v4 (single detector replaced by 5 trait nodes)."""
from __future__ import annotations

import copy
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workflows" / "n8n" / "big5loop-pandora-eval-v4.json"
OUT = ROOT / "workflows" / "n8n" / "big5loop-pandora-eval-v4-five-detectors.json"

# Keep stable so `n8n import:workflow` updates the same workflow and CLI publish targets match prod.
CANONICAL_WORKFLOW_ID = "940251a5-dd5b-4f5f-b024-513023536523"

PROMPTS: dict[str, str] = {
    "O": """You are an Openness detection specialist. Analyze the linguistic style of this Reddit-style message for Openness ONLY.

Focus on: abstract thinking, novelty-seeking, intellectual curiosity, unconventional framing, exploration of ideas vs concrete, literal, repetitive, or rigid thinking patterns.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly abstract, philosophical, curious, novel thinking
- +0.3 to +0.7 = moderately open, some intellectual curiosity
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = highly concrete, literal, repetitive, rigid thinking

Output ONLY a JSON object with key "O" containing a float from -1.0 to 1.0.
Be decisive. Look for strong linguistic evidence of cognitive style.""",
    "C": """You are a Conscientiousness detection specialist. Analyze the linguistic style of this Reddit-style message for Conscientiousness ONLY.

Focus on: structured, planful, disciplined, organized language vs impulsive, disorganized, inconsistent, or scattered expression.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly structured, planful, disciplined, organized communication
- +0.3 to +0.7 = moderately conscientious, some self-regulation
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = highly impulsive, disorganized, inconsistent, scattered

Output ONLY a JSON object with key "C" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic evidence of self-regulation and structure.""",
    "E": """You are an Extraversion detection specialist. Analyze the linguistic style of this Reddit-style message for Extraversion ONLY.

Focus on: energetic, assertive, socially engaging, outgoing style vs restrained, withdrawn, low-energy, or avoidant communication.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly energetic, assertive, socially engaging, outgoing style
- +0.3 to +0.7 = moderately extraverted, some social energy
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = restrained, withdrawn, low-energy, avoidant communication

Output ONLY a JSON object with key "E" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic markers of social activation and energy.""",
    "A": """You are an Agreeableness detection specialist. Analyze the linguistic style of this Reddit-style message for Agreeableness ONLY.

Focus on: empathetic, cooperative, warm, tactful stance vs hostile, contemptuous, combative, or self-centered tone.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = highly empathetic, cooperative, warm, tactful communication
- +0.3 to +0.7 = moderately agreeable, some warmth
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = hostile, contemptuous, combative, self-centered tone

Output ONLY a JSON object with key "A" containing a float from -1.0 to 1.0.
Be decisive. Focus on interpersonal stance and emotional tone.""",
    "N": """You are a Neuroticism detection specialist. Analyze the linguistic style of this Reddit-style message for Neuroticism ONLY.

Focus on: anxious, reactive, ruminative, emotionally volatile language vs calm, regulated, steady, emotionally stable expression.

You MUST use the FULL range [-1.0, 1.0]. Do not be conservative.
- +0.8 to +1.0 = high emotional volatility, rumination, anxiety markers
- +0.3 to +0.7 = moderately emotionally reactive
- -0.3 to +0.2 = neutral or mixed evidence
- -0.8 to -1.0 = calm, regulated, steady, emotionally stable communication

Output ONLY a JSON object with key "N" containing a float from -1.0 to 1.0.
Be decisive. Look for linguistic markers of emotional regulation.""",
}


def intermediate_detector_js(trait: str) -> str:
    sys_prompt = PROMPTS[trait].replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "")
    # sys_prompt will be inserted inside JS single-quoted string — avoid single quotes in prompts (none in PROMPTS)
    return f"""// Trait detector {trait} (1/5) — NVIDIA single-trait call
const TRAIT = '{trait}';
const d = $input.first().json;
if (d && d.success === false && d.error) return $input.all();
const userText = String(d.clean_msg || d.user_message || '').trim();

let apiKey = '';
try {{ apiKey = process.env.NVIDIA_API_KEY || ''; }} catch (_) {{}}
if (!apiKey) try {{ apiKey = (typeof $env !== 'undefined' && $env.NVIDIA_API_KEY) || ''; }} catch (_) {{}}
let apiUrl = '';
try {{ apiUrl = process.env.NVIDIA_API_URL || ''; }} catch (_) {{}}
if (!apiUrl) apiUrl = 'https://integrate.api.nvidia.com/v1/chat/completions';
let model = 'meta/llama-3.1-70b-instruct';
try {{ model = process.env.NVIDIA_MODEL || model; }} catch (_) {{}}
if (!model) try {{ model = (typeof $env !== 'undefined' && $env.NVIDIA_MODEL) || model; }} catch (_) {{}}

const systemPrompt = `{sys_prompt.replace("`", "\\`")}`;

const started = Date.now();
let score = 0;
let ok = false;
let err = null;
if (apiKey && apiKey.length > 10) {{
  try {{
    const body = await this.helpers.httpRequest({{
      url: apiUrl,
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json', Authorization: 'Bearer ' + apiKey }},
      body: {{
        model,
        messages: [
          {{ role: 'system', content: systemPrompt }},
          {{ role: 'user', content: 'Analyze this user message (Reddit-style):\\n' + userText }}
        ],
        temperature: 0.25,
        max_tokens: 120
      }},
      timeout: 30000,
      json: true
    }});
    const raw = String(body?.choices?.[0]?.message?.content || '');
    const re = new RegExp('"' + TRAIT + '"\\\\s*:\\\\s*(-?[0-9]+\\\\.?[0-9]*)');
    const m = raw.match(re);
    if (m) {{
      score = Math.max(-1, Math.min(1, parseFloat(m[1])));
      ok = true;
    }} else {{
      const i = raw.indexOf('{{');
      const j = raw.lastIndexOf('}}');
      if (i >= 0 && j > i) {{
        const o = JSON.parse(raw.slice(i, j + 1));
        if (typeof o[TRAIT] === 'number') {{
          score = Math.max(-1, Math.min(1, o[TRAIT]));
          ok = true;
        }}
      }}
    }}
  }} catch (e) {{ err = String(e.message || e); }}
}} else {{ err = 'missing_api_key'; }}

const chainStart = d._detection_chain_start != null ? d._detection_chain_start : started;
const dur = Math.max(0, Date.now() - started);
const partial = {{ ...(d._partial_ocean || {{}}) }};
partial[TRAIT] = ok ? score : 0;
const details = {{ ...(d._partial_agent_details || {{}}) }};
details[TRAIT] = {{ score: partial[TRAIT], success: ok, error: err, agent: TRAIT + '-Agent', duration_ms: dur }};

return [{{
  json: {{
    ...d,
    _detection_chain_start: chainStart,
    _partial_ocean: partial,
    _partial_agent_details: details
  }}
}}];"""


def stamp_parallel_detection_js() -> str:
    return """// Shared wall-clock start for all parallel trait branches.
const d = $input.first().json;
if (d && d.success === false && d.error) return $input.all();
return [{ json: { ...d, _detection_chain_start: Date.now() } }];"""


def assemble_parallel_traits_js() -> str:
    """Merge outputs of Merge (append): O, C, E, A, N items → one regulation payload."""
    return """// Assemble OCEAN from five parallel trait branches (Merge append → 5 items).
const items = $input.all();
if (!items.length) {
  return [{
    json: {
      success: false,
      error: {
        error_code: 'internal_error',
        message: 'No parallel detection items returned.',
        stage: 'detection',
        retryable: true
      }
    }
  }];
}
const first = items[0].json;
if (first && first.success === false && first.error) return [{ json: first }];

let oceanScores = {};
let agentDetails = {};
let chainStart = first._detection_chain_start;
for (const item of items) {
  const j = item.json || {};
  if (j.success === false && j.error) continue;
  if (j._partial_ocean && typeof j._partial_ocean === 'object') {
    oceanScores = { ...oceanScores, ...j._partial_ocean };
  }
  if (j._partial_agent_details && typeof j._partial_agent_details === 'object') {
    agentDetails = { ...agentDetails, ...j._partial_agent_details };
  }
  if (chainStart == null && j._detection_chain_start != null) chainStart = j._detection_chain_start;
}
if (chainStart == null) chainStart = Date.now();

const TRAITS = ['O', 'C', 'E', 'A', 'N'];
for (const t of TRAITS) {
  if (oceanScores[t] === undefined) oceanScores[t] = 0;
}

const detectionEndedAt = Date.now();
const timing = {
  ...(first.timing || {}),
  detection: {
    status: 'five_trait_nodes_v4',
    started_at: new Date(chainStart).toISOString(),
    ended_at: new Date(detectionEndedAt).toISOString(),
    duration_ms: Math.max(0, detectionEndedAt - chainStart),
    method: 'five_parallel_nvidia_calls',
    num_agents: 5
  }
};

const d = { ...first };
delete d._detection_chain_start;
delete d._partial_ocean;
delete d._partial_agent_details;

let anyFail = false;
let firstErr = null;
for (const t of TRAITS) {
  const ad = agentDetails[t];
  if (ad && !ad.success) {
    anyFail = true;
    if (!firstErr) firstErr = ad.error || 'trait_call_failed';
  }
}

return [{
  json: {
    ...d,
    timing,
    detector: {
      api_status: anyFail ? 'degraded' : 'five_trait_nodes_v4',
      error: anyFail ? (firstErr || 'one_or_more_trait_calls_failed') : null,
      method: 'five_trait_nodes_v4',
      num_agents: 5,
      traits_covered: TRAITS,
      ocean_detected: oceanScores,
      agent_details: agentDetails,
      personality_stable: true,
      smoothed_ocean: oceanScores,
      smoothed_confidence: { O: 0.75, C: 0.75, E: 0.75, A: 0.75, N: 0.75 },
      timestamp: new Date().toISOString()
    },
    ocean_disc: oceanScores,
    predicted_ocean: oceanScores,
    agent_details: agentDetails,
    method: 'five_trait_nodes_v4'
  }
}];"""


def code_node(node_id: str, name: str, x: int, y: int, js: str) -> dict:
    return {
        "parameters": {"jsCode": js},
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.code",
        "position": [x, y],
        "typeVersion": 2,
    }


def merge_parallel_node(node_id: str, name: str, x: int, y: int) -> dict:
    return {
        "parameters": {"mode": "append", "numberInputs": 5, "options": {}},
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.merge",
        "position": [x, y],
        "typeVersion": 3.2,
    }


def main() -> None:
    data = json.loads(SRC.read_text())
    wf = data[0]

    old_id = "5d1a3f7a-59d6-4612-8bf2-7d443ca7d41c"
    nodes = wf["nodes"]
    new_nodes = [n for n in nodes if n.get("id") != old_id]

    # Parallel layout: stamp → O,C,E,A,N (same x) → merge (append) → assemble → regulation
    stamp_id = str(uuid.uuid4())
    merge_id = str(uuid.uuid4())
    assemble_id = str(uuid.uuid4())
    chain = [
        ("Detect Trait O (NVIDIA)", intermediate_detector_js("O"), -1040),
        ("Detect Trait C (NVIDIA)", intermediate_detector_js("C"), -920),
        ("Detect Trait E (NVIDIA)", intermediate_detector_js("E"), -800),
        ("Detect Trait A (NVIDIA)", intermediate_detector_js("A"), -680),
        ("Detect Trait N (NVIDIA)", intermediate_detector_js("N"), -560),
    ]
    new_nodes.append(code_node(stamp_id, "Stamp parallel detection start", 128, -896, stamp_parallel_detection_js()))
    for label, js, y in chain:
        nid = str(uuid.uuid4())
        new_nodes.append(code_node(nid, label, 280, y, js))
    new_nodes.append(merge_parallel_node(merge_id, "Merge parallel trait branches", 520, -896))
    new_nodes.append(
        code_node(assemble_id, "Assemble OCEAN (parallel)", 720, -896, assemble_parallel_traits_js())
    )

    wf["nodes"] = new_nodes
    wf["name"] = "Big5Loop Phase 5 PANDORA Evaluation v4 (5 detector nodes)"
    wf["id"] = CANONICAL_WORKFLOW_ID
    wf["active"] = False

    webhook_name: str | None = None
    for n in wf["nodes"]:
        if n.get("type") == "n8n-nodes-base.webhook":
            n["parameters"]["path"] = "big5loop-pandora-eval-v4-five"
            n["name"] = "Webhook Trigger (POST PANDORA eval v4 five detectors)"
            n["id"] = str(uuid.uuid4())
            n["webhookId"] = str(uuid.uuid4())
            webhook_name = n["name"]
            break

    con = wf["connections"]
    if webhook_name:
        for k in list(con.keys()):
            if k != webhook_name and k.startswith("Webhook Trigger"):
                payload = con.pop(k, None)
                if payload is not None and webhook_name not in con:
                    con[webhook_name] = payload
                break
    stamp_name = "Stamp parallel detection start"
    merge_name = "Merge parallel trait branches"
    assemble_name = "Assemble OCEAN (parallel)"

    con["Merge Previous State"] = {"main": [[{"node": stamp_name, "type": "main", "index": 0}]]}
    con[stamp_name] = {
        "main": [
            [
                {"node": chain[0][0], "type": "main", "index": 0},
                {"node": chain[1][0], "type": "main", "index": 0},
                {"node": chain[2][0], "type": "main", "index": 0},
                {"node": chain[3][0], "type": "main", "index": 0},
                {"node": chain[4][0], "type": "main", "index": 0},
            ]
        ]
    }
    for merge_input_idx, (detector_name, _, _) in enumerate(chain):
        con[detector_name] = {
            "main": [[{"node": merge_name, "type": "main", "index": merge_input_idx}]]
        }
    con[merge_name] = {"main": [[{"node": assemble_name, "type": "main", "index": 0}]]}
    con[assemble_name] = {
        "main": [[{"node": "Enhanced Regulation (Implemented)", "type": "main", "index": 0}]]
    }
    if "Zurich Model Detection (EMA)" in con:
        del con["Zurich Model Detection (EMA)"]

    OUT.write_text(json.dumps([wf], indent=2) + "\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
