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

export default function ChatPage() {
  const { settings } = useSettings();
  const chat = useChat("chat", settings);

  const [draftValue, setDraftValue] = useState("");

  const hasMessages = chat.messages.length > 0;

  function handleEdit(index, content) {
    chat.trimMessagesFrom(index);
    setDraftValue(content);
  }

  return (
    <main className="page with-fixed-input">
      <StatusBar
        mode="GENERAL CHAT"
        language="ENGLISH"
        sentiment={chat.sentiment}
      />

      <Navbar active="chat" />

      {!hasMessages && (
        <>
          <PageTitle title="Chat." subtitle="Ask anything." />

          <PromptCards
            prompts={[
              "Explain artificial intelligence in simple terms.",
              "Summarize the benefits of exercise.",
              "Translate a sentence into Hindi.",
              "Give me a study plan for one week.",
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
        placeholder="Message..."
        onSubmit={chat.send}
        loading={chat.loading}
        language={settings.language}
        sticky
        draftValue={draftValue}
      />
    </main>
  );
}