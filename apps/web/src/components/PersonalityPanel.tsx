"use client";

import type { PersonalityState } from "./types";

const TRAIT_NAMES: Record<string, string> = {
  O: "Openness",
  C: "Conscientiousness",
  E: "Extraversion",
  A: "Agreeableness",
  N: "Neuroticism",
};

function normalizeTrait(value: number): number {
  return Math.max(0, Math.min(100, ((value + 1) / 2) * 100));
}

function barVariant(value: number): "low" | "mid" | "high" {
  if (value > 0.3) return "high";
  if (value < -0.3) return "low";
  return "mid";
}

type PersonalityPanelProps = {
  personality: PersonalityState;
};

export default function PersonalityPanel({ personality }: PersonalityPanelProps) {
  const order = ["O", "C", "E", "A", "N"] as const;

  if (!personality?.ocean || Object.keys(personality.ocean).length === 0) {
    return (
      <div className="careloop-panel__section">
        <h3 className="careloop-panel__title">Personality</h3>
        <p className="careloop-panel__hint">
          OCEAN traits will appear as the assistant learns your style.
        </p>
      </div>
    );
  }

  return (
    <div className="careloop-panel__section">
      <h3 className="careloop-panel__title">
        Personality
        <span
          className={`careloop-badge ${personality.stable ? "careloop-badge--stable" : "careloop-badge--learning"}`}
        >
          {personality.stable ? "Stable" : "Learning"}
        </span>
      </h3>

      {order.map((key) => {
        const value = personality.ocean[key] ?? 0;
        const pct = normalizeTrait(value);
        const variant = barVariant(value);
        const confidence = personality.confidence_scores?.[key];
        return (
          <div key={key} className="careloop-trait">
            <div className="careloop-trait__header">
              <span className="careloop-trait__name">
                {TRAIT_NAMES[key] ?? key}
              </span>
              <span className="careloop-trait__value">
                {value.toFixed(2)}
                {confidence != null && (
                  <span className="careloop-trait__conf">
                    {" "}({Math.round(confidence * 100)}%)
                  </span>
                )}
              </span>
            </div>
            <div className="careloop-trait__bar">
              <div
                className={`careloop-trait__bar-fill careloop-trait__bar-fill--${variant}`}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        );
      })}

      {personality.ema_applied && (
        <p className="careloop-panel__hint" style={{ marginTop: 8 }}>
          EMA smoothing applied
        </p>
      )}
    </div>
  );
}
