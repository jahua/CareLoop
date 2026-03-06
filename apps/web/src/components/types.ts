export type Citation = {
  source_id: string;
  title: string;
  url: string;
};

export type PipelineMeta = {
  mode_confidence?: number;
  mode_routing_reason?: string;
  pipeline_status?: Record<string, string>;
  stage_timings?: Array<{ stage: string; ms: number }>;
  agents_involved?: string[];
};

export type Message = {
  role: "user" | "assistant";
  content: string;
  turn_index?: number;
  request_id?: string;
  timestamp?: string;
  latency_ms?: number;
  citations?: Citation[];
  pipeline?: PipelineMeta;
};

export type Ocean = Record<string, number>;

export type PersonalitySnapshot = {
  ocean: Ocean;
  timestamp: string;
};

export type PersonalityState = {
  ocean: Ocean;
  stable?: boolean;
  ema_applied?: boolean;
  confidence_scores?: Record<string, number>;
  history?: PersonalitySnapshot[];
} | null;

export type ChatMode = "simple" | "standard" | "detailed";

export type HealthStatus = "healthy" | "degraded" | "offline" | "unknown";

export type AgentInfo = {
  name: string;
  role: string;
  status: "active" | "idle" | "processing" | "error";
  metrics?: {
    success_rate?: number;
    avg_time_ms?: number;
    processed?: number;
  };
};
