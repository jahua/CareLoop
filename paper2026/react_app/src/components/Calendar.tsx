import React from "react";

function formatDate(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function Calendar() {
  const [current, setCurrent] = React.useState<Date>(new Date());

  const addYears = (delta: number) => {
    setCurrent((prev) => {
      const next = new Date(prev);
      next.setFullYear(prev.getFullYear() + delta);
      return next;
    });
  };

  const addMonths = (delta: number) => {
    setCurrent((prev) => {
      const next = new Date(prev);
      // setDate to 1st to avoid month overflow issues (e.g., Jan 31 + 1 month)
      const day = next.getDate();
      next.setDate(1);
      next.setMonth(prev.getMonth() + delta);
      // restore day, clamped to end of month
      const endOfMonth = new Date(next.getFullYear(), next.getMonth() + 1, 0).getDate();
      next.setDate(Math.min(day, endOfMonth));
      return next;
    });
  };

  const addDays = (delta: number) => {
    setCurrent((prev) => {
      const next = new Date(prev);
      next.setDate(prev.getDate() + delta);
      return next;
    });
  };

  const groupStyle: React.CSSProperties = { display: "flex", gap: 8, alignItems: "center" };
  const btnStyle: React.CSSProperties = {
    padding: "6px 10px",
    borderRadius: 6,
    border: "1px solid #d1d5db",
    background: "#f9fafb",
    cursor: "pointer",
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <div>
        <strong>Date:</strong> {formatDate(current)}
      </div>
      <div style={groupStyle}>
        <span>Year</span>
        <button style={btnStyle} onClick={() => addYears(-1)}>-</button>
        <button style={btnStyle} onClick={() => addYears(1)}>+</button>
      </div>
      <div style={groupStyle}>
        <span>Month</span>
        <button style={btnStyle} onClick={() => addMonths(-1)}>-</button>
        <button style={btnStyle} onClick={() => addMonths(1)}>+</button>
      </div>
      <div style={groupStyle}>
        <span>Day</span>
        <button style={btnStyle} onClick={() => addDays(-1)}>-</button>
        <button style={btnStyle} onClick={() => addDays(1)}>+</button>
      </div>
    </div>
  );
}