"use client";

import { useEffect, useState } from "react";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import PageTitle from "@/components/ui/PageTitle";
import SentimentCard from "@/components/ui/SentimentCard";
import SentimentChart from "@/components/charts/SentimentChart";

import { percentage } from "@/lib/helpers";

export default function AnalyticsPage() {
  const [stats, setStats] = useState({
    positive: 0,
    neutral: 0,
    negative: 0,
    total: 0,
    series: [60, 74, 65, 84, 58, 34, 61],
  });

  useEffect(() => {
    const stored = JSON.parse(
      localStorage.getItem("watergpt-analytics") || "[]"
    );

    let positive = 0;
    let neutral = 0;
    let negative = 0;

    const values = [];

    stored.forEach((item) => {
      if (item.sentiment === "positive") {
        positive += 1;
        values.push(80);
      } else if (item.sentiment === "negative") {
        negative += 1;
        values.push(25);
      } else {
        neutral += 1;
        values.push(55);
      }
    });

    const total = positive + neutral + negative;

    setStats({
      positive,
      neutral,
      negative,
      total,
      series:
        values.length > 0
          ? values.slice(-7)
          : [60, 74, 65, 84, 58, 34, 61],
    });
  }, []);

  return (
    <main className="page">
      <Navbar active="analytics" line />

      <PageTitle title="Sentiment." subtitle="How we understand you." />

      <section className="sentiment-grid">
        <SentimentCard
          label="POSITIVE"
          value={percentage(stats.positive, stats.total)}
        />

        <SentimentCard
          label="NEUTRAL"
          value={percentage(stats.neutral, stats.total)}
        />

        <SentimentCard
          label="NEGATIVE"
          value={percentage(stats.negative, stats.total)}
        />
      </section>

      <SentimentChart data={stats.series} />

      <section className="stats-section" style={{ marginTop: 60 }}>
        <div className="section-label">SESSION STATS</div>

        <div style={{ marginTop: 30 }}>
          <div className="stat-row">
            <span className="stat-label">TOTAL MESSAGES</span>
            <span className="stat-value">{stats.total}</span>
          </div>

          <div className="stat-row">
            <span className="stat-label">POSITIVE</span>
            <span className="stat-value">{stats.positive}</span>
          </div>

          <div className="stat-row">
            <span className="stat-label">NEUTRAL</span>
            <span className="stat-value">{stats.neutral}</span>
          </div>

          <div className="stat-row">
            <span className="stat-label">NEGATIVE</span>
            <span className="stat-value">{stats.negative}</span>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}