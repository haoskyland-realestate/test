"use client";

import Link from "next/link";
import { useState } from "react";
import { ChevronDown, Menu, X, Check } from "lucide-react";

const navLinks = [
  { href: "/projects", label: "Projects" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

const languages = [
  { code: "EN", label: "English" },
  { code: "TW", label: "繁體中文" },
  { code: "CN", label: "简体中文" },
  { code: "KR", label: "한국어" },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const [lang, setLang] = useState(languages[0]);

  return (
    <header className="sticky top-0 z-40 border-b border-ink/8 bg-paper/90 backdrop-blur">
      <div className="container-page flex h-[72px] items-center justify-between gap-4">
        <Link href="/" className="flex items-center gap-3" onClick={() => setMobileOpen(false)}>
          <span className="flex h-9 w-9 items-center justify-center rounded-md bg-lacquer-gradient font-display text-base font-semibold text-gold-light">
            V
          </span>
          <span className="leading-tight">
            <span className="block font-display text-[15px] font-semibold tracking-tight text-ink">
              VIETLAND
            </span>
            <span className="block text-[11px] text-ink/50">by Lotus Bridge Realty</span>
          </span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-[14.5px] font-medium text-ink/70 transition hover:text-lacquer"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          <div className="relative">
            <button
              onClick={() => setLangOpen((v) => !v)}
              aria-expanded={langOpen}
              aria-haspopup="listbox"
              className="flex items-center gap-1.5 rounded-full border border-ink/12 px-3 py-1.5 text-[13px] font-medium text-ink/75 transition hover:border-lacquer/40"
            >
              {lang.code} <ChevronDown size={14} className={`transition ${langOpen ? "rotate-180" : ""}`} />
            </button>
            {langOpen && (
              <ul
                role="listbox"
                className="absolute right-0 top-[calc(100%+8px)] w-40 overflow-hidden rounded-lg border border-ink/8 bg-white py-1 shadow-pop"
              >
                {languages.map((l) => (
                  <li key={l.code}>
                    <button
                      role="option"
                      aria-selected={lang.code === l.code}
                      onClick={() => {
                        setLang(l);
                        setLangOpen(false);
                      }}
                      className="flex w-full items-center justify-between px-3 py-2 text-left text-[13.5px] text-ink/75 hover:bg-paper"
                    >
                      <span>
                        <span className="mr-2 text-ink/40">{l.code}</span>
                        {l.label}
                      </span>
                      {lang.code === l.code && <Check size={14} className="text-lacquer" />}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <Link
            href="/contact"
            className="rounded-full bg-lacquer px-5 py-2.5 text-[13.5px] font-semibold text-white shadow-card transition hover:bg-lacquer-dark"
          >
            Book a free consultation
          </Link>
        </div>

        <button
          className="p-1.5 text-ink md:hidden"
          onClick={() => setMobileOpen((v) => !v)}
          aria-label="Toggle menu"
        >
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {mobileOpen && (
        <div className="border-t border-ink/8 bg-paper px-5 pb-6 pt-3 md:hidden">
          <nav className="flex flex-col gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="rounded-md px-2 py-2.5 text-[15px] font-medium text-ink/80 hover:bg-ink/5"
              >
                {link.label}
              </Link>
            ))}
          </nav>
          <Link
            href="/contact"
            onClick={() => setMobileOpen(false)}
            className="mt-3 block rounded-full bg-lacquer px-5 py-3 text-center text-[14px] font-semibold text-white"
          >
            Book a free consultation
          </Link>
        </div>
      )}
    </header>
  );
}
