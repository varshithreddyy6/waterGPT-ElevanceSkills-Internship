"use client";

import { useEffect, useState } from "react";

import { getKnowledgeStats } from "@/lib/api";

export default function useKnowledge() {
  const [stats, setStats] = useState({
    total: 0,
    medical: 0,
    research: 0,
    user_docs: 0,
  });

  async function refresh() {
    const data = await getKnowledgeStats();
    setStats(data);
  }

  useEffect(() => {
    refresh().catch(() => {});
  }, []);

  return {
    stats,
    refresh,
  };
}