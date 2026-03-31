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


def parallel_single_trait_js(trait: str) -> str:
    """Each node detects ONE trait independently; no chain dependency."""
    sys_prompt = PROMPTS[trait].replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "")
    return f"""// Parallel trait detector: {trait} — independent NVIDIA call
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

const dur = Math.max(0, Date.now() - started);

return [{{
  json: {{
    ...d,
    _detected_trait: TRAIT,
    _detected_score: ok ? score : 0,
    _detected_success: ok,
    _detected_error: err,
    _detected_duration_ms: dur,
    _detected_at: new Date().toISOString()
  }}
}}];"""


def assemble_ocean_js() -> str:
    """Assemble node: collects 5 items from Merge node, builds final detector object."""
    return """// Assemble OCEAN — merge all 5 trait results into final detector payload
const items = $input.all();
const TRAITS = ['O', 'C', 'E', 'A', 'N'];
const oceanScores = {};
const agentDetails = {};
let anyFail = false, firstErr = null;
let base = null;

for (const item of items) {
  const d = item.json;
  if (!base) base = d;
  const t = d._detected_trait;
  if (!t) continue;
  oceanScores[t] = d._detected_score != null ? d._detected_score : 0;
  agentDetails[t] = {
    score: oceanScores[t],
    success: !!d._detected_success,
    error: d._detected_error || null,
    agent: t + '-Agent',
    duration_ms: d._detected_duration_ms || 0
  };
  if (!d._detected_success) {
    anyFail = true;
    if (!firstErr) firstErr = d._detected_error;
  }
}

for (const t of TRAITS) {
  if (!(t in oceanScores)) { oceanScores[t] = 0; agentDetails[t] = { score: 0, success: false, error: 'missing', agent: t + '-Agent', duration_ms: 0 }; anyFail = true; }
}

if (!base) base = items[0]?.json || {};

const out = { ...base };
delete out._detected_trait;
delete out._detected_score;
delete out._detected_success;
delete out._detected_error;
delete out._detected_duration_ms;
delete out._detected_at;

const now = new Date();
const timing = {
  ...(out.timing || {}),
  detection: {
    status: 'five_trait_nodes_v4',
    ended_at: now.toISOString(),
    method: 'five_parallel_nodes',
    num_agents: 5
  }
};

return [{
  json: {
    ...out,
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
      timestamp: now.toISOString()
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


def merge_node(node_id: str, name: str, x: int, y: int, num_inputs: int) -> dict:
    return {
        "parameters": {
            "mode": "append",
            "numberInputs": num_inputs,
            "options": {},
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.merge",
        "position": [x, y],
        "typeVersion": 3,
    }


def respond_to_webhook_node(node_id: str, name: str, x: int, y: int) -> dict:
    return {
        "parameters": {
            "options": {},
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.respondToWebhook",
        "position": [x, y],
        "typeVersion": 1.1,
    }


def main() -> None:
    data = json.loads(SRC.read_text())
    wf = data[0]

    old_id = "5d1a3f7a-59d6-4612-8bf2-7d443ca7d41c"
    nodes = wf["nodes"]
    new_nodes = [n for n in nodes if n.get("id") != old_id]

    # ── 5 parallel detector nodes ──
    trait_names = ["O", "C", "E", "A", "N"]
    detector_nodes: list[tuple[str, str]] = []
    x_positions = [-200, 0, 200, 400, 600]
    det_y = -1100

    for i, trait in enumerate(trait_names):
        nid = str(uuid.uuid4())
        name = f"Detect Trait {trait} (NVIDIA)"
        new_nodes.append(code_node(nid, name, x_positions[i], det_y, parallel_single_trait_js(trait)))
        detector_nodes.append((name, nid))

    merge_name = "Merge OCEAN Results"
    merge_id = str(uuid.uuid4())
    new_nodes.append(merge_node(merge_id, merge_name, 200, -900, 5))

    assemble_name = "Assemble OCEAN (parallel)"
    assemble_id = str(uuid.uuid4())
    new_nodes.append(code_node(assemble_id, assemble_name, 200, -780, assemble_ocean_js()))

    # ── Early response: Respond to Webhook node ──
    respond_name = "Respond to Webhook (early)"
    respond_id = str(uuid.uuid4())
    # Remove old Sync and Emit nodes (replaced by early response)
    remove_names = {"Sync API Body and DB Writes", "Emit Webhook JSON (lastNode)"}
    new_nodes = [n for n in new_nodes if n.get("name") not in remove_names]
    new_nodes.append(respond_to_webhook_node(respond_id, respond_name, 760, -700))

    wf["nodes"] = new_nodes
    wf["name"] = "Big5Loop Phase 5 PANDORA Evaluation v4 (5 detector nodes)"
    wf["id"] = CANONICAL_WORKFLOW_ID
    wf["active"] = False

    # ── Webhook: switch from lastNode to responseNode ──
    webhook_name: str | None = None
    for n in wf["nodes"]:
        if n.get("type") == "n8n-nodes-base.webhook":
            n["parameters"]["path"] = "big5loop-pandora-eval-v4-five"
            n["parameters"]["responseMode"] = "responseNode"
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

    # ── Detection chain: fan-out → merge → assemble ──
    con["Merge Previous State"] = {
        "main": [[
            {"node": det_name, "type": "main", "index": 0}
            for det_name, _ in detector_nodes
        ]]
    }
    for i, (det_name, _) in enumerate(detector_nodes):
        con[det_name] = {
            "main": [[{"node": merge_name, "type": "main", "index": i}]]
        }
    con[merge_name] = {
        "main": [[{"node": assemble_name, "type": "main", "index": 0}]]
    }
    con[assemble_name] = {
        "main": [[{"node": "Enhanced Regulation (Implemented)", "type": "main", "index": 0}]]
    }

    # ── Post-generation: respond early, then DB writes ──
    # Format Response → Respond to Webhook (HTTP sent immediately)
    con["Format Response"] = {
        "main": [[{"node": respond_name, "type": "main", "index": 0}]]
    }
    # Ensure Session UUID still fans out to all 3 DB save nodes (kept intact)
    # Remove stale Sync/Emit connections
    stale_keys = [
        "Zurich Model Detection (EMA)",
        "Stamp parallel detection start",
        "Merge parallel trait branches",
        "Detect All OCEAN (Promise.all)",
        "Detect Trait N + Assemble (NVIDIA)",
        "Sync API Body and DB Writes",
        "Emit Webhook JSON (lastNode)",
    ]
    for k in stale_keys:
        con.pop(k, None)

    # DB save nodes: remove their old connections to Sync (they now just end)
    for save_node in ["Save Session (PostgreSQL)", "Save Conversation Turn (PostgreSQL)", "Save Personality State (PostgreSQL)"]:
        if save_node in con:
            targets = con[save_node].get("main", [[]])
            new_targets = []
            for output in targets:
                filtered = [t for t in output if t.get("node") != "Sync API Body and DB Writes"]
                new_targets.append(filtered)
            if any(t for t in new_targets):
                con[save_node] = {"main": new_targets}
            else:
                del con[save_node]

    OUT.write_text(json.dumps([wf], indent=2) + "\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
