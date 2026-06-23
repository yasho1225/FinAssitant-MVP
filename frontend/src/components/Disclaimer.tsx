interface Props {
  variant?: "banner" | "inline" | "compact";
}

function IconAlert({ className = "w-4 h-4" }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
      />
    </svg>
  );
}

export function Disclaimer({ variant = "banner" }: Props) {
  if (variant === "compact") {
    return (
      <p className="text-[11px] text-ink-600 leading-relaxed">
        <span className="text-ink-500">© Research tool only.</span>{" "}
        Not financial advice · Invest at your own risk
      </p>
    );
  }

  if (variant === "inline") {
    return (
      <div
        role="note"
        aria-label="Investment risk disclaimer"
        className="relative overflow-hidden rounded-2xl border border-ink-700/50 bg-ink-900/50 backdrop-blur-sm"
      >
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-accent-gold/60 via-accent-gold/30 to-transparent" />
        <div className="flex items-start gap-4 px-5 py-4 pl-6">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-ink-800/80 border border-ink-700/50 text-accent-gold/90">
            <IconAlert />
          </div>
          <div className="min-w-0 pt-0.5">
            <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-ink-400 mb-1">
              Research disclaimer
            </p>
            <p className="text-sm text-ink-400 leading-relaxed">
              Educational summaries only — not investment advice. Do your own due diligence.
              <span className="text-ink-300"> Invest at your own risk.</span>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      role="note"
      aria-label="Investment risk disclaimer"
      className="mx-auto max-w-2xl"
    >
      <div className="flex items-center justify-center gap-3 rounded-full border border-ink-700/40 bg-ink-900/40 backdrop-blur-sm px-5 py-2.5">
        <div className="flex h-6 w-6 items-center justify-center rounded-full bg-ink-800 text-accent-gold/80">
          <IconAlert className="w-3.5 h-3.5" />
        </div>
        <p className="text-xs text-ink-500">
          <span className="text-ink-400">Not financial advice</span>
          <span className="mx-2 text-ink-700">·</span>
          Research &amp; education only
          <span className="mx-2 text-ink-700">·</span>
          <span className="text-ink-400">Invest at your own risk</span>
        </p>
      </div>
    </div>
  );
}
