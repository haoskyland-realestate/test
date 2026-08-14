import Link from "next/link";
import { ArrowRight } from "lucide-react";
import Hero from "../components/Hero";
import ProjectCard from "../components/ProjectCard";
import TrustSection from "../components/TrustSection";
import ProcessSteps from "../components/ProcessSteps";
import CtaBanner from "../components/CtaBanner";
import { projects } from "../data/projects";

export default function HomePage() {
  const featured = projects.slice(0, 3);

  return (
    <>
      <Hero />

      <section className="border-t border-ink/8 bg-paper py-16 md:py-20">
        <div className="container-page">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="eyebrow text-lacquer">Featured listings</p>
              <h2 className="mt-3 font-display text-[2rem] font-semibold text-ink sm:text-[2.3rem]">
                Verified projects, ready to view.
              </h2>
            </div>
            <Link
              href="/projects"
              className="flex items-center gap-1.5 text-[13.5px] font-semibold text-ink/70 hover:text-lacquer"
            >
              View all projects <ArrowRight size={15} />
            </Link>
          </div>

          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {featured.map((p) => (
              <ProjectCard key={p.slug} project={p} />
            ))}
          </div>
        </div>
      </section>

      <TrustSection />
      <ProcessSteps />
      <CtaBanner />
    </>
  );
}
