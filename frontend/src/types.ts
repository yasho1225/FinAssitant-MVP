export type Recommendation = "BUY" | "HOLD" | "SELL";

export interface KeyMetrics {
  revenue_cagr: string;
  eps_cagr: string;
  net_margin: string;
  roic: string;
  roe: string;
  debt_equity: string;
}

export interface InvestmentMemo {
  executive_summary: string;
  business_overview: string;
  financial_health: string;
  valuation: string;
  catalysts: string;
  risks: string;
  bear_case: string;
  what_would_change_my_mind: string;
  data_appendix: string;
  citations: string[];
}

export interface MemoStructuredOutput {
  ticker: string;
  recommendation: Recommendation;
  confidence: number;
  key_metrics: KeyMetrics;
  thesis: { bull: string[]; bear: string[] };
  risks: string[];
  catalysts: string[];
  mind_change_triggers: string[];
}

export interface ResearchResponse {
  ticker: string;
  generated_at: string;
  memo: InvestmentMemo;
  structured: MemoStructuredOutput;
  analytics_snapshot: Record<string, unknown>;
  raw_sources: Record<string, string>;
}

export interface AnalyticsResponse {
  ticker: string;
  computed_at: string;
  key_metrics_flat: KeyMetrics;
  market?: {
    company_name?: string;
    sector?: string;
    industry?: string;
    price?: { display: string };
    pe?: { display: string };
    ev_ebitda?: { display: string };
    return_1y?: { display: string };
    return_5y?: { display: string };
  };
  buffett_signals?: {
    signals_met: number;
    signals_total: number;
  };
}
