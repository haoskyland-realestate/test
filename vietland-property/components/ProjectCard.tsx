import Link from "next/link";
import { Building2, MapPin, BedDouble, Ruler, ShieldCheck } from "lucide-react";
import { Project, formatUsd, formatVnd } from "../data/projects";

const gradients = [
  "linear-gradient(135deg,#A6231D,#711712)",
  "linear-gradient(135deg,#C9A15A,#8F6C33)",
  "linear-gradient(135deg,#4C7C6D,#2F5D50)",
  "linear-gradient(135deg,#1C2740,#10182B)",
  "linear-gradient(135deg,#C43A2E,#C9A15A)",
  "linear-gradient(135deg,#4C7C6D,#10182B)",
];

export default function ProjectCard({ project }: { project: Project }) {
  return (
    <article className="group flex flex-col overflow-hidden rounded-2xl border border-ink/8 bg-white shadow-card transition hover:-translate-y-0.5 hover:shadow-pop">
      <div
        className="relative flex h-44 items-end justify-between p-4"
        style={{ backgroundImage: gradients[project.accent % gradients.length] }}
      >
        <div className="flex gap-2">
          {project.badge && (
            <span className="rounded-full bg-white px-2.5 py-1 text-[10.5px] font-semibold uppercase tracking-wide text-ink">
              {project.badge}
            </span>
          )}
          <span className="flex items-center gap-1 rounded-full bg-ink/40 px-2.5 py-1 text-[10.5px] font-semibold text-white backdrop-blur">
            <ShieldCheck size={12} /> Verified foreign ownership
          </span>
        </div>
        <Building2 className="absolute right-4 top-4 text-white/25" size={42} strokeWidth={1.25} />
      </div>

      <div className="flex flex-1 flex-col p-5">
        <div className="flex items-center justify-between text-[12px] text-ink/45">
          <span className="flex items-center gap-1">
            <MapPin size={12} /> {project.district}
          </span>
          <span className="font-mono text-[10.5px] text-jade">Advisor-verified · {project.verifiedDate}</span>
        </div>

        <h3 className="mt-2 font-display text-[1.2rem] font-semibold text-ink">{project.name}</h3>
        <p className="mt-1.5 line-clamp-2 text-[13.5px] leading-relaxed text-ink/55">{project.description}</p>

        <span className="mt-3 inline-block w-fit rounded-md bg-gold/10 px-2.5 py-1 font-mono text-[10.5px] font-medium text-gold-dark">
          {project.tag}
        </span>

        <div className="mt-3 flex items-center gap-4 text-[12.5px] text-ink/55">
          <span className="flex items-center gap-1">
            <BedDouble size={13} /> {project.beds}
          </span>
          <span className="flex items-center gap-1">
            <Ruler size={13} /> {project.area}
          </span>
        </div>

        <div className="mt-4 flex items-end justify-between border-t border-ink/8 pt-4">
          <div>
            <p className="text-[13.5px] font-semibold text-lacquer">
              {formatVnd(project.priceFromVnd)} – {formatVnd(project.priceToVnd)}
            </p>
            <p className="text-[11.5px] text-ink/40">
              ≈ {formatUsd(project.priceFromUsd)} – {formatUsd(project.priceToUsd)}
            </p>
          </div>
          <Link
            href={`/projects/${project.slug}`}
            className="shrink-0 text-[13px] font-semibold text-ink underline decoration-gold decoration-2 underline-offset-4 transition group-hover:text-lacquer"
          >
            View details →
          </Link>
        </div>
      </div>
    </article>
  );
}
