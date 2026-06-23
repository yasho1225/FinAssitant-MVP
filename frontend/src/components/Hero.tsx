import { IconChart, IconDocument, IconShield } from "./Icons";

const FEATURES = [
  {
    icon: IconChart,
    title: "Deterministic Analytics",
    desc: "Revenue CAGR, margins, ROIC, FCF — every number computed in Layer B before the LLM sees it.",
    accent: "text-accent-teal",
    border: "hover:border-accent-teal/30",
  },
  {
    icon: IconDocument,
    title: "Institutional Memos",
    desc: "10-section research reports with executive summary, valuation, risks, and source-cited appendix.",
    accent: "text-accent-gold",
    border: "hover:border-accent-gold/30",
  },
  {
    icon: IconShield,
    title: "Zero Hallucinated Numbers",
    desc: "The LLM interprets precomputed metrics only. No invented financials, no hidden quality scores.",
    accent: "text-accent-violet",
    border: "hover:border-accent-violet/30",
  },
];

export function Hero() {
  return (
    <div className="text-center mb-14">
      <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-ink-900/80 border border-ink-700/50 text-[11px] uppercase tracking-[0.15em] text-ink-400 mb-8">
        <span className="w-1.5 h-1.5 rounded-full bg-accent-teal animate-pulse" />
        Institutional-Quality Research
      </div>

      <h2 className="font-display text-4xl sm:text-5xl md:text-6xl text-ink-100 mb-5 leading-[1.1] tracking-tight">
        Equity research,
        <br />
        <span className="italic text-ink-400">grounded in data</span>
      </h2>

      <p className="text-ink-400 max-w-xl mx-auto text-base md:text-lg leading-relaxed mb-10">
        Enter any US ticker to generate a full investment memo powered by deterministic
        financial analytics and AI narrative synthesis.
      </p>

      <div className="grid sm:grid-cols-3 gap-4 max-w-3xl mx-auto text-left">
        {FEATURES.map(({ icon: Icon, title, desc, accent, border }) => (
          <div
            key={title}
            className={`glass-card-hover p-5 border ${border} group`}
          >
            <div className={`mb-3 ${accent}`}>
              <Icon className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-semibold text-ink-100 mb-1.5">{title}</h3>
            <p className="text-xs text-ink-500 leading-relaxed">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
