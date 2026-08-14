interface VietRibbonProps {
  stroke: string;
  glow?: string;
  className?: string;
}

/**
 * A stylised, hand-drawn "dragon spine" ribbon running north to south.
 * Not a literal map — an abstract throughline used in the hero and in the
 * office-network sections to visually connect every region of the country.
 */
export default function VietRibbon({ stroke, glow, className }: VietRibbonProps) {
  const d =
    "M110,18 C38,86 192,146 118,228 C54,298 186,356 100,438 C40,488 150,528 104,606";

  return (
    <svg
      viewBox="0 0 220 640"
      className={className}
      preserveAspectRatio="xMidYMin meet"
      aria-hidden="true"
    >
      {glow && (
        <path d={d} fill="none" stroke={glow} strokeWidth={16} strokeLinecap="round" opacity={0.18} />
      )}
      <path d={d} fill="none" stroke={stroke} strokeWidth={3.5} strokeLinecap="round" opacity={0.9} />
      <path
        d={d}
        fill="none"
        stroke={stroke}
        strokeWidth={1}
        strokeDasharray="1 9"
        strokeLinecap="round"
        opacity={0.6}
      />
    </svg>
  );
}
