"use client";

import { useEffect, useState } from "react";

const DEFAULT_SETTINGS = {
  language: "en",
  responseLength: "medium",
  showSentiment: true,
  showSources: true,
  voiceInput: false,
};

export default function useSettings() {
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);

  useEffect(() => {
    const saved = localStorage.getItem("watergpt-settings");

    if (saved) {
      setSettings({
        ...DEFAULT_SETTINGS,
        ...JSON.parse(saved),
      });
    }
  }, []);

  function update(patch) {
    setSettings((prev) => {
      const next = {
        ...prev,
        ...patch,
      };

      localStorage.setItem("watergpt-settings", JSON.stringify(next));

      return next;
    });
  }

  return {
    settings,
    update,
  };
}