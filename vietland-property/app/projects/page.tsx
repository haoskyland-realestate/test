import { Suspense } from "react";
import type { Metadata } from "next";
import ProjectsExplorer from "../../components/ProjectsExplorer";

export const metadata: Metadata = {
  title: "Projects — Vietland",
};

export default function ProjectsPage() {
  return (
    <Suspense fallback={null}>
      <ProjectsExplorer />
    </Suspense>
  );
}
