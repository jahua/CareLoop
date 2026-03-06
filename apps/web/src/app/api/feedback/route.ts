import { NextRequest, NextResponse } from "next/server";
import { feedbackLog } from "@/lib/feedback";

export const dynamic = "force-dynamic";

/**
 * Phase 3 P1-5: Optional post-turn feedback (Spec §11, ROADMAP §6.3 DoD).
 * POST body: { session_id, turn_index?, request_id?, thumbs_up_down?: 'up'|'down', helpfulness_score?: number }
 * Does not block; always returns 202 when accepted.
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => null);
    if (!body || typeof body !== "object") {
      return NextResponse.json({ error: "JSON body required" }, { status: 400 });
    }
    const session_id = typeof body.session_id === "string" ? body.session_id.trim() : "";
    if (!session_id) {
      return NextResponse.json({ error: "session_id required" }, { status: 400 });
    }
    const turn_index =
      typeof body.turn_index === "number" && Number.isInteger(body.turn_index) ? body.turn_index : undefined;
    const request_id = typeof body.request_id === "string" ? body.request_id.trim() || undefined : undefined;
    let thumbs_up_down: "up" | "down" | undefined;
    if (body.thumbs_up_down === "up" || body.thumbs_up_down === "down") {
      thumbs_up_down = body.thumbs_up_down;
    }
    let helpfulness_score: number | undefined;
    if (typeof body.helpfulness_score === "number" && body.helpfulness_score >= 0 && body.helpfulness_score <= 5) {
      helpfulness_score = body.helpfulness_score;
    }
    if (!thumbs_up_down && helpfulness_score === undefined) {
      return NextResponse.json(
        { error: "At least one of thumbs_up_down or helpfulness_score (0–5) required" },
        { status: 400 }
      );
    }
    const payload = {
      session_id,
      turn_index,
      request_id,
      thumbs_up_down,
      helpfulness_score,
      timestamp: new Date().toISOString(),
    };
    feedbackLog(payload);
    return NextResponse.json({ ok: true }, { status: 202 });
  } catch {
    return NextResponse.json({ error: "Request failed" }, { status: 500 });
  }
}
