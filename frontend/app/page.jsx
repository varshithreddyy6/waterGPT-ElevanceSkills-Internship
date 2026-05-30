import Link from "next/link";

import AnnouncementBar from "@/components/layout/AnnouncementBar";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";

export default function HomePage() {
  return (
    <main className="page">
      <AnnouncementBar />

      <Navbar active="home" />

      <section className="hero">
        <div className="hero-title">
          Intelligence.
          <br />
          The foundation of
          <br />
          every answer.
        </div>

        <p className="hero-text">
          waterGPT combines advanced reasoning, medical insight,
          <br />
          and visionary AI to deliver answers that matter.
          <br />
          Built for depth. Designed for clarity. Trusted by experts.
        </p>

        <Link href="/chat" className="cta">
          BEGIN CHAT
        </Link>
      </section>

      <Footer big />
    </main>
  );
}