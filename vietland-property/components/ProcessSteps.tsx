const steps = [
  {
    n: "01",
    title: "Discover",
    body: "Browse vetted listings by city, budget and property type, or tell us what you're after.",
  },
  {
    n: "02",
    title: "Verify",
    body: "We confirm the project's foreign-ownership quota and legal status before you commit.",
  },
  {
    n: "03",
    title: "Reserve",
    body: "Sign the sale & purchase agreement directly with the developer; your deposit is escrowed.",
  },
  {
    n: "04",
    title: "Own",
    body: "We handle title registration and stay on for resale, rental or repatriation support.",
  },
];

export default function ProcessSteps() {
  return (
    <section className="bg-paper py-16 md:py-20">
      <div className="container-page">
        <div className="max-w-xl">
          <p className="eyebrow text-jade">How it works</p>
          <h2 className="mt-3 font-display text-[2rem] font-semibold text-ink sm:text-[2.3rem]">
            Four steps from first look to final deed.
          </h2>
        </div>

        <div className="mt-10 grid gap-0 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((s, i) => (
            <div key={s.n} className="relative border-t border-ink/10 py-6 pr-6 lg:border-l lg:border-t-0 lg:pl-6 lg:py-0 lg:first:border-l-0">
              <span className="font-mono text-[13px] text-gold-dark">{s.n}</span>
              <h3 className="mt-2 font-display text-[1.15rem] font-semibold text-ink">{s.title}</h3>
              <p className="mt-2 text-[13.5px] leading-relaxed text-ink/55">{s.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
