const SECTION_NUMBERS: Record<string, number> = {
  "Executive Summary": 1,
  "Business Overview": 2,
  "Financial Health": 3,
  Valuation: 4,
  Catalysts: 5,
  Risks: 6,
  "Bear Case": 7,
  "What Would Change My Mind": 8,
  "Data Appendix": 9,
};

interface Props {
  id?: string;
  title: string;
  content: string;
  variant?: "default" | "risk" | "catalyst";
  index?: number;
  children?: React.ReactNode;
}

const VARIANT_ACCENT = {
  default: "border-accent-teal/50 text-accent-teal",
  risk: "border-signal-sell/50 text-signal-sell",
  catalyst: "border-accent-gold/50 text-accent-gold",
};

export function MemoSection({ id, title, content, variant = "default", index, children }: Props) {
  const num = SECTION_NUMBERS[title];

  return (
    <article
      id={id}
      className="glass-card p-6 md:p-8 animate-slide-up scroll-mt-28"
      style={{ animationDelay: index !== undefined ? `${index * 40}ms` : undefined }}
    >
      <header className="flex items-start gap-4 mb-5 pb-5 border-b border-ink-700/40">
        {num && (
          <span
            className={`flex items-center justify-center w-9 h-9 rounded-lg border font-mono text-sm font-semibold shrink-0 ${VARIANT_ACCENT[variant]}`}
          >
            {num}
          </span>
        )}
        <h3 className="section-title pt-0.5">{title}</h3>
      </header>
      <div className="prose-memo pl-0 md:pl-[52px]">{content}</div>
      {children && <div className="pl-0 md:pl-[52px]">{children}</div>}
    </article>
  );
}
