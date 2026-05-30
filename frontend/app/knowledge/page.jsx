"use client";

import { useState } from "react";

import Navbar from "@/components/layout/Navbar";
import StatusBar from "@/components/layout/StatusBar";
import Footer from "@/components/layout/Footer";
import PageTitle from "@/components/ui/PageTitle";
import KnowledgeRow from "@/components/ui/KnowledgeRow";

import useKnowledge from "@/hooks/useKnowledge";

import {
  addKnowledgeUrl,
  addKnowledgeText,
  addKnowledgeFile,
  clearKnowledge,
} from "@/lib/api";

export default function KnowledgePage() {
  const { stats, refresh } = useKnowledge();

  const [mode, setMode] = useState("url");
  const [value, setValue] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();

    if (!value.trim()) return;

    setLoading(true);

    try {
      if (mode === "url") {
        await addKnowledgeUrl(value);
      }

      if (mode === "text") {
        await addKnowledgeText(value);
      }

      setValue("");
      await refresh();
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleFile(event) {
    const file = event.target.files?.[0];

    if (!file) return;

    setLoading(true);

    try {
      await addKnowledgeFile(file);
      await refresh();
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleClear() {
    if (!confirm("Clear the knowledge base?")) return;

    await clearKnowledge();
    await refresh();
  }

  return (
    <main className="page">
      <StatusBar mode="KNOWLEDGE BASE" documents={stats.total} />

      <Navbar active="knowledge" />

      <PageTitle title="Knowledge." subtitle="Always evolving." />

      <section className="knowledge-section">
        <div className="knowledge-grid">
          <div>
            <div className="section-label">ADD SOURCE</div>

            <KnowledgeRow
              num="01"
              name="FROM URL"
              active={mode === "url"}
              onClick={() => setMode("url")}
            />

            <KnowledgeRow
              num="02"
              name="FROM TEXT"
              active={mode === "text"}
              onClick={() => setMode("text")}
            />

            <KnowledgeRow
              num="03"
              name="FROM FILE"
              active={mode === "file"}
              onClick={() => setMode("file")}
            />
          </div>

          <form className="kb-form" onSubmit={submit}>
            {mode === "url" && (
              <>
                <input
                  placeholder="Paste a URL to learn from..."
                  value={value}
                  onChange={(event) => setValue(event.target.value)}
                />

                <button disabled={loading}>
                  {loading ? "ADDING..." : "FETCH AND ADD"}
                </button>
              </>
            )}

            {mode === "text" && (
              <>
                <textarea
                  placeholder="Paste text content..."
                  value={value}
                  onChange={(event) => setValue(event.target.value)}
                />

                <button disabled={loading}>
                  {loading ? "ADDING..." : "ADD TEXT"}
                </button>
              </>
            )}

            {mode === "file" && (
              <input
                type="file"
                accept=".txt,.md,.csv,.pdf"
                onChange={handleFile}
              />
            )}
          </form>
        </div>

        <div className="stats-section" style={{ padding: 0, marginTop: 60 }}>
          <div className="section-label">LIBRARY STATS</div>

          <div style={{ marginTop: 30 }}>
            <div className="stat-row">
              <span className="stat-label">MEDICAL Q&AS</span>
              <span className="stat-value">
                {stats.medical?.toLocaleString()}
              </span>
            </div>

            <div className="stat-row">
              <span className="stat-label">RESEARCH PAPERS</span>
              <span className="stat-value">
                {stats.research?.toLocaleString()}
              </span>
            </div>

            <div className="stat-row">
              <span className="stat-label">USER DOCUMENTS</span>
              <span className="stat-value">
                {stats.user_docs?.toLocaleString()}
              </span>
            </div>

            <div className="stat-line"></div>

            <div className="stat-row">
              <span className="stat-label">TOTAL</span>
              <span className="stat-total">{stats.total?.toLocaleString()}</span>
            </div>

            <button
              className="send-button"
              style={{ height: 56, width: 280, marginTop: 24 }}
              onClick={handleClear}
              type="button"
            >
              CLEAR KNOWLEDGE
            </button>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}