import type { Metadata } from "next";
import { MapPin, Mail, Clock } from "lucide-react";
import ContactForm from "../../components/ContactForm";
import OfficeNetworkMap from "../../components/OfficeNetworkMap";
import NewsletterForm from "../../components/NewsletterForm";

export const metadata: Metadata = {
  title: "Contact — Vietland",
};

export default function ContactPage() {
  return (
    <>
      <section className="py-14 md:py-20">
        <div className="container-page grid gap-12 lg:grid-cols-[1fr_1.1fr]">
          <div>
            <p className="eyebrow text-lacquer">Contact</p>
            <h1 className="mt-3 font-display text-[2.1rem] font-semibold leading-tight text-ink sm:text-[2.4rem]">
              Talk to an advisor in your language.
            </h1>
            <p className="mt-4 max-w-md text-[14.5px] leading-relaxed text-ink/60">
              Tell us where you&rsquo;re looking and what matters most, and we&rsquo;ll match you with the
              advisor on our team best placed to help.
            </p>

            <div className="mt-8 space-y-4 border-t border-ink/8 pt-6">
              <p className="flex items-start gap-3 text-[13.5px] text-ink/65">
                <MapPin size={16} className="mt-0.5 shrink-0 text-lacquer" />
                Lotus Bridge Tower, Thao Dien, Thu Duc, Ho Chi Minh City
              </p>
              <p className="flex items-start gap-3 text-[13.5px] text-ink/65">
                <Mail size={16} className="mt-0.5 shrink-0 text-lacquer" />
                hello@vietland-example.com
              </p>
              <p className="flex items-start gap-3 text-[13.5px] text-ink/65">
                <Clock size={16} className="mt-0.5 shrink-0 text-lacquer" />
                Mon – Sat, 8:30am – 6:30pm (GMT+7)
              </p>
            </div>
          </div>

          <ContactForm />
        </div>
      </section>

      <section className="border-t border-ink/8 bg-ink-gradient py-16 text-white md:py-20">
        <div className="container-page">
          <p className="eyebrow text-gold-light">Our office network</p>
          <h2 className="mt-3 font-display text-[1.9rem] font-semibold sm:text-[2.2rem]">
            Nine years, three regions, one advisory.
          </h2>
          <div className="mt-10">
            <OfficeNetworkMap variant="full" />
          </div>
        </div>
      </section>

      <section className="bg-paper py-14">
        <div className="container-page">
          <div className="flex flex-col items-start gap-5 rounded-2xl border border-ink/8 bg-white p-8 shadow-card sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="font-display text-lg font-semibold text-ink">Subscribe to the Market Pulse</p>
              <p className="mt-1 max-w-sm text-[13.5px] text-ink/55">
                A short monthly note on pricing, new launches and ownership-rule changes — in the language you choose.
              </p>
            </div>
            <div className="w-full sm:w-80">
              <NewsletterForm />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
