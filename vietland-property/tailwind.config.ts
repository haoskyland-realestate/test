import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: "#FBF8F1",
        lacquer: {
          DEFAULT: "#A6231D",
          dark: "#711712",
          light: "#C43A2E",
        },
        gold: {
          DEFAULT: "#C9A15A",
          light: "#E7CE93",
          dark: "#8F6C33",
        },
        ink: {
          DEFAULT: "#10182B",
          light: "#1C2740",
          soft: "#2A3550",
        },
        jade: {
          DEFAULT: "#2F5D50",
          light: "#4C7C6D",
        },
        body: "#3D3A35",
      },
      fontFamily: {
        display: ['"Fraunces"', "ui-serif", "Georgia", "serif"],
        body: ['"IBM Plex Sans"', "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ['"IBM Plex Mono"', "ui-monospace", "SFMono-Regular", "monospace"],
      },
      backgroundImage: {
        "lacquer-gradient": "linear-gradient(135deg, #711712 0%, #A6231D 55%, #C43A2E 100%)",
        "ink-gradient": "linear-gradient(180deg, #10182B 0%, #1C2740 100%)",
      },
      boxShadow: {
        card: "0 1px 2px rgba(16,24,43,0.06), 0 12px 32px -12px rgba(16,24,43,0.18)",
        pop: "0 20px 45px -18px rgba(16,24,43,0.35)",
      },
      keyframes: {
        marquee: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
        pulseRing: {
          "0%": { transform: "scale(0.9)", opacity: "0.7" },
          "70%": { transform: "scale(2.1)", opacity: "0" },
          "100%": { transform: "scale(0.9)", opacity: "0" },
        },
      },
      animation: {
        marquee: "marquee 34s linear infinite",
        pulseRing: "pulseRing 2.6s cubic-bezier(0.4,0,0.6,1) infinite",
      },
    },
  },
  plugins: [],
};

export default config;
