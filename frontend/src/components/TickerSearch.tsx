import { useState } from "react";
import { IconSearch } from "./Icons";

const POPULAR = [
  { ticker: "AAPL", name: "Apple" },
  { ticker: "MSFT", name: "Microsoft" },
  { ticker: "NVDA", name: "NVIDIA" },
  { ticker: "GOOGL", name: "Alphabet" },
  { ticker: "AMZN", name: "Amazon" },
  { ticker: "META", name: "Meta" },
];

interface Props {
  onSubmit: (ticker: string, mode: "memo" | "analytics") => void;
  loading: boolean;
  disabled?: boolean;
}

export function TickerSearch({ onSubmit, loading, disabled }: Props) {
  const [ticker, setTicker] = useState("");
  const [mode, setMode] = useState<"memo" | "analytics">("memo");
  const [focused, setFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const t = ticker.trim().toUpperCase();
    if (t) onSubmit(t, mode);
  };

  const pick = (t: string) => {
    setTicker(t);
    onSubmit(t, mode);
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <div
          className={`glass-card p-2 transition-all duration-300 ${
            focused ? "shadow-glow border-accent-teal/30" : ""
          }`}
        >
          <div className="flex flex-col sm:flex-row gap-2">
            <div className="flex-1 flex items-center gap-3 px-4 py-2">
              <IconSearch className={`w-5 h-5 shrink-0 transition-colors ${focused ? "text-accent-teal" : "text-ink-500"}`} />
              <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                onFocus={() => setFocused(true)}
                onBlur={() => setFocused(false)}
                placeholder="Ticker symbol — AAPL, MSFT, NVDA…"
                maxLength={10}
                disabled={loading || disabled}
                className="flex-1 bg-transparent text-xl font-mono text-ink-100 placeholder:text-ink-600 outline-none disabled:opacity-50"
                autoComplete="off"
                spellCheck={false}
              />
            </div>

            <div className="flex gap-2 p-1 sm:p-0">
              <div className="flex rounded-xl bg-ink-850 p-1 border border-ink-700/50">
                {(["memo", "analytics"] as const).map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => setMode(m)}
                    className={`px-4 py-2.5 text-xs font-semibold rounded-lg transition-all ${
                      mode === m
                        ? m === "memo"
                          ? "bg-accent-teal/15 text-accent-teal shadow-inner"
                          : "bg-accent-gold/15 text-accent-gold shadow-inner"
                        : "text-ink-500 hover:text-ink-300"
                    }`}
                  >
                    {m === "memo" ? "Full Memo" : "Analytics"}
                  </button>
                ))}
              </div>

              <button
                type="submit"
                disabled={!ticker.trim() || loading || disabled}
                className="btn-primary shrink-0"
              >
                {loading ? "Running…" : "Analyze →"}
              </button>
            </div>
          </div>
        </div>
      </form>

      <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-2">
        {POPULAR.map(({ ticker: t, name }) => (
          <button
            key={t}
            type="button"
            onClick={() => pick(t)}
            disabled={loading}
            className="group flex items-center justify-between px-4 py-3 rounded-xl bg-ink-900/50 border border-ink-700/40 hover:border-accent-teal/30 hover:bg-ink-800/50 transition-all disabled:opacity-40 text-left"
          >
            <span className="font-mono font-semibold text-ink-200 group-hover:text-accent-teal transition-colors">
              {t}
            </span>
            <span className="text-xs text-ink-500 truncate ml-2">{name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
