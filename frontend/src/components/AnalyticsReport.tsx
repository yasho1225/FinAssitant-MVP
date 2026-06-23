import type { AnalyticsResponse } from "../types";
import { MetricsGrid } from "./MetricsGrid";
import { MarketStrip } from "./MarketStrip";
import { Disclaimer } from "./Disclaimer";

interface Props {
  data: AnalyticsResponse;
}

export function AnalyticsReport({ data }: Props) {
  const market = data.market || {};
  const buffett = data.buffett_signals;

  const marketItems = [
    { label: "Price", value: market.price?.display, highlight: true },
    { label: "Sector", value: market.sector },
    { label: "Industry", value: market.industry },
    { label: "P/E", value: market.pe?.display },
    { label: "EV/EBITDA", value: market.ev_ebitda?.display },
    { label: "1Y Return", value: market.return_1y?.display },
    { label: "5Y Return", value: market.return_5y?.display },
  ];

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl mx-auto">
      <Disclaimer variant="inline" />
      <header className="glass-card p-6 md:p-8 shadow-glow relative overflow-hidden">
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-accent-gold/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/4 pointer-events-none" />
        <div className="relative">
          <span className="inline-block px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-widest bg-accent-gold/10 text-accent-gold border border-accent-gold/20 mb-3">
            Layer B — Deterministic
          </span>
          <h2 className="font-display text-3xl md:text-4xl text-ink-100 mb-1">
            {market.company_name || data.ticker}
          </h2>
          <p className="font-mono text-accent-gold font-semibold">{data.ticker}</p>

          {buffett && (
            <div className="mt-4 inline-flex items-center gap-3 px-4 py-2 rounded-xl bg-ink-850 border border-ink-700/50">
              <div className="flex gap-1">
                {Array.from({ length: buffett.signals_total }).map((_, i) => (
                  <span
                    key={i}
                    className={`w-2 h-2 rounded-full ${
                      i < buffett.signals_met ? "bg-accent-teal" : "bg-ink-700"
                    }`}
                  />
                ))}
              </div>
              <span className="text-sm text-ink-300">
                <span className="font-mono text-accent-teal">{buffett.signals_met}</span>
                <span className="text-ink-500">/{buffett.signals_total}</span> Buffett signals
              </span>
              <span className="text-[10px] text-ink-600 uppercase tracking-wider">narrative only</span>
            </div>
          )}
        </div>
      </header>

      <MarketStrip items={marketItems} />

      <div className="glass-card p-6">
        <p className="text-[10px] uppercase tracking-widest text-ink-500 mb-4">Computed Metrics</p>
        <MetricsGrid metrics={data.key_metrics_flat} />
      </div>

      <p className="text-center text-xs text-ink-600 pb-4">
        All values computed in the analytics engine — reproducible and source-linked.
      </p>
    </div>
  );
}
