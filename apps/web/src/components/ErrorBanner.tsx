"use client";

type ErrorBannerProps = {
  message: string;
  onRetry?: () => void;
};

export default function ErrorBanner({ message, onRetry }: ErrorBannerProps) {
  return (
    <div className="careloop-error" role="alert">
      <span className="careloop-error__msg">{message}</span>
      {onRetry && (
        <button
          type="button"
          className="careloop-error__retry"
          onClick={onRetry}
        >
          Retry
        </button>
      )}
    </div>
  );
}
