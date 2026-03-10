/* eslint-disable no-console */

const API_URL = process.env.BIG5LOOP_API_URL || "http://localhost:3003/api/chat";
const sessionId = crypto.randomUUID();

const turns = [
  "I feel overwhelmed and anxious today.",
  "How to build a daily caregiving routine with clear steps and a plan?",
  "I am worried about IV eligibility benefits in my canton and feel stressed.",
  "I feel lonely and exhausted recently.",
  "Can you guide me with practical techniques to organize medication reminders?",
  "I am anxious about policy forms and eligibility procedure for allowance support.",
];

async function sendTurn(message, turnIndex) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      turn_index: turnIndex,
      message,
      context: { language: "en", canton: "ZH" },
    }),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(`Turn ${turnIndex} failed: HTTP ${response.status} ${JSON.stringify(data)}`);
  }
  return data;
}

async function main() {
  console.log(`Session: ${sessionId}`);
  const seenModes = new Set();

  for (let i = 0; i < turns.length; i += 1) {
    const result = await sendTurn(turns[i], i + 1);
    const mode = result?.coaching_mode ?? "missing";
    const stable = result?.personality_state?.stable ?? null;
    const verifier = result?.pipeline_status?.verifier ?? "missing";
    seenModes.add(mode);

    console.log(
      `Turn ${i + 1}: mode=${mode}, stable=${String(stable)}, verifier=${verifier}, msg="${turns[i]}"`
    );
  }

  const requiredModes = ["emotional_support", "practical_education", "mixed"];
  const missingModes = requiredModes.filter((mode) => !seenModes.has(mode));

  console.log(`Seen modes: ${Array.from(seenModes).join(", ")}`);
  if (missingModes.length > 0) {
    console.log(`Missing expected modes: ${missingModes.join(", ")}`);
    process.exitCode = 1;
    return;
  }

  console.log("Runtime mode-routing check passed.");
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
