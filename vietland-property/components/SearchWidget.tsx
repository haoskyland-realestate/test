"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Search } from "lucide-react";
import { projectTypes } from "../data/projects";

const budgets = [
  { label: "Any budget", value: "" },
  { label: "Under $150K", value: "0-150000" },
  { label: "$150K – $400K", value: "150000-400000" },
  { label: "$400K – $800K", value: "400000-800000" },
  { label: "Over $800K", value: "800000-999999999" },
];

export default function SearchWidget() {
  const router = useRouter();
  const [mode, setMode] = useState<"Buy" | "Invest">("Buy");
  const [query, setQuery] = useState("");
  const [type, setType] = useState("");
  const [budget, setBudget] = useState("");

  function handleSearch() {
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (type) params.set("type", type);
    if (budget) params.set("budget", budget);
    if (mode === "Invest") params.set("mode", "invest");
    router.push(`/projects${params.toString() ? `?${params.toString()}` : ""}`);
  }

  return (
    <div className="rounded-2xl border border-ink/8 bg-white p-2 shadow-pop">
      <div className="flex gap-1 px-1 pt-1">
        {(["Buy", "Invest"] as const).map((m) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            className={`rounded-lg px-4 py-2 text-[13.5px] font-semibold transition ${
              mode === m ? "bg-ink text-white" : "text-ink/55 hover:bg-ink/5"
            }`}
          >
            {m}
          </button>
        ))}
      </div>

      <div className="mt-2 grid gap-2 p-2 sm:grid-cols-[1.4fr_1fr_1fr_auto]">
        <label className="block">
          <span className="mb-1 block font-mono text-[10px] uppercase tracking-wider text-ink/40">Project</span>
          <div className="flex items-center gap-2 rounded-lg border border-ink/12 px-3 py-2.5">
            <Search size={15} className="text-ink/35" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by project name"
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
            <option value="">Any type</option>
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

        <button
          onClick={handleSearch}
          className="flex items-center justify-center gap-2 rounded-lg bg-lacquer px-5 py-2.5 text-[13.5px] font-semibold text-white transition hover:bg-lacquer-dark sm:mt-[22px]"
        >
          <Search size={15} /> Search
        </button>
      </div>
    </div>
  );
}
