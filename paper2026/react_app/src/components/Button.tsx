import React from "react";

type ButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary";
};

export function Button({ children, onClick, variant = "primary" }: ButtonProps) {
  const base = {
    padding: "8px 12px",
    borderRadius: "6px",
    border: "1px solid transparent",
    cursor: "pointer",
    fontSize: 14,
  } as const;

  const styles =
    variant === "primary"
      ? { ...base, backgroundColor: "#2563eb", color: "white" }
      : { ...base, backgroundColor: "#e5e7eb", color: "#111827" };

  return (
    <button style={styles} onClick={onClick}>
      {children}
    </button>
  );
}






































