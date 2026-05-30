"use client";

import { useState } from "react";

import Navbar from "@/components/layout/Navbar";
import StatusBar from "@/components/layout/StatusBar";
import PageTitle from "@/components/ui/PageTitle";
import UploadZone from "@/components/ui/UploadZone";
import ChatInput from "@/components/ui/ChatInput";
import ChatMessage from "@/components/ui/ChatMessage";

import useSettings from "@/hooks/useSettings";
import { sendVisionQuestion } from "@/lib/api";
import { nowTime } from "@/lib/helpers";

export default function VisionPage() {
  const { settings } = useSettings();

  const [image, setImage] = useState(null);
  const [imageName, setImageName] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const hasMessages = messages.length > 0;

  function handleImageChange(event) {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      setImage(null);
      setImageName("");
      setMessages([]);
      return;
    }

    const allowedTypes = ["image/png", "image/jpeg", "image/webp"];

    if (!allowedTypes.includes(selectedFile.type)) {
      alert("Please upload PNG, JPG, JPEG, or WEBP images only.");
      return;
    }

    setImage(selectedFile);
    setImageName(selectedFile.name);
    setMessages([]);
  }

  function buildVisionHistory() {
    return messages
      .slice(-6)
      .map((msg) => {
        const who = msg.role === "user" ? "User" : "waterGPT";
        return `${who}: ${msg.content}`;
      })
      .join("\n");
  }

  async function askVision(question) {
    if (!image) {
      alert("Please upload an image first.");
      return;
    }

    const userMessage = {
      role: "user",
      content: question,
      time: nowTime(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const data = await sendVisionQuestion({
        image,
        question,
        targetLanguage: settings.language,
        history: buildVisionHistory(),
      });

      const botMessage = {
        role: "bot",
        content: data.answer || "No response received.",
        time: nowTime(),
        sources: [],
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const botMessage = {
        role: "bot",
        content: `Error: ${error.message}. Please make sure the FastAPI backend is running.`,
        time: nowTime(),
        sources: [],
      };

      setMessages((prev) => [...prev, botMessage]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page with-fixed-input">
      <StatusBar mode="VISION AI" language="ENGLISH" sentiment="neutral" />

      <Navbar active="vision" />

      {!hasMessages && <PageTitle title="Vision." subtitle="See and understand." />}

      <section className="vision-section">
        <label className="upload-label">
          <UploadZone />

          <input
            className="hidden-file-input"
            type="file"
            accept="image/png,image/jpeg,image/webp"
            onChange={handleImageChange}
          />
        </label>

        {imageName && (
          <div className="selected-file">SELECTED IMAGE · {imageName}</div>
        )}
      </section>

      <section className={`messages ${hasMessages ? "messages-active" : ""}`}>
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            index={index}
            msg={message}
            showSources={false}
          />
        ))}

        {messages.length > 0 && (
          <div className="sources">MODEL · GROQ VISION</div>
        )}
      </section>

      <ChatInput
        placeholder="What would you like to know about this image?"
        onSubmit={askVision}
        loading={loading}
        button="↵"
        language={settings.language}
        sticky
      />
    </main>
  );
}