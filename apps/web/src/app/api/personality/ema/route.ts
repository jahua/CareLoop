import { NextRequest, NextResponse } from "next/server";
import type { ErrorCode, ErrorStage } from "@big5loop/contracts";

/** Phase 3: structured error envelope (Spec §12). */
function errorResponse(
  error_code: ErrorCode,
  message: string,
  status: number,
  options?: { stage?: ErrorStage; retryable?: boolean }
): NextResponse {
  return NextResponse.json(
    {
      success: false as const,
      error: {
        error_code,
        message,
        stage: options?.stage ?? "unknown",
        retryable: options?.retryable ?? false,
      },
      timestamp: new Date().toISOString(),
    },
    { status }
  );
}

const OCEAN_KEYS = ["O", "C", "E", "A", "N"] as const;
const DEFAULT_ALPHA = 0.3;
const CONFIDENCE_THRESHOLD = 0.4;
const STABILITY_TURNS = 6;
const STABILITY_VARIANCE_THRESHOLD = 0.05;

type OceanScores = Record<(typeof OCEAN_KEYS)[number], number>;
type ConfidenceScores = Record<(typeof OCEAN_KEYS)[number], number>;

interface DetectionOutput {
  ocean: OceanScores;
  confidence: ConfidenceScores;
  reasoning: string;
}

interface RequestBody {
  previous_state?: { ocean: OceanScores; confidence: ConfidenceScores } | null;
  ocean_history?: OceanScores[];
  detection_output: DetectionOutput;
  alpha?: number;
}

function applyEMA(
  previous: OceanScores | null,
  detection: DetectionOutput,
  alpha: number
): { ocean: OceanScores; confidence: ConfidenceScores; ema_applied: boolean } {
  const ocean: OceanScores = { O: 0, C: 0, E: 0, A: 0, N: 0 };
  const confidence = { ...detection.confidence };
  let ema_applied = false;
  for (const k of OCEAN_KEYS) {
    const conf = detection.confidence[k];
    const detected = detection.ocean[k];
    if (previous === null || conf < CONFIDENCE_THRESHOLD) {
      ocean[k] = previous === null ? detected : previous[k];
      if (previous === null) ema_applied = true;
    } else {
      ocean[k] = alpha * detected + (1 - alpha) * previous[k];
      ema_applied = true;
    }
  }
  return { ocean, confidence, ema_applied };
}

function oceanVariance(history: OceanScores[]): number {
  if (history.length < 2) return 0;
  let sum = 0;
  for (const k of OCEAN_KEYS) {
    const values = history.map((h) => h[k]);
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const variance = values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length;
    sum += variance;
  }
  return sum / OCEAN_KEYS.length;
}

function isStable(history: OceanScores[]): boolean {
  if (history.length < STABILITY_TURNS) return false;
  const recent = history.slice(-STABILITY_TURNS);
  return oceanVariance(recent) <= STABILITY_VARIANCE_THRESHOLD;
}

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as RequestBody;
    const { previous_state, ocean_history = [], detection_output, alpha = DEFAULT_ALPHA } = body;
    if (!detection_output?.ocean || !detection_output?.confidence) {
      return errorResponse(
        "validation_failed",
        "detection_output with ocean and confidence required",
        400,
        { stage: "detection", retryable: false }
      );
    }
    const previous =
      previous_state?.ocean && previous_state?.confidence
        ? previous_state.ocean
        : null;
    const result = applyEMA(previous, detection_output, alpha);
    const stable = isStable([...ocean_history, result.ocean]);
    return NextResponse.json({
      ...result,
      stable,
    });
  } catch (e) {
    const message = e instanceof Error ? e.message : "Request failed";
    return errorResponse("internal_error", message, 500, { stage: "ema", retryable: true });
  }
}
