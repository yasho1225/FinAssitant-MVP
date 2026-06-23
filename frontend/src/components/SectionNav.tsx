const SECTIONS = [
  { id: "executive", label: "Executive Summary" },
  { id: "business", label: "Business Overview" },
  { id: "financial", label: "Financial Health" },
  { id: "valuation", label: "Valuation" },
  { id: "catalysts", label: "Catalysts" },
  { id: "risks", label: "Risks" },
  { id: "bear", label: "Bear Case" },
  { id: "mind-change", label: "Mind Change" },
  { id: "appendix", label: "Data Appendix" },
];

interface Props {
  activeId?: string;
}

export function SectionNav({ activeId }: Props) {
  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <nav className="no-print glass-card p-4 sticky top-24">
      <p className="text-[10px] uppercase tracking-widest text-ink-500 font-semibold mb-3 px-3">
        Contents
      </p>
      <ul className="space-y-0.5">
        {SECTIONS.map((s) => (
          <li key={s.id}>
            <button
              onClick={() => scrollTo(s.id)}
              className={activeId === s.id ? "nav-link-active" : "nav-link"}
            >
              {s.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export { SECTIONS };
