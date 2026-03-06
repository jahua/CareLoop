"use client";

import { useState, useEffect, useCallback } from "react";
import {
  getRecentSessions,
  removeRecentSession,
  type RecentSession,
} from "@/lib/session-storage";
import ThemeToggle from "./ThemeToggle";

type SessionSidebarProps = {
  currentSessionId: string;
  onSelectSession: (sessionId: string) => void;
  onNewChat: () => void;
};

function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

export default function SessionSidebar({
  currentSessionId,
  onSelectSession,
  onNewChat,
}: SessionSidebarProps) {
  const [sessions, setSessions] = useState<RecentSession[]>([]);

  const refresh = useCallback(() => {
    setSessions(getRecentSessions());
  }, []);

  useEffect(() => {
    refresh();
  }, [currentSessionId, refresh]);

  const handleRemove = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    removeRecentSession(id);
    refresh();
  };

  return (
    <aside className="careloop-sidebar">
      <div className="careloop-sidebar__header">
        <div className="careloop-sidebar__brand">
          <span className="careloop-sidebar__logo">CareLoop</span>
          <ThemeToggle />
        </div>
        <button
          type="button"
          className="careloop-sidebar__new-btn"
          onClick={onNewChat}
        >
          + New Chat
        </button>
      </div>

      <div className="careloop-sidebar__sessions">
        {sessions.length === 0 ? (
          <div className="careloop-sidebar__empty">
            No conversations yet.
            <br />
            Start chatting!
          </div>
        ) : (
          sessions.map((s) => (
            <button
              key={s.id}
              type="button"
              className={`careloop-session-item ${s.id === currentSessionId ? "careloop-session-item--active" : ""}`}
              onClick={() => onSelectSession(s.id)}
            >
              <span className="careloop-session-item__title">{s.label}</span>
              <span className="careloop-session-item__meta">
                <span>{s.messageCount} msgs</span>
                <span>{timeAgo(s.lastUsed)}</span>
                {s.id !== currentSessionId && (
                  <span
                    role="button"
                    tabIndex={0}
                    className="careloop-session-item__delete"
                    onClick={(e) => handleRemove(e, s.id)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleRemove(e as unknown as React.MouseEvent, s.id);
                    }}
                    title="Remove from list"
                  >
                    ✕
                  </span>
                )}
              </span>
            </button>
          ))
        )}
      </div>

      <div className="careloop-sidebar__footer">
        <span style={{ fontSize: 11, color: "var(--color-text-muted)" }}>
          {sessions.length} conversation{sessions.length !== 1 ? "s" : ""}
        </span>
      </div>
    </aside>
  );
}
