"use client";

import type { HealthStatus } from "./types";

const COLORS: Record<HealthStatus, string> = {
  healthy: "#10b981",
  degraded: "#f59e0b",
  offline: "#ef4444",
  unknown: "#9ca3af",
};

const LABELS: Record<HealthStatus, string> = {
  healthy: "All systems operational",
  degraded: "Service degraded",
  offline: "Service offline",
  unknown: "Checking status…",
};

type StatusDotProps = {
  status: HealthStatus;
};

export default function StatusDot({ status }: StatusDotProps) {
  return (
    <span
      className="careloop-status-dot"
      style={{ background: COLORS[status] }}
      title={LABELS[status]}
      aria-label={LABELS[status]}
      role="status"
    />
  );
}
