import Link from "next/link";
import SearchWidget from "./SearchWidget";
import CityNetworkMap from "./CityNetworkMap";

const stats = [
  { value: "3,000+", label: "Global buyers advised" },
  { value: "58", label: "Provinces mapped" },
  { value: "9", label: "Years guiding foreign buyers" },
  { value: "5", label: "Languages spoken" },
];

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-paper pb-16 pt-14 md:pb-24 md:pt-20">
      <div className="container-page grid gap-12 md:grid-cols-[1.05fr_0.75fr] md:items-start">
        <div>
          <span className="eyebrow rounded-full border border-lacquer/25 bg-lacquer/5 px-3 py-1.5 text-lacquer">
            Vietnam real estate · Multilingual concierge
          </span>

          <h1 className="mt-5 font-display text-[2.6rem] font-semibold leading-[1.08] tracking-tight text-ink sm:text-[3.4rem]">
            Own property in Vietnam
            <span className="block text-lacquer">— vetted, legal, guided.</span>
          </h1>

          <p className="mt-5 max-w-xl text-[16.5px] leading-relaxed text-ink/60">
            Hand-picked apartments, villas and condotels across Vietnam&rsquo;s fastest-growing cities.
            Every listing is checked against foreign-ownership rules, with an advisor who speaks your
            language from first call to final deed.
          </p>

          <div className="mt-8">
            <SearchWidget />
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <Link
              href="/contact"
              className="rounded-full bg-lacquer px-6 py-3 text-[14px] font-semibold text-white shadow-card transition hover:bg-lacquer-dark"
            >
              Book a free consultation
            </Link>
            <Link
              href="/projects"
              className="rounded-full border border-ink/15 px-6 py-3 text-[14px] font-semibold text-ink/75 transition hover:border-lacquer/40 hover:text-lacquer"
            >
              Explore all projects
            </Link>
          </div>

          <dl className="mt-12 grid grid-cols-2 gap-x-6 gap-y-7 border-t border-ink/8 pt-8 sm:grid-cols-4">
            {stats.map((s) => (
              <div key={s.label}>
                <dt className="font-display text-[1.9rem] font-semibold text-ink">{s.value}</dt>
                <dd className="mt-1 text-[12.5px] uppercase tracking-wide text-ink/45">{s.label}</dd>
              </div>
            ))}
          </dl>
        </div>

        <div className="relative mx-auto w-full max-w-sm md:mx-0">
          <CityNetworkMap />
        </div>
      </div>
    </section>
  );
}
