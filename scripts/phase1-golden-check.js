/* eslint-disable no-console */

const API_URL = process.env.BIG5LOOP_API_URL || "http://localhost:3003/api/chat";

async function sendTurn(sessionId, turnIndex, message) {
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
    throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
  }
  return data;
}

function assertCondition(condition, message) {
  if (!condition) throw new Error(message);
}

async function runHighNGolden() {
  const sessionId = crypto.randomUUID();
  const prompt = "I feel very anxious, overwhelmed, and worried all the time.";
  const result = await sendTurn(sessionId, 1, prompt);

  const n = Number(result?.personality_state?.ocean?.N ?? 0);
  const mode = String(result?.coaching_mode ?? "");
  const content = String(result?.message?.content ?? "");

  assertCondition(content.length > 0, "high-N: empty response content");
  assertCondition(mode === "emotional_support", `high-N: expected emotional_support, got ${mode}`);
  assertCondition(n > 0, `high-N: expected N > 0, got ${n}`);
}

async function runHighCGolden() {
  const sessionId = crypto.randomUUID();
  const prompt = "Please give me a clear step-by-step plan and structured routine for daily caregiving.";
  const result = await sendTurn(sessionId, 1, prompt);

  const c = Number(result?.personality_state?.ocean?.C ?? 0);
  const mode = String(result?.coaching_mode ?? "");
  const content = String(result?.message?.content ?? "");

  assertCondition(content.length > 0, "high-C: empty response content");
  assertCondition(mode === "practical_education", `high-C: expected practical_education, got ${mode}`);
  assertCondition(c > 0, `high-C: expected C > 0, got ${c}`);
}

async function main() {
  await runHighNGolden();
  console.log("high-N golden check passed");

  await runHighCGolden();
  console.log("high-C golden check passed");

  console.log("Phase 1 golden regression checks passed.");
}

main().catch((error) => {
  console.error(`Golden check failed: ${error.message}`);
  process.exit(1);
});
