import type { Recommendation } from "../types";
import { ConfidenceGauge } from "./ConfidenceGauge";

const STYLES: Record<Recommendation, { bg: string; text: string; border: string; glow: string }> = {
  BUY: {
    bg: "from-signal-buy/20 to-signal-buy/5",
    text: "text-signal-buy",
    border: "border-signal-buy/30",
    glow: "shadow-[0_0_32px_-4px_rgba(52,211,153,0.25)]",
  },
  HOLD: {
    bg: "from-signal-hold/20 to-signal-hold/5",
    text: "text-signal-hold",
    border: "border-signal-hold/30",
    glow: "shadow-[0_0_32px_-4px_rgba(251,191,36,0.2)]",
  },
  SELL: {
    bg: "from-signal-sell/20 to-signal-sell/5",
    text: "text-signal-sell",
    border: "border-signal-sell/30",
    glow: "shadow-[0_0_32px_-4px_rgba(248,113,113,0.25)]",
  },
};

interface Props {
  recommendation: Recommendation;
  confidence: number;
}

export function RecommendationBadge({ recommendation, confidence }: Props) {
  const s = STYLES[recommendation];

  return (
    <div
      className={`flex items-center gap-5 rounded-2xl border bg-gradient-to-br px-6 py-4 ${s.bg} ${s.border} ${s.glow}`}
    >
      <ConfidenceGauge confidence={confidence} recommendation={recommendation} />
      <div>
        <p className="text-[10px] uppercase tracking-[0.2em] text-ink-400 mb-1">Recommendation</p>
        <p className={`font-mono text-3xl font-bold tracking-wider ${s.text}`}>
          {recommendation}
        </p>
      </div>
    </div>
  );
}
