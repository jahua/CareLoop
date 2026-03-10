"use client";

type ErrorBannerProps = {
  message: string;
  onRetry?: () => void;
};

export default function ErrorBanner({ message, onRetry }: ErrorBannerProps) {
  return (
    <div className="big5loop-error" role="alert">
      <span className="big5loop-error__msg">{message}</span>
      {onRetry && (
        <button
          type="button"
          className="big5loop-error__retry"
          onClick={onRetry}
        >
          Retry
        </button>
      )}
    </div>
  );
}
