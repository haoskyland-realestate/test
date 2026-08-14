export interface TimelineEntry {
  period: string;
  detail: string;
}

export interface TeamMember {
  name: string;
  alias?: string;
  role: string;
  initials: string;
  accent: number;
  timeline: TimelineEntry[];
}

export const founder: TeamMember & { quote: string } = {
  name: "Mai Anh Thu",
  alias: "Anna",
  role: "Founder & CEO",
  initials: "MT",
  accent: 0,
  quote:
    "We named the firm Vietland because a bridge only matters if both sides can cross it. Our job is to make Vietnam feel reachable, in whatever language you think in.",
  timeline: [
    { period: "2008 – 2018", detail: "Senior leadership roles across two national developer sales networks." },
    { period: "2019", detail: "Founded the original Lotus Bridge advisory brand for cross-border buyers." },
    { period: "2016", detail: "Founded Lotus Bridge Realty JSC." },
  ],
};

export const teamMembers: TeamMember[] = [
  {
    name: "Do Trung Kien",
    alias: "Kevin",
    role: "Director of Sales & Digital Marketing",
    initials: "DK",
    accent: 1,
    timeline: [
      { period: "2010 – 2016", detail: "B.A. Business Administration, RMIT Vietnam." },
      { period: "2016 – 2019", detail: "Head of International Sales, national developer network." },
      { period: "2020 – present", detail: "Director of Sales & Digital Marketing, Lotus Bridge Realty." },
    ],
  },
  {
    name: "Han Ji-woo",
    role: "Head of Korean Client Desk",
    initials: "HJ",
    accent: 2,
    timeline: [
      { period: "2017 – 2020", detail: "B.A. Hospitality Management, Kyonggi University." },
      { period: "2021 – 2023", detail: "International marketing, regional clinic group." },
      { period: "2023 – present", detail: "Head of Korean Client Desk, Lotus Bridge Realty." },
    ],
  },
  {
    name: "Su Wen-Hao",
    alias: "Kevin",
    role: "Head of Greater China Client Desk",
    initials: "SW",
    accent: 3,
    timeline: [
      { period: "2010 – 2013", detail: "B.B.A. Business Administration, Yuan Ze University, Taiwan." },
      { period: "2014 – 2018", detail: "Foreign client sales executive, regional developer." },
      { period: "2019 – present", detail: "Head of Greater China Client Desk, Lotus Bridge Realty." },
    ],
  },
];
