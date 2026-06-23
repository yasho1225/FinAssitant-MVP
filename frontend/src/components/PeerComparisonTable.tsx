interface RelativeMetric {
  subject: number | null;
  peer_median: number | null;
  vs_peers: string;
}

interface PeerComparison {
  peer_tickers?: string[];
  relative_valuation?: Record<string, RelativeMetric>;
  source?: string;
}

const LABELS: Record<string, string> = {
  pe: "P/E",
  ev_ebitda: "EV / EBITDA",
  ps: "P/S",
  net_margin: "Net Margin",
  roe: "ROE",
  roic: "ROIC",
};

const PERCENT_KEYS = new Set(["net_margin", "roe", "roic"]);

const VS_LABELS: Record<string, { text: string; className: string }> = {
  above_peers: { text: "Above peers", className: "text-signal-sell bg-signal-sell/10 border-signal-sell/20" },
  below_peers: { text: "Below peers", className: "text-signal-buy bg-signal-buy/10 border-signal-buy/20" },
  in_line: { text: "In line", className: "text-signal-hold bg-signal-hold/10 border-signal-hold/20" },
  insufficient_data: { text: "N/A", className: "text-ink-500 bg-ink-800 border-ink-700" },
};

function formatValue(key: string, value: number | null): string {
  if (value === null || value === undefined) return "—";
  if (PERCENT_KEYS.has(key)) return `${(value * 100).toFixed(1)}%`;
  return `${value.toFixed(2)}x`;
}

interface Props {
  data: PeerComparison | undefined;
}

export function PeerComparisonTable({ data }: Props) {
  const relative = data?.relative_valuation;
  if (!relative || Object.keys(relative).length === 0) return null;

  const peers = data?.peer_tickers?.join(", ");

  return (
    <div className="mt-5 space-y-3">
      {peers && (
        <p className="text-xs text-ink-500">
          vs peer median
          <span className="font-mono text-ink-400 ml-1">({peers})</span>
        </p>
      )}
      <div className="overflow-x-auto rounded-xl border border-ink-700/50">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-ink-850/80 text-left">
              <th className="px-4 py-3 text-[10px] uppercase tracking-widest text-ink-500 font-semibold">
                Metric
              </th>
              <th className="px-4 py-3 text-[10px] uppercase tracking-widest text-ink-500 font-semibold">
                Company
              </th>
              <th className="px-4 py-3 text-[10px] uppercase tracking-widest text-ink-500 font-semibold">
                Peer Median
              </th>
              <th className="px-4 py-3 text-[10px] uppercase tracking-widest text-ink-500 font-semibold">
                vs Peers
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-ink-700/40">
            {Object.entries(relative).map(([key, row]) => {
              const vs = VS_LABELS[row.vs_peers] || VS_LABELS.insufficient_data;
              return (
                <tr key={key} className="hover:bg-ink-850/40 transition-colors">
                  <td className="px-4 py-3 text-ink-300 font-medium">{LABELS[key] || key}</td>
                  <td className="px-4 py-3 font-mono text-ink-100 tabular-nums">
                    {formatValue(key, row.subject)}
                  </td>
                  <td className="px-4 py-3 font-mono text-ink-400 tabular-nums">
                    {formatValue(key, row.peer_median)}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-block text-[11px] font-medium px-2 py-0.5 rounded-md border ${vs.className}`}
                    >
                      {vs.text}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/** Strip raw JSON peer dumps from legacy memo text */
export function cleanValuationText(text: string): string {
  const marker = "Peer comparison:";
  const idx = text.indexOf(marker);
  if (idx === -1) return text;
  return text.slice(0, idx).trim();
}
