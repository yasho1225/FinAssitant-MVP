import type { KeyMetrics } from "../types";

const METRIC_LABELS: Record<keyof KeyMetrics, string> = {
  revenue_cagr: "Revenue CAGR",
  eps_cagr: "EPS CAGR",
  net_margin: "Net Margin",
  roic: "ROIC",
  roe: "ROE",
  debt_equity: "Debt / Equity",
};

interface Props {
  metrics: KeyMetrics;
}

export function MetricsGrid({ metrics }: Props) {
  const entries = Object.entries(metrics) as [keyof KeyMetrics, string][];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      {entries.map(([key, value], i) => (
        <div
          key={key}
          className="relative group rounded-xl bg-ink-850/80 border border-ink-700/40 p-4 hover:border-accent-teal/25 transition-all duration-300 overflow-hidden"
          style={{ animationDelay: `${i * 60}ms` }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-accent-teal/0 to-accent-teal/5 opacity-0 group-hover:opacity-100 transition-opacity" />
          <p className="relative text-[10px] uppercase tracking-wider text-ink-500 mb-2 group-hover:text-accent-teal/80 transition-colors">
            {METRIC_LABELS[key] || key}
          </p>
          <p className="relative metric-value text-base md:text-lg">{value}</p>
        </div>
      ))}
    </div>
  );
}
