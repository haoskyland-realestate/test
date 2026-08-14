import { Star, Gem, CircleDot } from "lucide-react";
import VietRibbon from "./VietRibbon";
import { offices, officeSummary, officesByRegion, Office } from "../data/offices";

const regionColor: Record<Office["region"], string> = {
  North: "#E7CE93",
  Central: "#7FA396",
  South: "#E08074",
};

const regionLabel: Record<Office["region"], string> = {
  North: "NORTH",
  Central: "CENTRAL",
  South: "SOUTH",
};

const mapDots: { region: Office["region"]; kind: Office["kind"]; label: string; x: number; y: number }[] = [
  { region: "North", kind: "headquarters", label: "Ha Noi", x: 108, y: 50 },
  { region: "Central", kind: "gallery", label: "Da Nang", x: 132, y: 250 },
  { region: "South", kind: "headquarters", label: "Thu Duc", x: 112, y: 566 },
  { region: "South", kind: "office", label: "Phu Quoc", x: 100, y: 606 },
];

function KindIcon({ kind, color }: { kind: Office["kind"]; color: string }) {
  if (kind === "headquarters") return <Star size={12} color={color} fill={color} />;
  if (kind === "gallery") return <Gem size={11} color={color} />;
  return <CircleDot size={9} color={color} />;
}

export default function OfficeNetworkMap({ variant = "full" }: { variant?: "full" | "compact" }) {
  const regions: Office["region"][] = ["North", "Central", "South"];

  return (
    <div className={`grid gap-8 ${variant === "full" ? "md:grid-cols-[280px_1fr]" : "sm:grid-cols-[200px_1fr] items-center"}`}>
      <div className="relative mx-auto aspect-[220/640] w-full max-w-[180px]">
        <VietRibbon stroke="#C9A15A" className="h-full w-full" />
        {mapDots.map((d) => {
          const left = `${(d.x / 220) * 100}%`;
          const top = `${(d.y / 640) * 100}%`;
          const color = regionColor[d.region];
          return (
            <div
              key={d.label}
              className="absolute flex -translate-x-1/2 -translate-y-1/2 items-center gap-1.5"
              style={{ left, top }}
            >
              <KindIcon kind={d.kind} color={color} />
              <span className="whitespace-nowrap font-mono text-[9px] uppercase tracking-wide" style={{ color }}>
                {d.label}
              </span>
            </div>
          );
        })}
      </div>

      {variant === "compact" ? (
        <div>
          <p className="eyebrow text-gold-light/80">Our office network</p>
          <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2">
            {regions.map((r) => (
              <span key={r} className="font-mono text-xs text-white/70">
                <span style={{ color: regionColor[r] }}>{regionLabel[r]}</span> · {officesByRegion(r).length}
              </span>
            ))}
          </div>
          <p className="mt-3 text-xs text-white/45">
            {officeSummary.total} offices · {officeSummary.provinces} provinces · {officeSummary.regions} regions
          </p>
        </div>
      ) : (
        <div className="grid gap-8 sm:grid-cols-3">
          {regions.map((region) => (
            <div key={region}>
              <p className="eyebrow" style={{ color: regionColor[region] }}>
                {regionLabel[region]} · {officesByRegion(region).length}
              </p>
              <ul className="mt-3 space-y-2">
                {officesByRegion(region).map((o) => (
                  <li key={o.name} className="flex items-center gap-2 text-sm text-white/70">
                    <KindIcon kind={o.kind} color={regionColor[region]} />
                    <span className={o.kind === "headquarters" ? "font-semibold text-white" : ""}>{o.name}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
          <p className="sm:col-span-3 mt-2 font-mono text-xs text-white/45">
            {officeSummary.total} offices · {officeSummary.provinces} provinces · {officeSummary.regions} regions
          </p>
        </div>
      )}
    </div>
  );
}
