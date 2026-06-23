import type { ResearchResponse } from "../types";
import { RecommendationBadge } from "./RecommendationBadge";
import { MetricsGrid } from "./MetricsGrid";
import { MemoSection } from "./MemoSection";
import { ThesisPanel } from "./ThesisPanel";
import { BulletList } from "./BulletList";
import { MarketStrip } from "./MarketStrip";
import { SectionNav } from "./SectionNav";
import { PeerComparisonTable, cleanValuationText } from "./PeerComparisonTable";
import { Disclaimer } from "./Disclaimer";

interface Props {
  data: ResearchResponse;
  onPrint?: () => void;
}

type AnalyticsSnap = {
  market?: {
    company_name?: string;
    sector?: string;
    industry?: string;
    price?: { display: string };
    pe?: { display: string };
    ev_ebitda?: { display: string };
    return_1y?: { display: string };
    return_5y?: { display: string };
    volatility_1y?: { display: string };
  };
  buffett_signals?: { signals_met: number; signals_total: number };
  peer_comparison?: {
    peer_tickers?: string[];
    relative_valuation?: Record<string, { subject: number | null; peer_median: number | null; vs_peers: string }>;
  };
};

export function MemoReport({ data, onPrint }: Props) {
  const { memo, structured, generated_at, raw_sources, analytics_snapshot } = data;
  const snap = analytics_snapshot as AnalyticsSnap;
  const market = snap.market || {};
  const companyName = market.company_name || structured.ticker;

  const formattedDate = new Date(generated_at).toLocaleString("en-US", {
    dateStyle: "long",
    timeStyle: "short",
  });

  const marketItems = [
    { label: "Price", value: market.price?.display, highlight: true },
    { label: "Sector", value: market.sector },
    { label: "P/E", value: market.pe?.display },
    { label: "EV/EBITDA", value: market.ev_ebitda?.display },
    { label: "1Y Return", value: market.return_1y?.display },
    { label: "5Y Return", value: market.return_5y?.display },
  ];

  return (
    <div className="animate-fade-in">
      <div className="mb-5">
        <Disclaimer variant="inline" />
      </div>
      {/* Report header */}
      <header className="glass-card p-6 md:p-8 mb-6 shadow-glow relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-accent-teal/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none" />
        <div className="relative flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-3">
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-widest bg-accent-teal/10 text-accent-teal border border-accent-teal/20">
                Research Memo
              </span>
              {market.industry && (
                <span className="text-xs text-ink-500">{market.industry}</span>
              )}
            </div>
            <h2 className="font-display text-3xl md:text-4xl lg:text-5xl text-ink-100 mb-2 leading-tight">
              {companyName}
            </h2>
            <p className="font-mono text-ink-400 flex flex-wrap items-center gap-x-2 gap-y-1">
              <span className="text-accent-teal font-semibold">{structured.ticker}</span>
              <span className="text-ink-600">·</span>
              <span className="text-ink-500">{formattedDate}</span>
            </p>
          </div>
          <div className="flex flex-col sm:flex-row items-start gap-3">
            <RecommendationBadge
              recommendation={structured.recommendation}
              confidence={structured.confidence}
            />
            <button
              onClick={() => (onPrint ? onPrint() : window.print())}
              className="no-print px-4 py-2 text-xs font-medium text-ink-400 border border-ink-700 rounded-xl hover:text-ink-100 hover:border-ink-600 transition-colors"
            >
              Export PDF
            </button>
          </div>
        </div>

        <div className="relative mt-6">
          <MarketStrip items={marketItems} />
        </div>

        <div className="relative mt-6 pt-6 border-t border-ink-700/40">
          <p className="text-[10px] uppercase tracking-widest text-ink-500 mb-3">Key Metrics</p>
          <MetricsGrid metrics={structured.key_metrics} />
        </div>
      </header>

      <div className="grid lg:grid-cols-[220px_1fr] gap-6 items-start">
        <aside className="hidden lg:block">
          <SectionNav />
        </aside>

        <div className="space-y-5 min-w-0">
          <ThesisPanel bull={structured.thesis.bull} bear={structured.thesis.bear} />

          <MemoSection id="executive" title="Executive Summary" content={memo.executive_summary} index={0} />
          <MemoSection id="business" title="Business Overview" content={memo.business_overview} index={1} />
          <MemoSection id="financial" title="Financial Health" content={memo.financial_health} index={2} />
          <MemoSection id="valuation" title="Valuation" content={cleanValuationText(memo.valuation)} index={3}>
            <PeerComparisonTable data={snap.peer_comparison} />
          </MemoSection>
          <MemoSection id="catalysts" title="Catalysts" content={memo.catalysts} variant="catalyst" index={4} />
          <MemoSection id="risks" title="Risks" content={memo.risks} variant="risk" index={5} />
          <MemoSection id="bear" title="Bear Case" content={memo.bear_case} variant="risk" index={6} />
          <MemoSection
            id="mind-change"
            title="What Would Change My Mind"
            content={memo.what_would_change_my_mind}
            index={7}
          />
          <MemoSection id="appendix" title="Data Appendix" content={memo.data_appendix} index={8} />

          <div className="grid md:grid-cols-3 gap-4">
            <BulletList items={structured.catalysts} title="Key Catalysts" variant="catalyst" />
            <BulletList items={structured.risks} title="Key Risks" variant="risk" />
            <BulletList
              items={structured.mind_change_triggers}
              title="Mind Change Triggers"
              variant="trigger"
            />
          </div>

          <footer className="glass-card p-6">
            <h4 className="text-xs uppercase tracking-widest text-ink-400 font-semibold mb-4">
              Sources & Citations
            </h4>
            <ul className="space-y-2 mb-5">
              {memo.citations.map((cite, i) => (
                <li key={i} className="flex gap-3 text-sm text-ink-400">
                  <span className="font-mono text-accent-teal/60 shrink-0">[{i + 1}]</span>
                  <span>{cite}</span>
                </li>
              ))}
            </ul>
            <div className="flex flex-wrap gap-2 pt-4 border-t border-ink-700/40">
              {Object.entries(raw_sources).map(([key, source]) => (
                <span
                  key={key}
                  className="text-[10px] uppercase tracking-wider px-2.5 py-1 rounded-lg bg-ink-850 border border-ink-700/50 text-ink-500"
                >
                  {key}: <span className="text-ink-400">{source}</span>
                </span>
              ))}
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
}
