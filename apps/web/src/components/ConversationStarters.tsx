"use client";

const STARTERS = [
  {
    label: "Feeling overwhelmed",
    prompt: "I'm feeling overwhelmed with caregiving responsibilities. Can you help?",
  },
  {
    label: "Daily routine tips",
    prompt: "Give me a step-by-step plan to manage my daily caregiving routine better.",
  },
  {
    label: "Zurich caregiver benefits",
    prompt: "What benefits and support are available for caregivers in Canton Zurich?",
  },
  {
    label: "Self-care strategies",
    prompt: "What are practical self-care strategies for someone caring for an elderly parent?",
  },
];

type ConversationStartersProps = {
  onSelect: (prompt: string) => void;
};

export default function ConversationStarters({ onSelect }: ConversationStartersProps) {
  return (
    <div className="careloop-starters">
      <div className="careloop-starters__grid">
        {STARTERS.map((s) => (
          <button
            key={s.label}
            type="button"
            className="careloop-starters__card"
            onClick={() => onSelect(s.prompt)}
          >
            <span className="careloop-starters__label">{s.label}</span>
            <span className="careloop-starters__preview">{s.prompt}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
