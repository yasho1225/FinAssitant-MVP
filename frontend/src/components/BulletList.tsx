interface Props {
  items: string[];
  title: string;
  variant?: "risk" | "catalyst" | "trigger";
}

const STYLES = {
  risk: { dot: "bg-signal-sell", label: "text-signal-sell" },
  catalyst: { dot: "bg-accent-gold", label: "text-accent-gold" },
  trigger: { dot: "bg-accent-teal", label: "text-accent-teal" },
};

export function BulletList({ items, title, variant = "risk" }: Props) {
  const s = STYLES[variant];

  return (
    <div className="glass-card p-5 h-full">
      <h4 className={`text-xs uppercase tracking-widest font-bold mb-4 flex items-center gap-2 ${s.label}`}>
        <span className={`w-1.5 h-1.5 rounded-full ${s.dot}`} />
        {title}
      </h4>
      <ul className="space-y-2.5">
        {items.map((item, i) => (
          <li key={i} className="flex gap-2.5 text-sm text-ink-300 leading-relaxed">
            <span className="font-mono text-[10px] text-ink-600 mt-0.5 w-4 shrink-0">
              {i + 1}.
            </span>
            <span>{item}</span>
          </li>
        ))}
        {items.length === 0 && (
          <li className="text-ink-600 text-sm italic">None listed</li>
        )}
      </ul>
    </div>
  );
}
