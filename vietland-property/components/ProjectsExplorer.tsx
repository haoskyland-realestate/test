"use client";

import { useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Search, SlidersHorizontal } from "lucide-react";
import ProjectCard from "./ProjectCard";
import { projects, projectTypes } from "../data/projects";

const budgets = [
  { label: "Any budget", value: "" },
  { label: "Under $150K", value: "0-150000" },
  { label: "$150K – $400K", value: "150000-400000" },
  { label: "$400K – $800K", value: "400000-800000" },
  { label: "Over $800K", value: "800000-999999999" },
];

const sorts = ["Featured", "Price: Low to High", "Price: High to Low", "Newest"] as const;

export default function ProjectsExplorer() {
  const params = useSearchParams();

  const [query, setQuery] = useState(params.get("q") ?? "");
  const [type, setType] = useState(params.get("type") ?? "");
  const [budget, setBudget] = useState(params.get("budget") ?? "");
  const [sort, setSort] = useState<(typeof sorts)[number]>("Featured");

  const filtered = useMemo(() => {
    let list = projects.filter((p) => {
      const matchesQuery = query
        ? p.name.toLowerCase().includes(query.toLowerCase()) || p.city.toLowerCase().includes(query.toLowerCase())
        : true;
      const matchesType = type ? p.type === type : true;
      const matchesBudget = budget
        ? (() => {
            const [min, max] = budget.split("-").map(Number);
            return p.priceFromUsd <= max && p.priceToUsd >= min;
          })()
        : true;
      return matchesQuery && matchesType && matchesBudget;
    });

    if (sort === "Price: Low to High") list = [...list].sort((a, b) => a.priceFromUsd - b.priceFromUsd);
    if (sort === "Price: High to Low") list = [...list].sort((a, b) => b.priceToUsd - a.priceToUsd);
    if (sort === "Newest") list = [...list].sort((a, b) => (a.verifiedDate < b.verifiedDate ? 1 : -1));

    return list;
  }, [query, type, budget, sort]);

  return (
    <section className="py-10 md:py-14">
      <div className="container-page">
        <div className="max-w-xl">
          <p className="eyebrow text-lacquer">Projects</p>
          <h1 className="mt-3 font-display text-[2.1rem] font-semibold text-ink sm:text-[2.4rem]">
            Vetted developments across Vietnam.
          </h1>
        </div>

        <div className="mt-8 rounded-2xl border border-ink/8 bg-white p-4 shadow-card">
          <div className="grid gap-3 sm:grid-cols-[1.4fr_1fr_1fr_1fr]">
            <label className="block">
              <span className="mb-1 block font-mono text-[10px] uppercase tracking-wider text-ink/40">Search</span>
              <div className="flex items-center gap-2 rounded-lg border border-ink/12 px-3 py-2.5">
                <Search size={15} className="text-ink/35" />
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search by name…"
                  className="w-full bg-transparent text-[13.5px] text-ink placeholder:text-ink/35 focus:outline-none"
                />
              </div>
            </label>

            <label className="block">
              <span className="mb-1 block font-mono text-[10px] uppercase tracking-wider text-ink/40">Type</span>
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="w-full rounded-lg border border-ink/12 px-3 py-2.5 text-[13.5px] text-ink"
              >
                <option value="">All types</option>
                {projectTypes.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </label>

            <label className="block">
              <span className="mb-1 block font-mono text-[10px] uppercase tracking-wider text-ink/40">Budget</span>
              <select
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full rounded-lg border border-ink/12 px-3 py-2.5 text-[13.5px] text-ink"
              >
                {budgets.map((b) => (
                  <option key={b.value} value={b.value}>
                    {b.label}
                  </option>
                ))}
              </select>
            </label>

            <label className="block">
              <span className="mb-1 flex items-center gap-1 font-mono text-[10px] uppercase tracking-wider text-ink/40">
                <SlidersHorizontal size={11} /> Sort by
              </span>
              <select
                value={sort}
                onChange={(e) => setSort(e.target.value as (typeof sorts)[number])}
                className="w-full rounded-lg border border-ink/12 px-3 py-2.5 text-[13.5px] text-ink"
              >
                {sorts.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>

        <p className="mt-5 text-[13.5px] text-ink/50">Showing {filtered.length} projects</p>

        {filtered.length > 0 ? (
          <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((p) => (
              <ProjectCard key={p.slug} project={p} />
            ))}
          </div>
        ) : (
          <div className="mt-10 rounded-2xl border border-dashed border-ink/15 py-16 text-center">
            <p className="font-display text-lg text-ink/70">No projects match those filters.</p>
            <p className="mt-1 text-[13.5px] text-ink/45">Try widening your budget or clearing the search.</p>
          </div>
        )}
      </div>
    </section>
  );
}
