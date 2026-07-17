"use client";

import { useEffect, useState } from "react";

import Navbar from "@/components/layout/Navbar";
import StatusBar from "@/components/layout/StatusBar";
import PageTitle from "@/components/ui/PageTitle";
import ChatInput from "@/components/ui/ChatInput";
import ChatMessage from "@/components/ui/ChatMessage";
import PromptCards from "@/components/ui/PromptCards";
import CategoryBarChart from "@/components/charts/CategoryBarChart";
import KeywordBarChart from "@/components/charts/KeywordBarChart";
import ConceptScatterChart from "@/components/charts/ConceptScatterChart";

import useSettings from "@/hooks/useSettings";
import useChat from "@/hooks/useChat";
import {
  searchPapers,
  summarizePaper,
  getCategoryDistribution,
  getTopKeywords,
  getConceptMap,
} from "@/lib/api";

const TABS = [
  { id: "chat", label: "ASK" },
  { id: "search", label: "SEARCH PAPERS" },
  { id: "visualize", label: "VISUALIZE" },
];

function PaperCard({ paper }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(false);

  async function loadSummary() {
    if (summary) {
      setExpanded((prev) => !prev);
      return;
    }

    setLoading(true);

    try {
      const data = await summarizePaper(paper.id, 3);
      setSummary(data);
      setExpanded(true);
    } catch (error) {
      setSummary({ summary: `Error: ${error.message}`, keywords: [] });
      setExpanded(true);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="paper-card">
      <div className="paper-card-title">{paper.title}</div>

      <div className="paper-card-meta">
        {paper.primary_category} · {paper.authors?.split(",").slice(0, 3).join(", ")}
        {paper.authors?.split(",").length > 3 ? " et al." : ""}
      </div>

      <div className="paper-card-abstract">
        {paper.abstract?.slice(0, 260)}
        {paper.abstract?.length > 260 ? "…" : ""}
      </div>

      <div className="paper-card-actions">
        <button onClick={loadSummary} disabled={loading} type="button">
          {loading ? "Summarizing..." : expanded ? "Hide Summary" : "Summarize + Keywords"}
        </button>

        {paper.link && (
          <a href={paper.link} target="_blank" rel="noreferrer">
            <button type="button">View on arXiv</button>
          </a>
        )}
      </div>

      {expanded && summary && (
        <div className="paper-summary-box">
          <strong>Extractive Summary (TextRank):</strong>
          <p style={{ marginTop: 8, color: "#dddddd", fontSize: 14, lineHeight: 1.6 }}>
            {summary.summary}
          </p>

          {summary.keywords?.length > 0 && (
            <>
              <strong>Keywords (TF-IDF):</strong>
              <div className="keyword-chip-row">
                {summary.keywords.map((kw) => (
                  <span className="keyword-chip" key={kw}>
                    {kw}
                  </span>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

function SearchTab() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [author, setAuthor] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function runSearch(event) {
    event?.preventDefault();
    setLoading(true);

    try {
      const data = await searchPapers({ query, category, author, limit: 20 });
      setResults(data.results || []);
      setSearched(true);
    } catch (error) {
      alert(`Search failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section style={{ padding: "0 20px" }}>
      <form className="research-search-form" onSubmit={runSearch}>
        <input
          placeholder="Search title/abstract (e.g. transformers, RAG)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <input
          placeholder="Category (e.g. cs.AI)"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />

        <input
          placeholder="Author name"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {searched && results.length === 0 && (
        <div className="selected-file">No papers matched your search.</div>
      )}

      {results.map((paper) => (
        <PaperCard key={paper.id} paper={paper} />
      ))}
    </section>
  );
}

function VisualizeTab() {
  const [categories, setCategories] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [conceptMap, setConceptMap] = useState({ points: [], categories: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [catData, keywordData, mapData] = await Promise.all([
          getCategoryDistribution(),
          getTopKeywords(15),
          getConceptMap(150),
        ]);

        setCategories(catData.data || []);
        setKeywords(keywordData.data || []);
        setConceptMap(mapData);
      } catch (error) {
        console.error("Failed to load visualization data:", error);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  if (loading) {
    return <div style={{ padding: "0 20px" }}>Loading visualizations...</div>;
  }

  return (
    <section style={{ padding: "0 20px" }}>
      <div className="viz-grid">
        <div>
          <div className="section-label" style={{ marginBottom: 16 }}>
            PAPERS PER CATEGORY
          </div>
          <CategoryBarChart data={categories} />
        </div>

        <div>
          <div className="section-label" style={{ marginBottom: 16 }}>
            TOP CORPUS KEYWORDS (TF-IDF)
          </div>
          <KeywordBarChart data={keywords} />
        </div>
      </div>

      <div className="section-label" style={{ marginBottom: 16 }}>
        CONCEPT MAP (TF-IDF + SVD PROJECTION)
      </div>
      <ConceptScatterChart points={conceptMap.points} categories={conceptMap.categories} />
    </section>
  );
}

export default function ResearchPage() {
  const { settings } = useSettings();
  const chat = useChat("research", settings);

  const [tab, setTab] = useState("chat");
  const [draftValue, setDraftValue] = useState("");

  const hasMessages = chat.messages.length > 0;

  function handleEdit(index, content) {
    chat.trimMessagesFrom(index);
    setDraftValue(content);
  }

  return (
    <main className="page with-fixed-input">
      <StatusBar
        mode="SCIENTIFIC RESEARCH"
        language="ENGLISH"
        sentiment={chat.sentiment}
      />

      <Navbar active="research" />

      <PageTitle title="Research." subtitle="Explore the frontier." />

      <div className="research-tabs" style={{ padding: "0 20px" }}>
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            className={`mode-toggle-btn ${tab === t.id ? "active" : ""}`}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "chat" && (
        <>
          {!hasMessages && (
            <PromptCards
              prompts={[
                "Explain retrieval augmented generation.",
                "What is FAISS vector search?",
                "Summarize transformer models in NLP.",
                "What are recent trends in computer vision?",
              ]}
              onPromptClick={chat.send}
            />
          )}

          {hasMessages && (
            <div className="chat-top-actions">
              <button onClick={chat.exportChat}>EXPORT CHAT</button>
              <button onClick={chat.clearChat}>CLEAR CHAT</button>
            </div>
          )}

          <section className={`messages ${hasMessages ? "messages-active" : ""}`}>
            {chat.messages.map((message, index) => (
              <ChatMessage
                key={index}
                index={index}
                msg={message}
                showSources={settings.showSources}
                onEdit={handleEdit}
              />
            ))}
          </section>

          <ChatInput
            placeholder="Search papers or ask a research question..."
            onSubmit={chat.send}
            loading={chat.loading}
            language={settings.language}
            sticky
            draftValue={draftValue}
          />
        </>
      )}

      {tab === "search" && <SearchTab />}

      {tab === "visualize" && <VisualizeTab />}
    </main>
  );
}