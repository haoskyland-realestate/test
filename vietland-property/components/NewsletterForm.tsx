"use client";

import { useState, FormEvent } from "react";
import { Send } from "lucide-react";

export default function NewsletterForm({ dark = false }: { dark?: boolean }) {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!email) return;
    setSent(true);
  }

  if (sent) {
    return (
      <p className={`text-[13.5px] ${dark ? "text-gold-light" : "text-jade"}`}>
        Thanks — check your inbox to confirm your subscription.
      </p>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        className={`w-full rounded-full border px-4 py-2.5 text-[13.5px] focus:outline-none ${
          dark
            ? "border-white/15 bg-white/5 text-white placeholder:text-white/35"
            : "border-ink/12 bg-white text-ink placeholder:text-ink/35"
        }`}
      />
      <button
        type="submit"
        className="flex shrink-0 items-center gap-1.5 rounded-full bg-gold px-4 py-2.5 text-[13px] font-semibold text-ink transition hover:bg-gold-light"
      >
        <Send size={14} /> Subscribe
      </button>
    </form>
  );
}
