"use client";

type HealthBannerProps = {
  onDismiss?: () => void;
};

export default function HealthBanner({ onDismiss }: HealthBannerProps) {
  return (
    <div
      className="careloop-health-banner"
      role="alert"
      aria-live="polite"
    >
      <span className="careloop-health-banner__text">
        Service temporarily unavailable. Check that the API and N8N are running.
      </span>
      {onDismiss && (
        <button
          type="button"
          className="careloop-health-banner__dismiss"
          onClick={onDismiss}
          aria-label="Dismiss health warning"
        >
          Dismiss
        </button>
      )}
    </div>
  );
}
