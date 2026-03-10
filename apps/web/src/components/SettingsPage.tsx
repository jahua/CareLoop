"use client";

import { useState } from "react";
import { useAuth } from "@/components/AuthProvider";

export default function SettingsPage() {
  const { user, refresh } = useAuth();
  const [displayName, setDisplayName] = useState(user?.name ?? "");
  const [currentPw, setCurrentPw] = useState("");
  const [newPw, setNewPw] = useState("");
  const [msg, setMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);
  const [saving, setSaving] = useState(false);

  const saveProfile = async () => {
    setSaving(true);
    setMsg(null);
    try {
      const res = await fetch("/api/auth/update-profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ displayName }),
      });
      const data = await res.json();
      if (!res.ok) { setMsg({ type: "err", text: data.error ?? "Failed" }); return; }
      setMsg({ type: "ok", text: "Profile updated" });
      refresh();
    } catch { setMsg({ type: "err", text: "Network error" }); }
    finally { setSaving(false); }
  };

  const changePassword = async () => {
    if (newPw.length < 6) { setMsg({ type: "err", text: "Password must be at least 6 characters" }); return; }
    setSaving(true);
    setMsg(null);
    try {
      const res = await fetch("/api/auth/change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ currentPassword: currentPw, newPassword: newPw }),
      });
      const data = await res.json();
      if (!res.ok) { setMsg({ type: "err", text: data.error ?? "Failed" }); return; }
      setMsg({ type: "ok", text: "Password changed" });
      setCurrentPw("");
      setNewPw("");
    } catch { setMsg({ type: "err", text: "Network error" }); }
    finally { setSaving(false); }
  };

  return (
    <div className="big5loop-page">
      <div className="big5loop-page__header">
        <h1>Settings</h1>
        <p className="big5loop-page__subtitle">Manage your account and preferences</p>
      </div>

      <div className="big5loop-page__content">
        {msg && (
          <div className={`big5loop-page__alert big5loop-page__alert--${msg.type}`}>
            {msg.text}
          </div>
        )}

        <section className="big5loop-card">
          <h2 className="big5loop-card__title">Profile</h2>
          <div className="big5loop-form-row">
            <label>Email</label>
            <input type="email" value={user?.email ?? ""} disabled className="big5loop-input big5loop-input--disabled" />
          </div>
          <div className="big5loop-form-row">
            <label>Display Name</label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="big5loop-input"
            />
          </div>
          <button className="big5loop-btn big5loop-btn--primary" onClick={saveProfile} disabled={saving}>
            {saving ? "Saving…" : "Save Profile"}
          </button>
        </section>

        <section className="big5loop-card">
          <h2 className="big5loop-card__title">Change Password</h2>
          <div className="big5loop-form-row">
            <label>Current Password</label>
            <input
              type="password"
              value={currentPw}
              onChange={(e) => setCurrentPw(e.target.value)}
              className="big5loop-input"
              autoComplete="current-password"
            />
          </div>
          <div className="big5loop-form-row">
            <label>New Password</label>
            <input
              type="password"
              value={newPw}
              onChange={(e) => setNewPw(e.target.value)}
              className="big5loop-input"
              placeholder="At least 6 characters"
              autoComplete="new-password"
            />
          </div>
          <button className="big5loop-btn big5loop-btn--primary" onClick={changePassword} disabled={saving}>
            {saving ? "Saving…" : "Change Password"}
          </button>
        </section>

        <section className="big5loop-card">
          <h2 className="big5loop-card__title">Account Info</h2>
          <div className="big5loop-info-grid">
            <div className="big5loop-info-item">
              <span className="big5loop-info-label">User ID</span>
              <span className="big5loop-info-value big5loop-info-value--mono">{user?.id?.slice(0, 8)}…</span>
            </div>
            <div className="big5loop-info-item">
              <span className="big5loop-info-label">Email</span>
              <span className="big5loop-info-value">{user?.email}</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
