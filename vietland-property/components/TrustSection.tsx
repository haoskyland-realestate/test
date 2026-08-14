import { ShieldCheck, Languages, FileCheck2, PiggyBank } from "lucide-react";

const reasons = [
  {
    icon: ShieldCheck,
    title: "Verified foreign-ownership eligibility",
    body: "Every listing is checked against each project's foreign-buyer quota before it reaches you.",
  },
  {
    icon: Languages,
    title: "Bilingual legal walkthroughs",
    body: "Contracts explained clause by clause in English, 中文 or 한국어 — not just translated.",
  },
  {
    icon: FileCheck2,
    title: "Escrow-backed agreements",
    body: "Sale & purchase agreements signed directly with the developer, deposits held in escrow.",
  },
  {
    icon: PiggyBank,
    title: "Post-sale & repatriation support",
    body: "Help with title registration, resale, rental management and repatriating proceeds.",
  },
];

export default function TrustSection() {
  return (
    <section className="border-t border-ink/8 bg-white py-16 md:py-20">
      <div className="container-page">
        <div className="max-w-xl">
          <p className="eyebrow text-lacquer">Why buyers choose Vietland</p>
          <h2 className="mt-3 font-display text-[2rem] font-semibold text-ink sm:text-[2.3rem]">
            Everything a local buyer knows, translated for you.
          </h2>
        </div>

        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {reasons.map((r) => (
            <div key={r.title} className="rounded-2xl border border-ink/8 p-6 transition hover:border-lacquer/30 hover:shadow-card">
              <span className="flex h-11 w-11 items-center justify-center rounded-full bg-lacquer/10 text-lacquer">
                <r.icon size={20} strokeWidth={1.75} />
              </span>
              <h3 className="mt-4 font-display text-[1.05rem] font-semibold text-ink">{r.title}</h3>
              <p className="mt-2 text-[13.5px] leading-relaxed text-ink/55">{r.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
