import type { Recommendation } from "../types";

interface Props {
  confidence: number;
  recommendation: Recommendation;
  size?: number;
}

const COLORS: Record<Recommendation, string> = {
  BUY: "#34d399",
  HOLD: "#fbbf24",
  SELL: "#f87171",
};

export function ConfidenceGauge({ confidence, recommendation, size = 88 }: Props) {
  const stroke = 6;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - confidence * circumference;
  const color = COLORS[recommendation];

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={stroke}
          className="text-ink-800"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="transition-all duration-1000 ease-out"
          style={{ filter: `drop-shadow(0 0 6px ${color}40)` }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-lg font-semibold text-ink-100">
          {(confidence * 100).toFixed(0)}%
        </span>
        <span className="text-[9px] uppercase tracking-widest text-ink-500">conf.</span>
      </div>
    </div>
  );
}
