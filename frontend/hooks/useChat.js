"use client";

import { useEffect, useState } from "react";

import { sendChatMessage } from "@/lib/api";
import { nowTime } from "@/lib/helpers";

function saveAnalytics(sentimentData) {
  if (typeof window === "undefined") return;

  const existing = JSON.parse(
    localStorage.getItem("watergpt-analytics") || "[]"
  );

  existing.push({
    sentiment: sentimentData?.sentiment || "neutral",
    score: sentimentData?.score || 0,
    time: new Date().toISOString(),
  });

  localStorage.setItem("watergpt-analytics", JSON.stringify(existing));
}

function chatStorageKey(mode) {
  return `watergpt-chat-${mode}`;
}

function downloadFile(filename, content) {
  const blob = new Blob([content], {
    type: "text/markdown;charset=utf-8",
  });

  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();

  URL.revokeObjectURL(url);
}

export default function useChat(mode, settings) {
  const [messages, setMessages] = useState([]);
  const [sentiment, setSentiment] = useState("neutral");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const saved = localStorage.getItem(chatStorageKey(mode));

    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch {
        setMessages([]);
      }
    }
  }, [mode]);

  useEffect(() => {
    if (typeof window === "undefined") return;

    localStorage.setItem(chatStorageKey(mode), JSON.stringify(messages));
  }, [messages, mode]);

  async function send(message) {
    if (!message.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: message,
        time: nowTime(),
      },
    ]);

    setLoading(true);

    try {
      const history = messages.slice(-8).map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      const data = await sendChatMessage({
        message,
        mode,
        targetLanguage: settings.language,
        responseLength: settings.responseLength,
        history,
      });

      const detectedSentiment = data.sentiment?.sentiment || "neutral";

      setSentiment(detectedSentiment);
      saveAnalytics(data.sentiment);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: data.answer,
          time: nowTime(),
          sources: data.sources || [],
          sentiment: data.sentiment,
          medicalEntities: data.medical_entities || {},
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: `Error: ${error.message}`,
          time: nowTime(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function trimMessagesFrom(index) {
    setMessages((prev) => prev.slice(0, index));
  }

  function clearChat() {
    setMessages([]);
    localStorage.removeItem(chatStorageKey(mode));
  }

  function exportChat() {
    if (!messages.length) {
      alert("No messages to export.");
      return;
    }

    const content = messages
      .map((msg) => {
        const who = msg.role === "user" ? "You" : "waterGPT";
        return `## ${who} (${msg.time})\n\n${msg.content}\n`;
      })
      .join("\n---\n\n");

    downloadFile(`watergpt-${mode}-chat.md`, content);
  }

  return {
    messages,
    sentiment,
    loading,
    send,
    trimMessagesFrom,
    clearChat,
    exportChat,
  };
}