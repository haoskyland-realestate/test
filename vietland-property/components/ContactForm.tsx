"use client";

import { useState, FormEvent } from "react";
import { CheckCircle2 } from "lucide-react";

const languages = ["English", "中文", "한국어", "Tiếng Việt"];
const budgets = ["Under $150K", "$150K – $400K", "$400K – $800K", "Over $800K"];

export default function ContactForm() {
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <div className="flex flex-col items-center justify-center rounded-2xl border border-jade/25 bg-jade/5 px-6 py-14 text-center">
        <CheckCircle2 className="text-jade" size={32} />
        <p className="mt-3 font-display text-lg font-semibold text-ink">Message sent.</p>
        <p className="mt-1 max-w-xs text-[13.5px] text-ink/55">
          An advisor will reply in your preferred language within one business day.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-2xl border border-ink/8 bg-white p-6 shadow-card sm:p-8">
      <div className="grid gap-5 sm:grid-cols-2">
        <label className="block">
          <span className="mb-1.5 block text-[13px] font-medium text-ink/70">Full name</span>
          <input
            required
            type="text"
            placeholder="Jane Smith"
            className="w-full rounded-lg border border-ink/12 px-3.5 py-2.5 text-[14px] text-ink placeholder:text-ink/30 focus:outline-none"
          />
        </label>

        <label className="block">
          <span className="mb-1.5 block text-[13px] font-medium text-ink/70">Email</span>
          <input
            required
            type="email"
            placeholder="you@example.com"
            className="w-full rounded-lg border border-ink/12 px-3.5 py-2.5 text-[14px] text-ink placeholder:text-ink/30 focus:outline-none"
          />
        </label>

        <label className="block">
          <span className="mb-1.5 block text-[13px] font-medium text-ink/70">Phone / WhatsApp</span>
          <input
            type="tel"
            placeholder="+1 555 000 0000"
            className="w-full rounded-lg border border-ink/12 px-3.5 py-2.5 text-[14px] text-ink placeholder:text-ink/30 focus:outline-none"
          />
        </label>

        <label className="block">
          <span className="mb-1.5 block text-[13px] font-medium text-ink/70">Preferred language</span>
          <select className="w-full rounded-lg border border-ink/12 px-3.5 py-2.5 text-[14px] text-ink focus:outline-none">
            {languages.map((l) => (
              <option key={l}>{l}</option>
            ))}
          </select>
        </label>

        <label className="block sm:col-span-2">
          <span className="mb-1.5 block text-[13px] font-medium text-ink/70">Budget range</span>
          <select className="w-full rounded-lg border border-ink/12 px-3.5 py-2.5 text-[14px] text-ink focus:outline-none">
            {budgets.map((b) => (
              <option key={b}>{b}</option>
            ))}
          </select>
        </label>

        <label className="block sm:col-span-2">
          <span className="mb-1.5 block text-[13px] font-medium text-ink/70">What are you looking for?</span>
          <textarea
            rows={4}
            placeholder="City, property type, timeline…"
            className="w-full resize-none rounded-lg border border-ink/12 px-3.5 py-2.5 text-[14px] text-ink placeholder:text-ink/30 focus:outline-none"
          />
        </label>
      </div>

      <button
        type="submit"
        className="mt-6 w-full rounded-full bg-lacquer px-6 py-3.5 text-[14px] font-semibold text-white transition hover:bg-lacquer-dark sm:w-auto"
      >
        Send message
      </button>
    </form>
  );
}
