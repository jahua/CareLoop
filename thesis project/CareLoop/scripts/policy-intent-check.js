/* eslint-disable no-console */

const API_URL = process.env.CARELOOP_API_URL || "http://localhost:3003/api/chat";

const cases = [
  {
    expected: "policy_navigation",
    message: "What are the IV eligibility rules in Zurich and which official forms are required?",
  },
  {
    expected: "policy_navigation",
    message: "Explain the allowance application procedure and policy documents I need to submit.",
  },
  {
    expected: "mixed",
    message: "I feel stressed and need help understanding IV benefit eligibility in my canton.",
  },
  {
    expected: "mixed",
    message: "I am anxious and confused about policy forms for caregiver support benefits.",
  },
  {
    expected: "practical_education",
    message: "Teach me a step-by-step caregiving routine and practical daily plan.",
  },
  {
    expected: "emotional_support",
    message: "I feel exhausted and lonely and just need emotional support right now.",
  },
];

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

async function main() {
  const sessionId = crypto.randomUUID();
  let correct = 0;

  for (let i = 0; i < cases.length; i += 1) {
    const c = cases[i];
    const result = await sendTurn(sessionId, i + 1, c.message);
    const actual = String(result?.coaching_mode ?? "missing");
    const ok = actual === c.expected;
    if (ok) correct += 1;
    console.log(
      `Case ${i + 1}: expected=${c.expected}, actual=${actual}, pass=${ok ? "yes" : "no"}`
    );
  }

  const accuracy = (correct / cases.length) * 100;
  console.log(`Policy-intent routing accuracy: ${accuracy.toFixed(1)}% (${correct}/${cases.length})`);

  // Phase-2 foundation gate: require at least 80% on this initial mini-benchmark.
  if (accuracy < 80) {
    process.exitCode = 1;
    return;
  }

  console.log("Policy-intent routing check passed.");
}

main().catch((error) => {
  console.error(`Policy-intent check failed: ${error.message}`);
  process.exit(1);
});
