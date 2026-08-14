export type ProjectType = "Apartment" | "Villa" | "Condotel" | "Township";

export interface Project {
  slug: string;
  name: string;
  developer: string;
  city: string;
  region: "North" | "Central" | "South";
  district: string;
  badge: "EXCLUSIVE" | "NEW" | null;
  verifiedDate: string;
  type: ProjectType;
  description: string;
  tag: string;
  beds: string;
  area: string;
  priceFromVnd: number;
  priceToVnd: number;
  priceFromUsd: number;
  priceToUsd: number;
  accent: number;
  handover: string;
}

export const projects: Project[] = [
  {
    slug: "riverline-residences",
    name: "Riverline Residences",
    developer: "Phuong Nam Land",
    city: "Ho Chi Minh City",
    region: "South",
    district: "District 2 · HCMC",
    badge: "EXCLUSIVE",
    verifiedDate: "2026-05",
    type: "Township",
    description:
      "A 92-hectare riverside masterplan with four residential clusters, a linear park and a private marina promenade.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "Studio · 1–3 BR",
    area: "34 – 128 m²",
    priceFromVnd: 4900000000,
    priceToVnd: 15800000000,
    priceFromUsd: 195000,
    priceToUsd: 630000,
    accent: 0,
    handover: "Q2 2028",
  },
  {
    slug: "sapphire-bay-towers",
    name: "Sapphire Bay Towers",
    developer: "Coastal Sun Group",
    city: "Da Nang",
    region: "Central",
    district: "My Khe, Son Tra",
    badge: "NEW",
    verifiedDate: "2026-04",
    type: "Condotel",
    description:
      "Beachfront condotel with resort-operated units, an infinity pool deck and full hotel-style rental management.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "Studio · 1–2 BR",
    area: "28 – 76 m²",
    priceFromVnd: 2600000000,
    priceToVnd: 7100000000,
    priceFromUsd: 104000,
    priceToUsd: 284000,
    accent: 1,
    handover: "Q4 2027",
  },
  {
    slug: "golden-lotus-residence",
    name: "Golden Lotus Residence",
    developer: "An Lac Investment",
    city: "Binh Duong",
    region: "South",
    district: "Thuan An, Binh Duong",
    badge: "NEW",
    verifiedDate: "2026-03",
    type: "Apartment",
    description:
      "Low-density residences bordered by a protected forest reserve, with a resident wellness pavilion and co-working lounge.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "1–3 BR + Duplex",
    area: "42 – 118 m²",
    priceFromVnd: 1900000000,
    priceToVnd: 5200000000,
    priceFromUsd: 76000,
    priceToUsd: 208000,
    accent: 2,
    handover: "Q1 2027",
  },
  {
    slug: "west-lake-crown",
    name: "West Lake Crown",
    developer: "Thang Long Urban JSC",
    city: "Ha Noi",
    region: "North",
    district: "Tay Ho, Ha Noi",
    badge: "EXCLUSIVE",
    verifiedDate: "2026-05",
    type: "Apartment",
    description:
      "Twin-tower residence overlooking West Lake, with a rooftop sky lounge and direct access to the lakeside promenade.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "1–4 BR + Penthouse",
    area: "48 – 165 m²",
    priceFromVnd: 6200000000,
    priceToVnd: 21000000000,
    priceFromUsd: 248000,
    priceToUsd: 840000,
    accent: 3,
    handover: "Q3 2028",
  },
  {
    slug: "azure-cove-villas",
    name: "Azure Cove Villas",
    developer: "Nha Trang Coastal Corp",
    city: "Nha Trang",
    region: "Central",
    district: "Bac Bai Dai, Nha Trang",
    badge: null,
    verifiedDate: "2026-02",
    type: "Villa",
    description:
      "Hillside villa enclave with private plunge pools, terraced gardens and uninterrupted sea views over Bai Dai bay.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "3–5 BR Villa",
    area: "210 – 340 m²",
    priceFromVnd: 18500000000,
    priceToVnd: 34000000000,
    priceFromUsd: 740000,
    priceToUsd: 1360000,
    accent: 4,
    handover: "Q2 2027",
  },
  {
    slug: "pearl-island-residences",
    name: "Pearl Island Residences",
    developer: "Emerald Isle Developments",
    city: "Phu Quoc",
    region: "South",
    district: "Duong Dong, Phu Quoc",
    badge: "NEW",
    verifiedDate: "2026-06",
    type: "Condotel",
    description:
      "Low-rise island condotel with a private beach club, ten minutes from the night market and the new marina district.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "Studio · 1–2 BR",
    area: "32 – 82 m²",
    priceFromVnd: 2200000000,
    priceToVnd: 6400000000,
    priceFromUsd: 88000,
    priceToUsd: 256000,
    accent: 5,
    handover: "Q4 2027",
  },
  {
    slug: "the-meridian-quarter",
    name: "The Meridian Quarter",
    developer: "Phuong Nam Land",
    city: "Ho Chi Minh City",
    region: "South",
    district: "Thu Duc City, HCMC",
    badge: null,
    verifiedDate: "2026-01",
    type: "Apartment",
    description:
      "Transit-oriented residential block beside the metro line, built around a shaded central courtyard and retail podium.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "Studio · 1–3 BR",
    area: "30 – 95 m²",
    priceFromVnd: 2900000000,
    priceToVnd: 7800000000,
    priceFromUsd: 116000,
    priceToUsd: 312000,
    accent: 0,
    handover: "Q1 2028",
  },
  {
    slug: "highland-pine-villas",
    name: "Highland Pine Villas",
    developer: "Alpine Ridge JSC",
    city: "Da Lat",
    region: "Central",
    district: "Xuan Tho, Da Lat",
    badge: null,
    verifiedDate: "2025-12",
    type: "Villa",
    description:
      "Pine-forest villa retreat in the highlands, designed for a cool-climate second home with a shared farm-to-table pavilion.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "3–4 BR Villa",
    area: "180 – 260 m²",
    priceFromVnd: 9800000000,
    priceToVnd: 16500000000,
    priceFromUsd: 392000,
    priceToUsd: 660000,
    accent: 1,
    handover: "Q3 2027",
  },
  {
    slug: "harbor-light-tower",
    name: "Harbor Light Tower",
    developer: "Coastal Sun Group",
    city: "Da Nang",
    region: "Central",
    district: "Han River, Da Nang",
    badge: null,
    verifiedDate: "2026-02",
    type: "Apartment",
    description:
      "Riverfront tower facing the Dragon Bridge, with a resident sky garden on the 32nd floor and full river-view glazing.",
    tag: "SPA · 50YR + RENEWABLE + RESELL → VN",
    beds: "1–3 BR",
    area: "44 – 110 m²",
    priceFromVnd: 3400000000,
    priceToVnd: 8900000000,
    priceFromUsd: 136000,
    priceToUsd: 356000,
    accent: 2,
    handover: "Q2 2027",
  },
];

export const projectTypes: ProjectType[] = ["Apartment", "Villa", "Condotel", "Township"];

export function formatVnd(value: number) {
  return `${(value / 1_000_000_000).toLocaleString("en-US", {
    maximumFractionDigits: 1,
  })} Billion VND`;
}

export function formatUsd(value: number) {
  return `$${Math.round(value / 1000)}K`;
}
