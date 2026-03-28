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


def concurrent_five_trait_detection_js() -> str:
    """Single Code node: fires 5 NVIDIA calls with Promise.all → true parallelism."""
    prompt_entries = []
    for trait in ["O", "C", "E", "A", "N"]:
        sys_prompt = PROMPTS[trait].replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "").replace("`", "\\`")
        prompt_entries.append(f"  {trait}: `{sys_prompt}`")
    prompts_obj = ",\n".join(prompt_entries)

    return """// ── Concurrent 5-trait OCEAN detection (Promise.all) ──
const d = $input.first().json;
if (d && d.success === false && d.error) return $input.all();
const userText = String(d.clean_msg || d.user_message || '').trim();

let apiKey = '';
try { apiKey = process.env.NVIDIA_API_KEY || ''; } catch (_) {}
if (!apiKey) try { apiKey = (typeof $env !== 'undefined' && $env.NVIDIA_API_KEY) || ''; } catch (_) {}
let apiUrl = '';
try { apiUrl = process.env.NVIDIA_API_URL || ''; } catch (_) {}
if (!apiUrl) apiUrl = 'https://integrate.api.nvidia.com/v1/chat/completions';
let model = 'meta/llama-3.1-70b-instruct';
try { model = process.env.NVIDIA_MODEL || model; } catch (_) {}
if (!model) try { model = (typeof $env !== 'undefined' && $env.NVIDIA_MODEL) || model; } catch (_) {}

const PROMPTS = {
""" + prompts_obj + """
};

const TRAITS = ['O', 'C', 'E', 'A', 'N'];
const chainStart = Date.now();
const oceanScores = {};
const agentDetails = {};

async function detectTrait(trait) {
  const started = Date.now();
  let score = 0, ok = false, err = null;
  if (!apiKey || apiKey.length <= 10) { err = 'missing_api_key'; }
  else {
    try {
      const body = await this.helpers.httpRequest({
        url: apiUrl,
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + apiKey },
        body: {
          model,
          messages: [
            { role: 'system', content: PROMPTS[trait] },
            { role: 'user', content: 'Analyze this user message (Reddit-style):\\n' + userText }
          ],
          temperature: 0.25,
          max_tokens: 120
        },
        timeout: 30000,
        json: true
      });
      const raw = String(body?.choices?.[0]?.message?.content || '');
      const re = new RegExp('"' + trait + '"\\\\s*:\\\\s*(-?[0-9]+\\\\.?[0-9]*)');
      const m = raw.match(re);
      if (m) {
        score = Math.max(-1, Math.min(1, parseFloat(m[1])));
        ok = true;
      } else {
        const i = raw.indexOf('{');
        const j = raw.lastIndexOf('}');
        if (i >= 0 && j > i) {
          const o = JSON.parse(raw.slice(i, j + 1));
          if (typeof o[trait] === 'number') {
            score = Math.max(-1, Math.min(1, o[trait]));
            ok = true;
          }
        }
      }
    } catch (e) { err = String(e.message || e); }
  }
  const dur = Math.max(0, Date.now() - started);
  return { trait, score: ok ? score : 0, success: ok, error: err, duration_ms: dur };
}

const results = await Promise.all(
  TRAITS.map(t => detectTrait.call(this, t))
);

let anyFail = false, firstErr = null;
for (const r of results) {
  oceanScores[r.trait] = r.score;
  agentDetails[r.trait] = {
    score: r.score, success: r.success, error: r.error,
    agent: r.trait + '-Agent', duration_ms: r.duration_ms
  };
  if (!r.success) { anyFail = true; if (!firstErr) firstErr = r.error; }
}

const detectionEndedAt = Date.now();
const timing = {
  ...(d.timing || {}),
  detection: {
    status: 'five_trait_nodes_v4',
    started_at: new Date(chainStart).toISOString(),
    ended_at: new Date(detectionEndedAt).toISOString(),
    duration_ms: Math.max(0, detectionEndedAt - chainStart),
    method: 'promise_all_five_concurrent',
    num_agents: 5
  }
};

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


def main() -> None:
    data = json.loads(SRC.read_text())
    wf = data[0]

    old_id = "5d1a3f7a-59d6-4612-8bf2-7d443ca7d41c"
    nodes = wf["nodes"]
    new_nodes = [n for n in nodes if n.get("id") != old_id]

    # Single node with Promise.all for true concurrent 5-trait detection
    detect_all_id = str(uuid.uuid4())
    detect_all_name = "Detect All OCEAN (Promise.all)"
    new_nodes.append(
        code_node(detect_all_id, detect_all_name, 240, -896, concurrent_five_trait_detection_js())
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
    con["Merge Previous State"] = {
        "main": [[{"node": detect_all_name, "type": "main", "index": 0}]]
    }
    con[detect_all_name] = {
        "main": [[{"node": "Enhanced Regulation (Implemented)", "type": "main", "index": 0}]]
    }
    stale_keys = [
        "Zurich Model Detection (EMA)",
        "Stamp parallel detection start",
        "Detect Trait O (NVIDIA)",
        "Detect Trait C (NVIDIA)",
        "Detect Trait E (NVIDIA)",
        "Detect Trait A (NVIDIA)",
        "Detect Trait N (NVIDIA)",
        "Detect Trait N + Assemble (NVIDIA)",
        "Merge parallel trait branches",
        "Assemble OCEAN (parallel)",
    ]
    for k in stale_keys:
        con.pop(k, None)

    OUT.write_text(json.dumps([wf], indent=2) + "\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
