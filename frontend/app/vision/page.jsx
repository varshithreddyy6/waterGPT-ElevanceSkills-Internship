"use client";

import { useState } from "react";

import Navbar from "@/components/layout/Navbar";
import StatusBar from "@/components/layout/StatusBar";
import PageTitle from "@/components/ui/PageTitle";
import UploadZone from "@/components/ui/UploadZone";
import ChatInput from "@/components/ui/ChatInput";
import ChatMessage from "@/components/ui/ChatMessage";

import useSettings from "@/hooks/useSettings";
import { sendVisionQuestion, generateImage, editImage } from "@/lib/api";
import { nowTime } from "@/lib/helpers";

const MODES = [
  { id: "understand", label: "UNDERSTAND", hint: "Upload an image, ask a question about it." },
  { id: "generate", label: "GENERATE", hint: "Describe an image you want Gemini to create." },
  { id: "edit", label: "EDIT", hint: "Upload an image and describe how to transform it." },
];

export default function VisionPage() {
  const { settings } = useSettings();

  const [mode, setMode] = useState("understand");
  const [image, setImage] = useState(null);
  const [imageName, setImageName] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const hasMessages = messages.length > 0;
  const requiresImage = mode === "understand" || mode === "edit";

  function switchMode(nextMode) {
    setMode(nextMode);
    setMessages([]);
  }

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

    const userMessage = { role: "user", content: question, time: nowTime() };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const data = await sendVisionQuestion({
        image,
        question,
        targetLanguage: settings.language,
        history: buildVisionHistory(),
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: data.answer || "No response received.",
          time: nowTime(),
          sources: [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: `Error: ${error.message}. Please make sure the FastAPI backend is running and GEMINI_API_KEY is set.`,
          time: nowTime(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function runGenerate(prompt) {
    const userMessage = { role: "user", content: prompt, time: nowTime() };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const data = await generateImage({
        prompt,
        targetLanguage: settings.language,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: data.answer || "Here is the generated image.",
          time: nowTime(),
          imageUrl: data.image_url,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: `Error: ${error.message}. Please make sure GEMINI_API_KEY is configured in backend/.env.`,
          time: nowTime(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function runEdit(prompt) {
    if (!image) {
      alert("Please upload an image first.");
      return;
    }

    const userMessage = { role: "user", content: prompt, time: nowTime() };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const data = await editImage({
        image,
        prompt,
        targetLanguage: settings.language,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: data.answer || "Here is your edited image.",
          time: nowTime(),
          imageUrl: data.image_url,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: `Error: ${error.message}. Please make sure GEMINI_API_KEY is configured in backend/.env.`,
          time: nowTime(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(value) {
    if (mode === "understand") return askVision(value);
    if (mode === "generate") return runGenerate(value);
    return runEdit(value);
  }

  const activeMode = MODES.find((m) => m.id === mode);

  return (
    <main className="page with-fixed-input">
      <StatusBar mode="VISION AI · GEMINI" language="ENGLISH" sentiment="neutral" />

      <Navbar active="vision" />

      {!hasMessages && <PageTitle title="Vision." subtitle="See, understand, and create." />}

      <section className="vision-section">
        <div className="mode-toggle-row">
          {MODES.map((m) => (
            <button
              key={m.id}
              type="button"
              className={`mode-toggle-btn ${mode === m.id ? "active" : ""}`}
              onClick={() => switchMode(m.id)}
            >
              {m.label}
            </button>
          ))}
        </div>

        <div className="selected-file" style={{ marginBottom: 16 }}>
          {activeMode.hint}
        </div>

        {requiresImage && (
          <>
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
          </>
        )}
      </section>

      <section className={`messages ${hasMessages ? "messages-active" : ""}`}>
        {messages.map((message, index) => (
          <div key={index}>
            <ChatMessage index={index} msg={message} showSources={false} />

            {message.imageUrl && (
              <div className="generated-image-wrap">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={message.imageUrl}
                  alt="Gemini generated"
                  className="generated-image"
                />
              </div>
            )}
          </div>
        ))}

        {messages.length > 0 && (
          <div className="sources">
            MODEL · GOOGLE GEMINI (
            {mode === "understand" ? "gemini-2.5-flash" : "gemini-2.5-flash-image"})
          </div>
        )}
      </section>

      <ChatInput
        placeholder={
          mode === "understand"
            ? "What would you like to know about this image?"
            : mode === "generate"
            ? "Describe the image you want Gemini to generate..."
            : "Describe how you want this image edited..."
        }
        onSubmit={handleSubmit}
        loading={loading}
        button="↵"
        language={settings.language}
        sticky
      />
    </main>
  );
}