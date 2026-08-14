import Link from "next/link";
import { MapPin, Mail, MessageCircle, Phone } from "lucide-react";
import NewsletterForm from "./NewsletterForm";
import OfficeNetworkMap from "./OfficeNetworkMap";

const exploreLinks = [
  { href: "/projects", label: "Projects" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

const guideLinks = [
  "How foreigners can buy in Vietnam",
  "Understanding ownership quotas & leasehold",
  "Repatriating your sale proceeds",
  "Taxes & fees to budget for",
  "What happens after 50 years?",
];

export default function Footer() {
  return (
    <footer className="bg-ink-gradient text-white">
      <div className="container-page py-16">
        <div className="grid gap-12 lg:grid-cols-[1fr_1fr]">
          <div>
            <Link href="/" className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-md bg-gold font-display text-base font-semibold text-ink">
                V
              </span>
              <span className="leading-tight">
                <span className="block font-display text-[15px] font-semibold text-white">VIETLAND</span>
                <span className="block text-[11px] text-white/45">by Lotus Bridge Realty</span>
              </span>
            </Link>

            <p className="mt-5 max-w-sm text-[13.5px] leading-relaxed text-white/55">
              Vietland is the international advisory arm of Lotus Bridge Realty JSC — nine years
              guiding foreign buyers across Vietnam&rsquo;s residential market.
            </p>

            <div className="mt-6 max-w-sm">
              <p className="eyebrow mb-2 text-gold-light/80">Market briefings</p>
              <NewsletterForm dark />
            </div>

            <div className="mt-6 space-y-2 text-[13px] text-white/55">
              <p className="flex items-center gap-2">
                <MapPin size={14} className="text-gold-light" /> Lotus Bridge Tower, Thao Dien, Thu Duc, Ho Chi Minh City
              </p>
              <p className="flex items-center gap-2">
                <Mail size={14} className="text-gold-light" /> hello@vietland-example.com
              </p>
            </div>

            <div className="mt-5 flex gap-2.5">
              {[MessageCircle, Phone, Mail].map((Icon, i) => (
                <span
                  key={i}
                  className="flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-white/70"
                >
                  <Icon size={16} />
                </span>
              ))}
            </div>
          </div>

          <OfficeNetworkMap variant="compact" />
        </div>

        <div className="mt-14 grid gap-8 border-t border-white/10 pt-10 sm:grid-cols-[1fr_2fr]">
          <div>
            <p className="eyebrow text-white/40">Explore</p>
            <ul className="mt-3 space-y-2">
              {exploreLinks.map((l) => (
                <li key={l.href}>
                  <Link href={l.href} className="text-[13.5px] text-white/60 hover:text-gold-light">
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="eyebrow text-white/40">Buyer guides</p>
            <ul className="mt-3 grid gap-2 sm:grid-cols-2">
              {guideLinks.map((g) => (
                <li key={g}>
                  <span className="text-[13.5px] text-white/60">{g}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="container-page flex flex-col gap-2 py-5 text-[12px] text-white/40 sm:flex-row sm:items-center sm:justify-between">
          <p>© {new Date().getFullYear()} Lotus Bridge Realty JSC. All rights reserved.</p>
          <p className="flex gap-4">
            <span>Privacy</span>
            <span>Terms</span>
            <span>Cookie policy</span>
          </p>
        </div>
      </div>
    </footer>
  );
}
