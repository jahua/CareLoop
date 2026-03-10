import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

/**
 * Phase 3 P1-10: Health check for availability monitoring (Spec §15.1.F, §17.6).
 * GET /api/health – use for gateway/load-balancer health checks and SLO availability.
 */
export function GET() {
  return NextResponse.json({
    ok: true,
    service: "big5loop-web",
    timestamp: new Date().toISOString(),
  });
}
