interface Props {
  bull: string[];
  bear: string[];
}

export function ThesisPanel({ bull, bear }: Props) {
  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="glass-card overflow-hidden">
        <div className="h-1 bg-gradient-to-r from-signal-buy/80 to-signal-buy/20" />
        <div className="p-6">
          <h4 className="text-xs uppercase tracking-[0.15em] text-signal-buy font-bold mb-4 flex items-center gap-2">
            <span className="w-6 h-6 rounded-md bg-signal-buy/15 flex items-center justify-center text-sm">↑</span>
            Bull Thesis
          </h4>
          <ul className="space-y-3">
            {bull.map((point, i) => (
              <li key={i} className="flex gap-3 text-sm text-ink-300 leading-relaxed">
                <span className="font-mono text-[10px] text-signal-buy/70 mt-1 shrink-0">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span>{point}</span>
              </li>
            ))}
            {bull.length === 0 && (
              <li className="text-ink-600 text-sm italic">No bull points generated</li>
            )}
          </ul>
        </div>
      </div>

      <div className="glass-card overflow-hidden">
        <div className="h-1 bg-gradient-to-r from-signal-sell/80 to-signal-sell/20" />
        <div className="p-6">
          <h4 className="text-xs uppercase tracking-[0.15em] text-signal-sell font-bold mb-4 flex items-center gap-2">
            <span className="w-6 h-6 rounded-md bg-signal-sell/15 flex items-center justify-center text-sm">↓</span>
            Bear Thesis
          </h4>
          <ul className="space-y-3">
            {bear.map((point, i) => (
              <li key={i} className="flex gap-3 text-sm text-ink-300 leading-relaxed">
                <span className="font-mono text-[10px] text-signal-sell/70 mt-1 shrink-0">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span>{point}</span>
              </li>
            ))}
            {bear.length === 0 && (
              <li className="text-ink-600 text-sm italic">No bear points generated</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}
