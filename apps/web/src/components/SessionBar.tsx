"use client";

import type { PersonalityState } from "./types";

const useGateway =
  typeof process !== "undefined" &&
  (process.env.NEXT_PUBLIC_USE_GATEWAY === "true" ||
    process.env.NEXT_PUBLIC_USE_GATEWAY === "1");

type SessionBarProps = {
  sessionId: string;
  messageCount: number;
  coachingMode: string | null;
  personality: PersonalityState;
  /** null = unknown, true = healthy, false = unhealthy */
  healthOk?: boolean | null;
  /** Number of thumbs-up this session */
  helpfulCount?: number;
  onCopySessionId?: () => void;
};

export default function SessionBar({
  sessionId,
  messageCount,
  coachingMode,
  personality,
  healthOk = null,
  helpfulCount = 0,
  onCopySessionId,
}: SessionBarProps) {
  const shortId = sessionId ? `${sessionId.slice(0, 8)}…` : "—";

  const copySession = () => {
    if (sessionId) {
      navigator.clipboard.writeText(sessionId);
      onCopySessionId?.();
    }
  };

  return (
    <div className="careloop-session-bar">
      {useGateway && (
        <div className="careloop-session-bar__item">
          <span
            className="careloop-session-bar__badge careloop-session-bar__badge--gateway"
            title="Requests go through gateway (shadow logging may be active)"
          >
            Gateway
          </span>
        </div>
      )}
      {healthOk === false && (
        <div className="careloop-session-bar__item">
          <span className="careloop-session-bar__badge careloop-session-bar__badge--error">
            Offline
          </span>
        </div>
      )}
      <div className="careloop-session-bar__item">
        <span>Session</span>
        <button
          type="button"
          className="careloop-session-bar__value careloop-copy-id"
          onClick={copySession}
          title="Copy session ID"
        >
          {shortId}
        </button>
      </div>
      <div className="careloop-session-bar__item">
        <span>Messages</span>
        <span className="careloop-session-bar__value">{messageCount}</span>
      </div>
      {helpfulCount > 0 && (
        <div className="careloop-session-bar__item">
          <span>Helpful</span>
          <span className="careloop-session-bar__value">{helpfulCount}</span>
        </div>
      )}
      {coachingMode && (
        <div className="careloop-session-bar__item">
          <span>Mode</span>
          <span
            className="careloop-session-bar__badge careloop-session-bar__badge--mode"
            title={`Coaching mode: ${coachingMode}`}
          >
            {coachingMode.replace(/_/g, " ")}
          </span>
        </div>
      )}
      {personality && (
        <div className="careloop-session-bar__item">
          <span>Personality</span>
          <span
            className={
              personality.stable
                ? "careloop-session-bar__badge careloop-session-bar__badge--stable"
                : "careloop-session-bar__badge careloop-session-bar__badge--learning"
            }
          >
            {personality.stable ? "Stable" : "Learning"}
          </span>
        </div>
      )}
    </div>
  );
}
