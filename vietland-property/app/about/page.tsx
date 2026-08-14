import type { Metadata } from "next";
import Avatar from "../../components/Avatar";
import { founder, teamMembers } from "../../data/team";
import CtaBanner from "../../components/CtaBanner";

export const metadata: Metadata = {
  title: "About — Vietland",
};

const stats = [
  { value: "3,000+", label: "International transactions since 2016" },
  { value: "$800M+", label: "Cumulative transaction value" },
  { value: "28", label: "Buyer-source countries" },
  { value: "9 yrs", label: "Specialised in foreign-buyer real estate" },
];

export default function AboutPage() {
  return (
    <>
      <section className="bg-lacquer-gradient px-5 py-16 md:px-8 md:py-20">
        <div className="container-page">
          <p className="eyebrow text-gold-light">About Vietland</p>
          <h1 className="mt-3 max-w-2xl font-display text-[2.1rem] font-semibold leading-tight text-white sm:text-[2.6rem]">
            A bridge between international buyers and Vietnamese real estate.
          </h1>
          <p className="mt-4 max-w-2xl text-[15px] leading-relaxed text-white/75">
            Founded in Ho Chi Minh City, Lotus Bridge Realty JSC has guided thousands of international
            families through buying residential property in Vietnam — across nine cities and dozens of
            developments.
          </p>
        </div>
      </section>

      <section className="py-16 md:py-20">
        <div className="container-page grid gap-12 md:grid-cols-2 md:items-center">
          <div>
            <p className="eyebrow text-lacquer">Our story</p>
            <h2 className="mt-3 font-display text-[1.9rem] font-semibold leading-tight text-ink sm:text-[2.2rem]">
              Built for the buyer who isn&rsquo;t from here.
            </h2>
            <div className="mt-5 space-y-4 text-[14.5px] leading-relaxed text-ink/60">
              <p>
                When Vietnam opened residential property to foreign buyers, the local distribution
                machinery wasn&rsquo;t ready for them: contracts in dense legal Vietnamese, advisors who
                didn&rsquo;t share a language with their clients, and support that quietly disappeared
                after the deposit cleared.
              </p>
              <p>
                We built Vietland to close that gap — a team that treats a language barrier as a problem
                to solve, not an inconvenience to route around. Today we work with developers across the
                country, chosen for the discipline we bring to Korean, Chinese, Taiwanese and English-speaking
                buyer pools.
              </p>
            </div>

            <dl className="mt-8 grid grid-cols-2 gap-x-6 gap-y-6 border-t border-ink/8 pt-6">
              {stats.map((s) => (
                <div key={s.label}>
                  <dt className="font-display text-[1.7rem] font-semibold text-ink">{s.value}</dt>
                  <dd className="mt-1 text-[12.5px] text-ink/45">{s.label}</dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="mx-auto flex aspect-square w-full max-w-sm flex-col items-center justify-center rounded-3xl bg-lacquer-gradient p-8 text-center shadow-pop">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-gold-light/80">Established 2016</p>
            <p className="mt-4 font-display text-4xl font-semibold text-white">VIETLAND</p>
            <p className="mt-2 text-[12px] uppercase tracking-[0.2em] text-white/60">
              Real Estate · Ho Chi Minh City
            </p>
          </div>
        </div>
      </section>

      <section className="border-t border-ink/8 bg-paper py-16 md:py-20">
        <div className="container-page">
          <p className="eyebrow text-jade">Leadership</p>
          <h2 className="mt-3 font-display text-[1.9rem] font-semibold text-ink sm:text-[2.2rem]">
            The people behind the advisory.
          </h2>

          <div className="mt-10 flex flex-col gap-6 rounded-2xl border border-ink/8 bg-white p-6 shadow-card sm:flex-row sm:p-8">
            <Avatar initials={founder.initials} accent={founder.accent} className="h-40 w-full shrink-0 rounded-xl sm:w-40" />
            <div>
              <p className="eyebrow text-lacquer">Founder & CEO</p>
              <h3 className="mt-1 font-display text-xl font-semibold text-ink">
                {founder.name} <span className="font-body text-base font-normal text-ink/45">({founder.alias})</span>
              </h3>
              <blockquote className="mt-3 border-l-2 border-gold pl-4 text-[14.5px] italic leading-relaxed text-ink/65">
                &ldquo;{founder.quote}&rdquo;
              </blockquote>
              <ul className="mt-4 flex flex-wrap gap-x-8 gap-y-2">
                {founder.timeline.map((t) => (
                  <li key={t.period} className="text-[12.5px] text-ink/55">
                    <span className="block font-mono text-[11px] font-semibold text-ink/80">{t.period}</span>
                    {t.detail}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mt-6 grid gap-6 sm:grid-cols-3">
            {teamMembers.map((m) => (
              <div key={m.name} className="overflow-hidden rounded-2xl border border-ink/8 bg-white shadow-card">
                <Avatar initials={m.initials} accent={m.accent} className="h-40 w-full" />
                <div className="p-5">
                  <p className="eyebrow text-lacquer">{m.role}</p>
                  <h3 className="mt-1 font-display text-[1.05rem] font-semibold text-ink">
                    {m.name} {m.alias && <span className="font-body text-sm font-normal text-ink/45">({m.alias})</span>}
                  </h3>
                  <ul className="mt-3 space-y-2 border-t border-ink/8 pt-3">
                    {m.timeline.map((t) => (
                      <li key={t.period} className="text-[12px] text-ink/55">
                        <span className="mr-1.5 font-mono text-[11px] font-semibold text-ink/75">{t.period}</span>
                        {t.detail}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <CtaBanner />
    </>
  );
}
