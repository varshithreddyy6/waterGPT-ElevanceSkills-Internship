"use client";

import { useState } from "react";

import Navbar from "@/components/layout/Navbar";
import StatusBar from "@/components/layout/StatusBar";
import PageTitle from "@/components/ui/PageTitle";
import ChatInput from "@/components/ui/ChatInput";
import ChatMessage from "@/components/ui/ChatMessage";
import PromptCards from "@/components/ui/PromptCards";

import useSettings from "@/hooks/useSettings";
import useChat from "@/hooks/useChat";

export default function MedicalPage() {
  const { settings } = useSettings();
  const chat = useChat("medical", settings);

  const [draftValue, setDraftValue] = useState("");

  const hasMessages = chat.messages.length > 0;

  function handleEdit(index, content) {
    chat.trimMessagesFrom(index);
    setDraftValue(content);
  }

  return (
    <main className="page with-fixed-input">
      <StatusBar
        mode="MEDICAL Q&A"
        language="ENGLISH"
        sentiment={chat.sentiment}
      />

      <Navbar active="medical" />

      {!hasMessages && (
        <>
          <PageTitle title="Medical." subtitle="Evidence-based answers." />

          <PromptCards
            prompts={[
              "What are the symptoms of diabetes?",
              "What causes fever?",
              "How is asthma treated?",
              "What are common symptoms of anemia?",
            ]}
            onPromptClick={chat.send}
          />
        </>
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
        placeholder="Ask a medical question..."
        onSubmit={chat.send}
        loading={chat.loading}
        language={settings.language}
        sticky
        draftValue={draftValue}
      />
    </main>
  );
}