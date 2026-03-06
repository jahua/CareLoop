/**
 * Data export (right to access) – Phase 3 P1-11.
 * GET /api/data/export?session_id=<uuid>
 * When DATABASE_URL (or AUDIT_DATABASE_URL) is set, returns session data bundle. Optional: set DATA_API_KEY and send x-api-key header.
 * See docs/DATA-EXPORT-AND-DELETION.md.
 */

import { NextRequest, NextResponse } from "next/server";
import { hasDatabase, withDb } from "@/lib/db";
import { exportSessionData } from "@/lib/data-export";

export const dynamic = "force-dynamic";

const DATA_API_KEY = process.env.DATA_API_KEY ?? "";

function requireAuth(request: NextRequest): NextResponse | null {
  if (!DATA_API_KEY) return null;
  const key = request.headers.get("x-api-key") || request.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (key !== DATA_API_KEY) {
    return NextResponse.json({ error: "Unauthorized. Provide x-api-key or Authorization header." }, { status: 401 });
  }
  return null;
}

export async function GET(request: NextRequest) {
  const authError = requireAuth(request);
  if (authError) return authError;

  const sessionId = request.nextUrl.searchParams.get("session_id");
  if (!sessionId) {
    return NextResponse.json({ error: "Missing session_id query parameter." }, { status: 400 });
  }
  const uuidRe = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (!uuidRe.test(sessionId)) {
    return NextResponse.json({ error: "Invalid session_id format (UUID required)." }, { status: 400 });
  }

  if (!hasDatabase()) {
    return NextResponse.json(
      {
        success: false,
        message: "Data export not configured. Set DATABASE_URL (or AUDIT_DATABASE_URL). See docs/DATA-EXPORT-AND-DELETION.md.",
        doc: "CareLoop/docs/DATA-EXPORT-AND-DELETION.md",
      },
      { status: 501 }
    );
  }

  try {
    const bundle = await withDb((client) => exportSessionData(client, sessionId));
    return NextResponse.json({ success: true, data: bundle });
  } catch (e) {
    const message = e instanceof Error ? e.message : "Export failed";
    return NextResponse.json({ success: false, error: message }, { status: 500 });
  }
}
