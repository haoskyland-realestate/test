import { Building2 } from "lucide-react";
import VietRibbon from "./VietRibbon";

interface CityNode {
  city: string;
  count: number;
  x: number; // 0-220
  y: number; // 0-640
  side: "left" | "right";
  highlight?: boolean;
}

const cities: CityNode[] = [
  { city: "Ha Noi", count: 5, x: 108, y: 46, side: "right" },
  { city: "Da Nang", count: 6, x: 132, y: 250, side: "right" },
  { city: "Binh Duong", count: 4, x: 58, y: 452, side: "left" },
  { city: "Ho Chi Minh City", count: 9, x: 112, y: 566, side: "right", highlight: true },
];

export default function CityNetworkMap() {
  return (
    <div className="relative mx-auto aspect-[220/640] w-full max-w-[280px] sm:max-w-[320px]">
      <VietRibbon stroke="#A6231D" glow="#C9A15A" className="h-full w-full" />

      {cities.map((node) => {
        const left = `${(node.x / 220) * 100}%`;
        const top = `${(node.y / 640) * 100}%`;
        return (
          <span key={node.city}>
            <span
              className="absolute -translate-x-1/2 -translate-y-1/2"
              style={{ left, top }}
            >
              <span className="relative flex h-3 w-3">
                {node.highlight && (
                  <span className="absolute inline-flex h-full w-full animate-pulseRing rounded-full bg-lacquer" />
                )}
                <span
                  className={`relative inline-flex h-3 w-3 rounded-full border-2 border-paper ${
                    node.highlight ? "bg-lacquer" : "bg-gold"
                  }`}
                />
              </span>
            </span>

            <div
              className={`absolute z-10 flex w-[132px] items-center gap-2 rounded-xl border border-ink/5 bg-white/95 px-2.5 py-2 shadow-card sm:w-[150px] ${
                node.side === "right" ? "" : "-translate-x-full"
              }`}
              style={{
                left: node.side === "right" ? `calc(${left} + 10px)` : `calc(${left} - 10px)`,
                top: `calc(${top} - 18px)`,
              }}
            >
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-lacquer/10 text-lacquer">
                <Building2 size={14} strokeWidth={2.25} />
              </span>
              <span className="leading-tight">
                <span className="block text-[12px] font-semibold text-ink">{node.city}</span>
                <span className="block text-[10.5px] text-ink/55">{node.count} active projects</span>
              </span>
            </div>
          </span>
        );
      })}
    </div>
  );
}
