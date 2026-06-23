interface Props {
  variant?: "banner" | "inline" | "compact";
}

export function Disclaimer({ variant = "banner" }: Props) {
  if (variant === "compact") {
    return (
      <p className="text-[10px] text-ink-500 leading-relaxed">
        Not financial advice. Invest at your own risk. Past performance does not guarantee future results.
      </p>
    );
  }

  if (variant === "inline") {
    return (
      <div className="flex gap-3 rounded-xl border border-signal-hold/25 bg-signal-hold/5 px-4 py-3">
        <span className="text-signal-hold shrink-0 mt-0.5" aria-hidden>
          ⚠
        </span>
        <p className="text-xs text-ink-400 leading-relaxed">
          <span className="font-semibold text-signal-hold">Disclaimer:</span> This tool generates
          research-style summaries for educational purposes only. It is{" "}
          <span className="text-ink-300">not investment advice</span>. Always do your own due
          diligence. <span className="text-ink-300">Invest at your own risk.</span>
        </p>
      </div>
    );
  }

  return (
    <div
      role="note"
      aria-label="Investment risk disclaimer"
      className="rounded-xl border border-signal-hold/30 bg-gradient-to-r from-signal-hold/10 to-transparent px-4 py-3 text-center"
    >
      <p className="text-xs text-ink-400 leading-relaxed">
        <span className="font-semibold uppercase tracking-wider text-signal-hold mr-1">
          Risk warning
        </span>
        — Not financial advice. For research &amp; education only. Invest at your own risk.
      </p>
    </div>
  );
}
