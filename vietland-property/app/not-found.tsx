import Link from "next/link";

export default function NotFound() {
  return (
    <section className="container-page flex flex-col items-center justify-center py-32 text-center">
      <p className="font-mono text-[13px] text-gold-dark">404</p>
      <h1 className="mt-3 font-display text-3xl font-semibold text-ink">Page not found</h1>
      <p className="mt-2 text-[14px] text-ink/55">The page you&rsquo;re looking for doesn&rsquo;t exist.</p>
      <Link
        href="/"
        className="mt-6 rounded-full bg-lacquer px-6 py-3 text-[13.5px] font-semibold text-white hover:bg-lacquer-dark"
      >
        Back to home
      </Link>
    </section>
  );
}
