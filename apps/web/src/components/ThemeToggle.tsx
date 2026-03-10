"use client";

import { useTheme } from "./ThemeProvider";

export default function ThemeToggle() {
  const { theme, setTheme, resolved } = useTheme();

  const cycle = () => {
    if (theme === "light") setTheme("dark");
    else if (theme === "dark") setTheme("system");
    else setTheme("light");
  };

  const label =
    theme === "system"
      ? `System (${resolved})`
      : theme === "dark"
        ? "Dark"
        : "Light";

  return (
    <button
      type="button"
      className="big5loop-theme-toggle"
      onClick={cycle}
      aria-label={`Theme: ${label}. Click to switch.`}
      title={`Theme: ${label}`}
    >
      {resolved === "dark" ? "🌙" : "☀️"}
      <span className="big5loop-theme-toggle__label">{label}</span>
    </button>
  );
}
