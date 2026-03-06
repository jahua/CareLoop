/**
 * NextChat-Enhanced: Phase 1 Personality Detection API Routes
 * Integrated with NextChat's API patterns
 */

import { NextRequest, NextResponse } from "next/server";
import { nanoid } from "nanoid";

// Phase 1 API Configuration
const PHASE1_API_URL = process.env.PHASE1_API_URL || "http://localhost:3001";
const PHASE1_API_KEY = process.env.PHASE1_API_KEY || "";

interface PersonalityDetectionRequest {
  session_id: string;
  message: string;
  user_id?: string;
  model?: string;
  enable_ema?: boolean;
  enable_verification?: boolean;
}

interface PersonalityState {
  ocean: {
    O: number;
    C: number; 
    E: number;
    A: number;
    N: number;
  };
  ocean_raw?: {
    O: number;
    C: number;
    E: number; 
    A: number;
    N: number;
  };
  stable: boolean;
  confidence_scores: {
    O: number;
    C: number;
    E: number;
    A: number;
    N: number;
  };
  policy_plan: string[];
  ema_applied: boolean;
  ema_alpha: number;
  turn_number: number;
  verification_stats: {
    average_adherence: number;
    refinements_applied: number;
    total_verified: number;
    last_score?: number;
  };
  emotional_state?: string;
  last_updated: string;
}

interface Phase1ApiResponse {
  session_id: string;
  reply: string;
  user_message: string;
  personality_state: PersonalityState;
  regulation: {
    directives: string[];
    analysis: any;
  };
  verification: {
    status: string;
    adherence_score: number;
    refinement_applied: boolean;
  };
  pipeline_status: {
    detector: string;
    regulator: string;
    generator: string;
    verifier: string;
    database: string;
  };
  api_metadata: {
    response_time: string;
    version: string;
    pipeline_type: string;
    turn_index: number;
  };
}

// Personality Detection Endpoint
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { session_id, message, user_id, model, enable_ema = true, enable_verification = true } = body as PersonalityDetectionRequest;

    if (!session_id || !message) {
      return NextResponse.json(
        { error: "Missing required parameters: session_id and message" },
        { status: 400 }
      );
    }

    // Forward request to Phase 1 API
    const phase1Response = await fetch(`${PHASE1_API_URL}/api/chat/message`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(PHASE1_API_KEY && { Authorization: `Bearer ${PHASE1_API_KEY}` }),
      },
      body: JSON.stringify({
        session_id,
        message,
        user_id,
        model,
        enable_ema,
        enable_verification,
      }),
    });

    if (!phase1Response.ok) {
      throw new Error(`Phase 1 API error: ${phase1Response.status}`);
    }

    const phase1Data: Phase1ApiResponse = await phase1Response.json();

    // Transform response to match NextChat patterns
    const response = {
      id: nanoid(),
      role: "assistant" as const,
      content: phase1Data.reply,
      timestamp: new Date().toISOString(),
      
      // Phase 1 Enhanced Data
      personality_state: phase1Data.personality_state,
      regulation: phase1Data.regulation,
      verification: phase1Data.verification,
      pipeline_status: phase1Data.pipeline_status,
      api_metadata: phase1Data.api_metadata,
      
      // NextChat compatibility
      model: model || "personality-adaptive-gpt4",
      session_id: phase1Data.session_id,
      
      // Agent metadata
      agents_involved: [
        "personality-detector",
        "behavioral-regulator", 
        "response-generator",
        "quality-verifier",
        "session-coordinator",
      ],
      
      // Performance metrics
      processing_time: phase1Data.api_metadata.response_time,
      quality_score: phase1Data.verification.adherence_score,
      ema_applied: phase1Data.personality_state.ema_applied,
    };

    return NextResponse.json(response);
    
  } catch (error) {
    console.error("Personality detection error:", error);
    
    return NextResponse.json(
      {
        error: "Personality detection failed",
        details: error instanceof Error ? error.message : "Unknown error",
        fallback_response: "I apologize, but I'm experiencing technical difficulties with the personality detection system. Let me try to help you anyway - how are you feeling today?",
      },
      { status: 500 }
    );
  }
}

// Get Session Personality State
export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const session_id = url.searchParams.get("session_id");
    
    if (!session_id) {
      return NextResponse.json(
        { error: "Missing session_id parameter" },
        { status: 400 }
      );
    }

    // Get personality state from Phase 1 API
    const response = await fetch(`${PHASE1_API_URL}/api/chat/session/${session_id}`, {
      headers: {
        ...(PHASE1_API_KEY && { Authorization: `Bearer ${PHASE1_API_KEY}` }),
      },
    });

    if (!response.ok) {
      throw new Error(`Phase 1 API error: ${response.status}`);
    }

    const sessionData = await response.json();
    
    return NextResponse.json({
      session_id,
      personality_state: sessionData.personality_state || null,
      conversation_summary: sessionData.conversation_summary || null,
      total_turns: sessionData.total_turns || 0,
      created_at: sessionData.created_at || new Date().toISOString(),
      agents_performance: {
        total_processed: sessionData.total_turns || 0,
        average_confidence: sessionData.personality_state?.confidence_scores 
          ? Object.values(sessionData.personality_state.confidence_scores).reduce((a: number, b: number) => a + b, 0) / 5
          : 0,
        verification_stats: sessionData.personality_state?.verification_stats || {
          average_adherence: 0,
          refinements_applied: 0,
          total_verified: 0,
        },
      },
    });
    
  } catch (error) {
    console.error("Session retrieval error:", error);
    
    return NextResponse.json(
      {
        error: "Failed to retrieve session data",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}

// Delete/Reset Session
export async function DELETE(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const session_id = url.searchParams.get("session_id");
    
    if (!session_id) {
      return NextResponse.json(
        { error: "Missing session_id parameter" },
        { status: 400 }
      );
    }

    // Delete session from Phase 1 API (if endpoint exists)
    try {
      await fetch(`${PHASE1_API_URL}/api/chat/session/${session_id}`, {
        method: "DELETE",
        headers: {
          ...(PHASE1_API_KEY && { Authorization: `Bearer ${PHASE1_API_KEY}` }),
        },
      });
    } catch (deleteError) {
      console.warn("Failed to delete session from Phase 1 API:", deleteError);
      // Continue anyway - client-side state will be reset
    }

    return NextResponse.json({
      success: true,
      message: `Session ${session_id} reset successfully`,
      session_id,
    });
    
  } catch (error) {
    console.error("Session reset error:", error);
    
    return NextResponse.json(
      {
        error: "Failed to reset session",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}

















































