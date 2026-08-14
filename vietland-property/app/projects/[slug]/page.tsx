import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, MapPin, ShieldCheck, BedDouble, Ruler, CalendarClock, Building2 } from "lucide-react";
import { projects, formatUsd, formatVnd } from "../../../data/projects";
import CtaBanner from "../../../components/CtaBanner";

const gradients = [
  "linear-gradient(135deg,#A6231D,#711712)",
  "linear-gradient(135deg,#C9A15A,#8F6C33)",
  "linear-gradient(135deg,#4C7C6D,#2F5D50)",
  "linear-gradient(135deg,#1C2740,#10182B)",
  "linear-gradient(135deg,#C43A2E,#C9A15A)",
  "linear-gradient(135deg,#4C7C6D,#10182B)",
];

export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }) {
  const project = projects.find((p) => p.slug === params.slug);
  return { title: project ? `${project.name} — Vietland` : "Project — Vietland" };
}

export default function ProjectDetailPage({ params }: { params: { slug: string } }) {
  const project = projects.find((p) => p.slug === params.slug);
  if (!project) notFound();

  const facts = [
    { label: "Type", value: project.type },
    { label: "Bedrooms", value: project.beds },
    { label: "Area", value: project.area },
    { label: "Developer", value: project.developer },
    { label: "Handover", value: project.handover },
    { label: "Ownership", value: "50-year leasehold, renewable" },
  ];

  return (
    <>
      <section className="pb-16 pt-8 md:pb-24">
        <div className="container-page">
          <Link href="/projects" className="flex w-fit items-center gap-1.5 text-[13px] font-medium text-ink/55 hover:text-lacquer">
            <ArrowLeft size={14} /> Back to projects
          </Link>

          <div
            className="relative mt-5 flex h-64 items-end rounded-2xl p-6 sm:h-80"
            style={{ backgroundImage: gradients[project.accent % gradients.length] }}
          >
            <Building2 className="absolute right-6 top-6 text-white/20" size={64} strokeWidth={1.1} />
            <div className="flex flex-wrap gap-2">
              {project.badge && (
                <span className="rounded-full bg-white px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-ink">
                  {project.badge}
                </span>
              )}
              <span className="flex items-center gap-1 rounded-full bg-ink/40 px-3 py-1 text-[11px] font-semibold text-white backdrop-blur">
                <ShieldCheck size={12} /> Verified foreign ownership
              </span>
            </div>
          </div>

          <div className="mt-8 grid gap-10 lg:grid-cols-[1.4fr_1fr]">
            <div>
              <p className="flex items-center gap-1.5 text-[13px] text-ink/50">
                <MapPin size={13} /> {project.district}
              </p>
              <h1 className="mt-2 font-display text-[2rem] font-semibold text-ink sm:text-[2.4rem]">
                {project.name}
              </h1>
              <p className="mt-4 max-w-2xl text-[15px] leading-relaxed text-ink/60">{project.description}</p>

              <span className="mt-4 inline-block rounded-md bg-gold/10 px-3 py-1.5 font-mono text-[11px] font-medium text-gold-dark">
                {project.tag}
              </span>

              <dl className="mt-8 grid grid-cols-2 gap-x-6 gap-y-5 border-t border-ink/8 pt-6 sm:grid-cols-3">
                {facts.map((f) => (
                  <div key={f.label}>
                    <dt className="font-mono text-[10.5px] uppercase tracking-wide text-ink/40">{f.label}</dt>
                    <dd className="mt-1 text-[14px] font-medium text-ink">{f.value}</dd>
                  </div>
                ))}
              </dl>

              <div className="mt-8 flex items-center gap-6 border-t border-ink/8 pt-6 text-[13.5px] text-ink/60">
                <span className="flex items-center gap-1.5">
                  <BedDouble size={15} /> {project.beds}
                </span>
                <span className="flex items-center gap-1.5">
                  <Ruler size={15} /> {project.area}
                </span>
                <span className="flex items-center gap-1.5">
                  <CalendarClock size={15} /> Handover {project.handover}
                </span>
              </div>
            </div>

            <aside className="h-fit rounded-2xl border border-ink/8 bg-white p-6 shadow-card lg:sticky lg:top-24">
              <p className="font-mono text-[10.5px] uppercase tracking-wide text-ink/40">Price range</p>
              <p className="mt-1 font-display text-[1.6rem] font-semibold text-lacquer">
                {formatVnd(project.priceFromVnd)}
              </p>
              <p className="text-[13px] text-ink/45">
                to {formatVnd(project.priceToVnd)} · ≈ {formatUsd(project.priceFromUsd)}–{formatUsd(project.priceToUsd)}
              </p>
              <Link
                href="/contact"
                className="mt-5 block rounded-full bg-lacquer px-5 py-3 text-center text-[13.5px] font-semibold text-white transition hover:bg-lacquer-dark"
              >
                Book a free consultation
              </Link>
              <p className="mt-3 text-center text-[12px] text-ink/40">Advisor-verified {project.verifiedDate}</p>
            </aside>
          </div>
        </div>
      </section>

      <CtaBanner />
    </>
  );
}
