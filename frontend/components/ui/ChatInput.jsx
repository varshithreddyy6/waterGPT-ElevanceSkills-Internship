"use client";

import { useEffect, useRef, useState } from "react";

import { transcribeVoice } from "@/lib/api";
import { languageLabel } from "@/lib/helpers";

export default function ChatInput({
  placeholder = "Message...",
  onSubmit,
  loading = false,
  button = "SEND",
  language = "en",
  sticky = false,
  draftValue = "",
}) {
  const [value, setValue] = useState("");
  const [recording, setRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    if (draftValue) {
      setValue(draftValue);
    }
  }, [draftValue]);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!value.trim()) return;

    await onSubmit(value.trim());
    setValue("");
  }

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      audioChunksRef.current = [];

      const mediaRecorder = new MediaRecorder(stream);

      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());

        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });

        if (audioBlob.size === 0) {
          alert("No audio recorded. Please try again.");
          return;
        }

        setTranscribing(true);

        try {
          const data = await transcribeVoice(audioBlob);

          if (data?.text) {
            setValue(data.text);
          } else {
            alert("Could not transcribe audio. Please try again.");
          }
        } catch (error) {
          console.error(error);
          alert(
            "Voice transcription failed. Please check backend and Groq API access."
          );
        } finally {
          setTranscribing(false);
        }
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (error) {
      console.error(error);
      alert("Microphone access denied or unavailable.");
    }
  }

  function stopRecording() {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  }

  function handleVoiceClick() {
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  }

  return (
    <form
      className={`chat-shell ${sticky ? "sticky-chat-input" : ""}`}
      onSubmit={handleSubmit}
    >
      <div className="chat-input-row">
        <input
          className="chat-input"
          placeholder={transcribing ? "Transcribing voice..." : placeholder}
          value={value}
          onChange={(event) => setValue(event.target.value)}
          disabled={loading || transcribing}
        />

        <button
          className="send-button"
          type="submit"
          disabled={loading || transcribing}
        >
          {loading ? "..." : button}
        </button>
      </div>

      <div className="input-tools">
        <button
          type="button"
          className="tool-button"
          title="Attach file"
          onClick={() =>
            alert("File attachment is available in Knowledge and Vision pages.")
          }
        >
          ⌘
        </button>

        <button
          type="button"
          className={`tool-button ${recording ? "active" : ""}`}
          title={recording ? "Stop recording" : "Start voice input"}
          onClick={handleVoiceClick}
          disabled={transcribing}
        >
          {recording ? "●" : transcribing ? "…" : "♩"}
        </button>

        <button
          type="button"
          className="tool-button"
          title="Language"
          onClick={() => {
            window.location.href = "/language";
          }}
        >
          ◎
        </button>

        <span className="lang">{languageLabel(language)}</span>
      </div>

      {sticky && (
        <div className="sticky-input-footer">
          <div>waterGPT · Powered by Groq · Llama 3.3 70B</div>
          <div>
            Developed by Vinayak Varshith Reddy Vangeti ·{" "}
            varshithreddyy6@gmail.com
          </div>
        </div>
      )}
    </form>
  );
}