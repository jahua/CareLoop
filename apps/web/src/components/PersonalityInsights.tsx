"use client";

import type { PersonalityState } from "./types";

const TRAIT_META: Record<
  string,
  { name: string; highLabel: string; lowLabel: string; description: string }
> = {
  O: {
    name: "Openness",
    highLabel: "Curious, creative",
    lowLabel: "Practical, conventional",
    description: "Reflects intellectual curiosity, creativity, and preference for variety.",
  },
  C: {
    name: "Conscientiousness",
    highLabel: "Organized, disciplined",
    lowLabel: "Flexible, spontaneous",
    description: "Indicates self-discipline, orderliness, and goal-directed behavior.",
  },
  E: {
    name: "Extraversion",
    highLabel: "Outgoing, energetic",
    lowLabel: "Reserved, reflective",
    description: "Measures sociability, assertiveness, and positive emotionality.",
  },
  A: {
    name: "Agreeableness",
    highLabel: "Cooperative, trusting",
    lowLabel: "Competitive, skeptical",
    description: "Reflects compassion, cooperativeness, and social harmony.",
  },
  N: {
    name: "Neuroticism",
    highLabel: "Sensitive, anxious",
    lowLabel: "Resilient, calm",
    description: "Indicates emotional instability, anxiety, and moodiness.",
  },
};

function interpret(value: number): "low" | "moderate" | "high" {
  if (value > 0.3) return "high";
  if (value < -0.3) return "low";
  return "moderate";
}

type PersonalityInsightsProps = {
  personality: PersonalityState;
};

export default function PersonalityInsights({ personality }: PersonalityInsightsProps) {
  if (!personality?.ocean || Object.keys(personality.ocean).length === 0) {
    return (
      <div className="big5loop-panel__section">
        <h3 className="big5loop-panel__title">Personality Insights</h3>
        <p className="big5loop-panel__hint">
          Insights will appear after a few exchanges as OCEAN traits are detected.
        </p>
      </div>
    );
  }

  const order = ["O", "C", "E", "A", "N"] as const;
  const strongTraits = order.filter(
    (k) => Math.abs(personality.ocean[k] ?? 0) > 0.3
  );
  const overallConf = personality.confidence_scores
    ? Object.values(personality.confidence_scores).reduce((a, b) => a + b, 0) /
      Object.values(personality.confidence_scores).length
    : null;

  return (
    <div className="big5loop-panel__section">
      <h3 className="big5loop-panel__title">
        Insights
        <span
          className={`big5loop-badge ${personality.stable ? "big5loop-badge--stable" : "big5loop-badge--learning"}`}
        >
          {personality.stable ? "Stable" : "Learning"}
        </span>
      </h3>

      {/* Overview cards */}
      <div className="big5loop-insights__overview">
        {overallConf != null && (
          <div className="big5loop-insights__stat">
            <span className="big5loop-insights__stat-value">
              {Math.round(overallConf * 100)}%
            </span>
            <span className="big5loop-insights__stat-label">Confidence</span>
          </div>
        )}
        <div className="big5loop-insights__stat">
          <span className="big5loop-insights__stat-value">
            {strongTraits.length}
          </span>
          <span className="big5loop-insights__stat-label">Strong traits</span>
        </div>
        {personality.history && (
          <div className="big5loop-insights__stat">
            <span className="big5loop-insights__stat-value">
              {personality.history.length}
            </span>
            <span className="big5loop-insights__stat-label">Snapshots</span>
          </div>
        )}
      </div>

      {/* Trait interpretation cards */}
      <div className="big5loop-insights__traits">
        {order.map((key) => {
          const value = personality.ocean[key] ?? 0;
          const meta = TRAIT_META[key];
          const level = interpret(value);
          const conf = personality.confidence_scores?.[key];
          return (
            <div key={key} className="big5loop-insights__trait-card">
              <div className="big5loop-insights__trait-top">
                <span className="big5loop-insights__trait-name">
                  {meta.name}
                </span>
                <span
                  className={`big5loop-insights__trait-level big5loop-insights__trait-level--${level}`}
                >
                  {level}
                </span>
              </div>
              <p className="big5loop-insights__trait-desc">
                {level === "high" ? meta.highLabel : level === "low" ? meta.lowLabel : `Between ${meta.lowLabel.toLowerCase()} and ${meta.highLabel.toLowerCase()}`}
              </p>

              {/* EMA visualization: raw → smoothed */}
              <div className="big5loop-insights__trait-bar-wrap">
                <div className="big5loop-insights__trait-bar">
                  <div
                    className={`big5loop-insights__trait-bar-fill big5loop-insights__trait-bar-fill--${level}`}
                    style={{ width: `${Math.max(0, Math.min(100, ((value + 1) / 2) * 100))}%` }}
                  />
                  <div className="big5loop-insights__trait-bar-center" />
                </div>
                <div className="big5loop-insights__trait-values">
                  <span>{value.toFixed(2)}</span>
                  {conf != null && (
                    <span className="big5loop-insights__trait-conf">
                      {Math.round(conf * 100)}% conf
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {personality.ema_applied && (
        <p className="big5loop-panel__hint" style={{ marginTop: 8 }}>
          Values smoothed with Exponential Moving Average (EMA)
        </p>
      )}
    </div>
  );
}
