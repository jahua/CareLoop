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
    <div className="big5loop-session-bar">
      {useGateway && (
        <div className="big5loop-session-bar__item">
          <span
            className="big5loop-session-bar__badge big5loop-session-bar__badge--gateway"
            title="Requests go through gateway (shadow logging may be active)"
          >
            Gateway
          </span>
        </div>
      )}
      {healthOk === false && (
        <div className="big5loop-session-bar__item">
          <span className="big5loop-session-bar__badge big5loop-session-bar__badge--error">
            Offline
          </span>
        </div>
      )}
      <div className="big5loop-session-bar__item">
        <span>Session</span>
        <button
          type="button"
          className="big5loop-session-bar__value big5loop-copy-id"
          onClick={copySession}
          title="Copy session ID"
        >
          {shortId}
        </button>
      </div>
      <div className="big5loop-session-bar__item">
        <span>Messages</span>
        <span className="big5loop-session-bar__value">{messageCount}</span>
      </div>
      {helpfulCount > 0 && (
        <div className="big5loop-session-bar__item">
          <span>Helpful</span>
          <span className="big5loop-session-bar__value">{helpfulCount}</span>
        </div>
      )}
      {coachingMode && (
        <div className="big5loop-session-bar__item">
          <span>Mode</span>
          <span
            className="big5loop-session-bar__badge big5loop-session-bar__badge--mode"
            title={`Coaching mode: ${coachingMode}`}
          >
            {coachingMode.replace(/_/g, " ")}
          </span>
        </div>
      )}
      {personality && (
        <div className="big5loop-session-bar__item">
          <span>Personality</span>
          <span
            className={
              personality.stable
                ? "big5loop-session-bar__badge big5loop-session-bar__badge--stable"
                : "big5loop-session-bar__badge big5loop-session-bar__badge--learning"
            }
          >
            {personality.stable ? "Stable" : "Learning"}
          </span>
        </div>
      )}
    </div>
  );
}
