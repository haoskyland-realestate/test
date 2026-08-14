export interface Office {
  name: string;
  region: "North" | "Central" | "South";
  kind: "headquarters" | "gallery" | "hub" | "office";
}

export const offices: Office[] = [
  { name: "Ha Noi Headquarters", region: "North", kind: "headquarters" },
  { name: "Ha Noi Sales Gallery", region: "North", kind: "gallery" },
  { name: "Ha Noi Service Hub", region: "North", kind: "hub" },
  { name: "My Dinh Office", region: "North", kind: "office" },
  { name: "Bac Ninh Office", region: "North", kind: "office" },
  { name: "Quang Ninh Office", region: "North", kind: "office" },
  { name: "Da Nang Sales Gallery", region: "Central", kind: "gallery" },
  { name: "Da Nang Office", region: "Central", kind: "office" },
  { name: "Nha Trang Office", region: "Central", kind: "office" },
  { name: "Thu Duc Office", region: "South", kind: "headquarters" },
  { name: "Sai Gon Office", region: "South", kind: "office" },
  { name: "Binh Duong Office", region: "South", kind: "office" },
  { name: "Long An Office", region: "South", kind: "office" },
  { name: "Phu Quoc Office", region: "South", kind: "office" },
];

export const officeSummary = {
  total: offices.length,
  provinces: 9,
  regions: 3,
};

export function officesByRegion(region: Office["region"]) {
  return offices.filter((o) => o.region === region);
}
