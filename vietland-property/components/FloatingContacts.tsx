import { MessageCircle, Phone, Mail, ArrowUp } from "lucide-react";

const buttons = [
  { icon: MessageCircle, href: "#", label: "Chat with an advisor", bg: "bg-jade" },
  { icon: Phone, href: "tel:+84000000000", label: "Call us", bg: "bg-lacquer" },
  { icon: Mail, href: "mailto:hello@vietland-example.com", label: "Email us", bg: "bg-gold" },
];

export default function FloatingContacts() {
  return (
    <div className="fixed bottom-5 right-5 z-30 flex flex-col items-center gap-3">
      {buttons.map((b) => (
        <a
          key={b.label}
          href={b.href}
          aria-label={b.label}
          className={`flex h-11 w-11 items-center justify-center rounded-full text-white shadow-pop transition hover:scale-105 ${b.bg}`}
        >
          <b.icon size={18} />
        </a>
      ))}
      <a
        href="#top"
        aria-label="Back to top"
        className="flex h-11 w-11 items-center justify-center rounded-full border border-ink/10 bg-white text-ink/60 shadow-card transition hover:text-lacquer"
      >
        <ArrowUp size={18} />
      </a>
    </div>
  );
}
