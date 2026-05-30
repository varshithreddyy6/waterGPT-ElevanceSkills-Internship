"use client";

import { useRouter } from "next/navigation";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import PageTitle from "@/components/ui/PageTitle";
import SettingsRow from "@/components/ui/SettingsRow";

import useSettings from "@/hooks/useSettings";

export default function SettingsPage() {
  const router = useRouter();
  const { settings, update } = useSettings();

  const lengths = ["short", "medium", "long"];

  function cycleResponseLength() {
    const currentIndex = lengths.indexOf(settings.responseLength);
    const next = lengths[(currentIndex + 1) % lengths.length];

    update({
      responseLength: next,
    });
  }

  return (
    <main className="page">
      <Navbar active="settings" line />

      <PageTitle title="Settings." subtitle="Make it yours." />

      <section className="settings-list">
        <SettingsRow
          num="01"
          name="LANGUAGE"
          value={settings.language.toUpperCase()}
          onClick={() => router.push("/language")}
        />

        <SettingsRow
          num="02"
          name="RESPONSE LENGTH"
          value={settings.responseLength.toUpperCase()}
          onClick={cycleResponseLength}
        />

        <SettingsRow
          num="03"
          name="SENTIMENT ANALYSIS"
          value={settings.showSentiment ? "ON" : "OFF"}
          onClick={() =>
            update({
              showSentiment: !settings.showSentiment,
            })
          }
        />

        <SettingsRow
          num="04"
          name="SOURCE CITATIONS"
          value={settings.showSources ? "ON" : "OFF"}
          onClick={() =>
            update({
              showSources: !settings.showSources,
            })
          }
        />

        <SettingsRow
          num="05"
          name="VOICE INPUT"
          value={settings.voiceInput ? "ON" : "OFF"}
          onClick={() =>
            update({
              voiceInput: !settings.voiceInput,
            })
          }
        />

        <SettingsRow num="06" name="THEME" value="DARK" />

        <SettingsRow
          num="07"
          name="CLEAR ALL CONVERSATIONS"
          value=""
          onClick={() => {
            localStorage.removeItem("watergpt-messages");
            localStorage.removeItem("watergpt-analytics");
            alert("Conversations and analytics cleared.");
          }}
        />
      </section>

      <Footer />
    </main>
  );
}