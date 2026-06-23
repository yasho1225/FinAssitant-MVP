interface Props {
  items: { label: string; value?: string; highlight?: boolean }[];
}

export function MarketStrip({ items }: Props) {
  const visible = items.filter((i) => i.value);
  if (visible.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-px bg-ink-700/30 rounded-xl overflow-hidden">
      {visible.map((item) => (
        <div
          key={item.label}
          className={`flex-1 min-w-[120px] px-4 py-3 bg-ink-850/90 ${
            item.highlight ? "bg-accent-teal/5" : ""
          }`}
        >
          <p className="text-[10px] uppercase tracking-widest text-ink-500 mb-0.5">{item.label}</p>
          <p
            className={`font-mono text-sm font-medium tabular-nums ${
              item.highlight ? "text-accent-teal" : "text-ink-200"
            }`}
          >
            {item.value}
          </p>
        </div>
      ))}
    </div>
  );
}
