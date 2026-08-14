const facts = [
  "Foreign ownership quota per project",
  "50-year leasehold, renewable",
  "Freely resold or leased",
  "Advisory in English · 中文 · 한국어",
  "Housing Law 2023",
  "SPA signed directly with the developer",
  "Resale to a Vietnamese national → freehold",
];

export default function MarqueeTicker() {
  const items = [...facts, ...facts];

  return (
    <div className="overflow-hidden border-b border-ink/8 bg-ink text-white">
      <div className="marquee-track py-2.5">
        {items.map((fact, i) => (
          <span key={i} className="flex shrink-0 items-center px-6 text-[12.5px] font-medium tracking-wide">
            <span className="mr-6 h-1.5 w-1.5 shrink-0 rounded-full bg-gold" />
            {fact}
          </span>
        ))}
      </div>
    </div>
  );
}
