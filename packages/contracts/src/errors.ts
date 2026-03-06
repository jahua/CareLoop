/**
 * Structured error envelope for Phase 3 (Spec §12, §17.2).
 * All failure paths must return this shape; no raw stack traces to clients.
 */
import { z } from "zod";

/** Stable error codes aligned with Spec §12 failure handling */
export const ERROR_CODES = [
  "detector_fallback",
  "rag_fallback",
  "verifier_fallback",
  "timeout_fallback",
  "ema_divergence",
  "mixed_mode_overflow",
  "language_fallback",
  "validation_failed",
  "internal_error",
] as const;

export type ErrorCode = (typeof ERROR_CODES)[number];

export const ErrorCodeSchema = z.enum(ERROR_CODES);

/** Pipeline stage where the error occurred (for correlation and logs) */
export const ErrorStageSchema = z.enum([
  "ingest",
  "detection",
  "ema",
  "routing",
  "retrieval",
  "generation",
  "verification",
  "persistence",
  "unknown",
]);

export type ErrorStage = z.infer<typeof ErrorStageSchema>;

/** Structured error envelope returned to clients and used in logs */
export const StructuredErrorSchema = z.object({
  error_code: ErrorCodeSchema,
  message: z.string(),
  stage: ErrorStageSchema.optional(),
  retryable: z.boolean().optional(),
  request_id: z.string().optional(),
  session_id: z.string().uuid().optional(),
});

export type StructuredError = z.infer<typeof StructuredErrorSchema>;

/** Response shape when the pipeline returns an error (e.g. fallback) */
export const ErrorResponseEnvelopeSchema = z.object({
  success: z.literal(false),
  error: StructuredErrorSchema,
  /** Optional safe fallback content for display (e.g. clarification prompt) */
  fallback_content: z.string().optional(),
  timestamp: z.string().datetime().optional(),
});

export type ErrorResponseEnvelope = z.infer<typeof ErrorResponseEnvelopeSchema>;

/** Parse and validate; throws on invalid shape */
export function parseStructuredError(data: unknown): StructuredError {
  return StructuredErrorSchema.parse(data);
}

/** Safe parse; returns { success, data } or { success: false, error } */
export function safeParseStructuredError(data: unknown): z.SafeParseReturnType<unknown, StructuredError> {
  return StructuredErrorSchema.safeParse(data);
}

export function parseErrorResponseEnvelope(data: unknown): ErrorResponseEnvelope {
  return ErrorResponseEnvelopeSchema.parse(data);
}

export function safeParseErrorResponseEnvelope(
  data: unknown
): z.SafeParseReturnType<unknown, ErrorResponseEnvelope> {
  return ErrorResponseEnvelopeSchema.safeParse(data);
}
