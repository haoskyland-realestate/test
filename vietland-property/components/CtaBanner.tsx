import Link from "next/link";
import { ArrowRight } from "lucide-react";

export default function CtaBanner() {
  return (
    <section className="bg-paper px-5 py-4 md:px-8">
      <div className="container-page">
        <div className="relative overflow-hidden rounded-3xl bg-lacquer-gradient px-8 py-14 text-center sm:px-16">
          <div
            className="pointer-events-none absolute inset-0 opacity-[0.08]"
            style={{
              backgroundImage:
                "radial-gradient(circle at 20% 20%, white 1px, transparent 1px), radial-gradient(circle at 80% 60%, white 1px, transparent 1px)",
              backgroundSize: "48px 48px",
            }}
          />
          <p className="eyebrow text-gold-light">Free, no-obligation consultation</p>
          <h2 className="mx-auto mt-3 max-w-xl font-display text-[1.9rem] font-semibold text-white sm:text-[2.3rem]">
            Let&rsquo;s find the right property, in the right language.
          </h2>
          <p className="mx-auto mt-3 max-w-md text-[14.5px] text-white/75">
            A 20-minute call with a licensed advisor — no pressure, just clarity on your options.
          </p>
          <Link
            href="/contact"
            className="mt-7 inline-flex items-center gap-2 rounded-full bg-white px-7 py-3.5 text-[14px] font-semibold text-lacquer transition hover:bg-gold-light"
          >
            Book a free consultation <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </section>
  );
}
