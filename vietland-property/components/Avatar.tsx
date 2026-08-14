const gradients = [
  "linear-gradient(160deg,#A6231D,#711712)",
  "linear-gradient(160deg,#C9A15A,#8F6C33)",
  "linear-gradient(160deg,#4C7C6D,#2F5D50)",
  "linear-gradient(160deg,#1C2740,#10182B)",
];

export default function Avatar({
  initials,
  accent = 0,
  className = "",
}: {
  initials: string;
  accent?: number;
  className?: string;
}) {
  return (
    <div
      className={`flex items-center justify-center font-display text-2xl font-semibold text-white/90 ${className}`}
      style={{ backgroundImage: gradients[accent % gradients.length] }}
    >
      {initials}
    </div>
  );
}
