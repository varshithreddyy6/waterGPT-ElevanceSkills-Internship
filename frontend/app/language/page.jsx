"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import PageTitle from "@/components/ui/PageTitle";

import useSettings from "@/hooks/useSettings";
import { LANGUAGES } from "@/lib/languages";

export default function LanguagePage() {
  const { settings, update } = useSettings();

  return (
    <main className="page">
      <Navbar active="settings" />

      <PageTitle title="Language." subtitle="Choose yours." />

      <section className="language-section">
        <div className="language-grid">
          {LANGUAGES.map(([code, name]) => (
            <button
              key={code}
              className={`language-btn ${
                settings.language === code ? "active" : ""
              }`}
              onClick={() => update({ language: code })}
            >
              {settings.language === code ? "● " : ""}
              {name}
            </button>
          ))}
        </div>

        <div className="auto-detect">AUTO-DETECT</div>
      </section>

      <Footer />
    </main>
  );
}