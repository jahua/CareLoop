"use client";

import { useState, useCallback } from "react";
import { exportSessionData, deleteSessionData } from "@/lib/api";

type DataActionsProps = {
  sessionId: string;
  onDeleted?: () => void;
};

export default function DataActions({ sessionId, onDeleted }: DataActionsProps) {
  const [status, setStatus] = useState<
    "idle" | "exporting" | "deleting" | "export-ok" | "export-err" | "delete-ok" | "delete-err"
  >("idle");
  const [message, setMessage] = useState<string | null>(null);

  const handleExport = useCallback(async () => {
    if (!sessionId) return;
    setStatus("exporting");
    setMessage(null);
    const result = await exportSessionData(sessionId);
    if ("error" in result) {
      setStatus("export-err");
      setMessage(result.error);
      return;
    }
    setStatus("export-ok");
    setMessage("Downloading…");
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `big5loop-export-${sessionId.slice(0, 8)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    setTimeout(() => { setStatus("idle"); setMessage(null); }, 2000);
  }, [sessionId]);

  const handleDelete = useCallback(async () => {
    if (!sessionId) return;
    if (
      typeof window !== "undefined" &&
      !window.confirm("Delete all data for this session? This cannot be undone.")
    ) return;
    setStatus("deleting");
    setMessage(null);
    const result = await deleteSessionData(sessionId);
    if ("error" in result) {
      setStatus("delete-err");
      setMessage(result.error);
      return;
    }
    setStatus("delete-ok");
    setMessage("Deleted.");
    onDeleted?.();
    setTimeout(() => { setStatus("idle"); setMessage(null); }, 2000);
  }, [sessionId, onDeleted]);

  const busy = status === "exporting" || status === "deleting";

  return (
    <div className="big5loop-panel__section">
      <h3 className="big5loop-panel__title">Session Data</h3>
      <div className="big5loop-panel-actions">
        <button
          type="button"
          className="big5loop-panel-actions__btn"
          onClick={handleExport}
          disabled={busy}
        >
          {status === "exporting" ? "Exporting…" : "Export data"}
        </button>
        <button
          type="button"
          className="big5loop-panel-actions__btn big5loop-panel-actions__btn--danger"
          onClick={handleDelete}
          disabled={busy}
        >
          {status === "deleting" ? "Deleting…" : "Delete data"}
        </button>
        {message && (
          <p className={`big5loop-panel-actions__msg ${status.endsWith("-err") ? "big5loop-panel-actions__msg--err" : ""}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}
