import { useEffect, useState } from "react";

const STEPS = [
  "Fetching price history",
  "Loading fundamentals",
  "Pulling SEC filings",
  "Computing analytics",
  "Synthesizing memo",
];

interface Props {
  ticker?: string;
}

export function LoadingState({ ticker }: Props) {
  const [step, setStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStep((s) => (s < STEPS.length - 1 ? s + 1 : s));
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  const progress = ((step + 1) / STEPS.length) * 100;

  return (
    <div className="flex flex-col items-center justify-center py-20 md:py-28 animate-fade-in max-w-lg mx-auto">
      <div className="glass-card p-8 w-full shadow-glow">
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-[10px] uppercase tracking-widest text-accent-teal mb-1">Analyzing</p>
            <h3 className="font-display text-2xl text-ink-100">{ticker || "—"}</h3>
          </div>
          <div className="w-12 h-12 rounded-full border-2 border-ink-700 border-t-accent-teal animate-spin" />
        </div>

        <div className="h-1.5 bg-ink-800 rounded-full overflow-hidden mb-6">
          <div
            className="h-full bg-gradient-to-r from-accent-teal/80 to-accent-teal rounded-full transition-all duration-700 ease-out shimmer-bar"
            style={{ width: `${progress}%` }}
          />
        </div>

        <ul className="space-y-3">
          {STEPS.map((label, i) => {
            const done = i < step;
            const active = i === step;
            return (
              <li
                key={label}
                className={`flex items-center gap-3 text-sm transition-all duration-300 ${
                  done ? "text-accent-teal" : active ? "text-ink-100" : "text-ink-600"
                }`}
              >
                <span
                  className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-mono shrink-0 border ${
                    done
                      ? "bg-accent-teal/20 border-accent-teal/50 text-accent-teal"
                      : active
                        ? "border-accent-teal/50 animate-step-pulse bg-ink-800"
                        : "border-ink-700 bg-ink-850"
                  }`}
                >
                  {done ? "✓" : i + 1}
                </span>
                {label}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
