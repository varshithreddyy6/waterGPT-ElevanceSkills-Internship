"use client";

import { marked } from "marked";

function renderMarkdown(content) {
  const html = marked.parse(content || "", {
    breaks: true,
    gfm: true,
  });

  return {
    __html: html,
  };
}

function showToast(message) {
  if (typeof window === "undefined") return;

  const oldToast = document.querySelector(".copy-toast");
  if (oldToast) oldToast.remove();

  const toast = document.createElement("div");
  toast.className = "copy-toast";
  toast.innerText = message;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 1400);
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text || "");
    showToast("Copied");
  } catch {
    alert("Copy failed.");
  }
}

async function shareText(text) {
  try {
    if (navigator.share) {
      await navigator.share({
        title: "waterGPT Response",
        text,
      });
    } else {
      await copyText(text);
      showToast("Copied to share");
    }
  } catch {
    // User cancelled share
  }
}

function saveFeedback(value, content) {
  const existing = JSON.parse(localStorage.getItem("watergpt-feedback") || "[]");

  existing.push({
    value,
    content,
    time: new Date().toISOString(),
  });

  localStorage.setItem("watergpt-feedback", JSON.stringify(existing));

  showToast(value === "up" ? "Marked helpful" : "Feedback saved");
}

function SourceViewer({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <details className="sources-inline-collapse">
      <summary className="sources-inline-summary">
        SOURCES ({sources.length}) · KNOWLEDGE BASE
      </summary>

      <div className="source-list">
        {sources.map((source, index) => {
          const metadata = source.metadata || {};
          const sourceName =
            metadata.source ||
            metadata.title ||
            metadata.paper_id ||
            metadata.type ||
            "Knowledge Base";

          return (
            <details key={index} className="source-details">
              <summary>
                Source {index + 1} · {String(sourceName)}
              </summary>

              <p>{source.text?.slice(0, 700)}...</p>

              {metadata && Object.keys(metadata).length > 0 && (
                <pre>{JSON.stringify(metadata, null, 2)}</pre>
              )}
            </details>
          );
        })}
      </div>
    </details>
  );
}

export default function ChatMessage({
  msg,
  index,
  showSources = true,
  onEdit,
}) {
  if (msg.role === "user") {
    return (
      <div className="msg">
        <div className="msg-head">
          <span>YOU</span>
          <span>{msg.time}</span>
        </div>

        <div className="msg-user">{msg.content}</div>

        <div className="message-actions icon-actions">
          <button
            type="button"
            onClick={() => copyText(msg.content)}
            title="Copy message"
            aria-label="Copy message"
          >
            ⧉
          </button>

          <button
            type="button"
            onClick={() => {
              if (onEdit) {
                onEdit(index, msg.content);
              }
            }}
            title="Edit message"
            aria-label="Edit message"
          >
            ✎
          </button>
        </div>

        <hr className="divider" />
      </div>
    );
  }

  return (
    <div className="msg">
      <div className="bot-name">waterGPT</div>

      <div
        className="bot-content markdown-content"
        dangerouslySetInnerHTML={renderMarkdown(msg.content)}
      />

      <div className="message-actions-row">
        <div className="message-actions icon-actions">
          <button
            type="button"
            onClick={() => copyText(msg.content)}
            title="Copy response"
            aria-label="Copy response"
          >
            ⧉
          </button>

          <button
            type="button"
            onClick={() => shareText(msg.content)}
            title="Share response"
            aria-label="Share response"
          >
            ↗
          </button>

          <button
            type="button"
            onClick={() => saveFeedback("up", msg.content)}
            title="Helpful"
            aria-label="Helpful"
          >
            ✓
          </button>

          <button
            type="button"
            onClick={() => saveFeedback("down", msg.content)}
            title="Not helpful"
            aria-label="Not helpful"
          >
            ×
          </button>
        </div>

        {showSources && <SourceViewer sources={msg.sources} />}
      </div>

      {msg.medicalEntities &&
        Object.values(msg.medicalEntities).some((items) => items.length > 0) && (
          <div className="sources">
            MEDICAL ENTITIES ·{" "}
            {Object.entries(msg.medicalEntities)
              .filter(([, items]) => items.length > 0)
              .map(([key, items]) => `${key}: ${items.join(", ")}`)
              .join(" · ")}
          </div>
        )}
    </div>
  );
}