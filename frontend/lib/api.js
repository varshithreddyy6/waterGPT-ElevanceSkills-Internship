function getApiBase() {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;

    // Mobile/LAN mode:
    // If frontend is opened as http://192.168.x.x:3000,
    // backend must be called as http://192.168.x.x:8000
    if (hostname !== "localhost" && hostname !== "127.0.0.1") {
      return `${protocol}//${hostname}:8000`;
    }
  }

  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

async function parseResponse(res) {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "API request failed");
  }

  return res.json();
}

export function getCurrentApiBase() {
  return getApiBase();
}

export async function sendChatMessage({
  message,
  mode = "chat",
  targetLanguage = "en",
  responseLength = "medium",
  history = [],
}) {
  const API_BASE = getApiBase();

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      mode,
      target_language: targetLanguage,
      response_length: responseLength,
      history,
    }),
  });

  return parseResponse(res);
}

export async function getKnowledgeStats() {
  const API_BASE = getApiBase();

  const res = await fetch(`${API_BASE}/knowledge/stats`, {
    cache: "no-store",
  });

  return parseResponse(res);
}

export async function addKnowledgeUrl(url) {
  const API_BASE = getApiBase();

  const res = await fetch(`${API_BASE}/knowledge/url`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  });

  return parseResponse(res);
}

export async function addKnowledgeText(text) {
  const API_BASE = getApiBase();

  const res = await fetch(`${API_BASE}/knowledge/text`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  return parseResponse(res);
}

export async function addKnowledgeFile(file) {
  const API_BASE = getApiBase();

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/knowledge/file`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(res);
}

export async function clearKnowledge() {
  const API_BASE = getApiBase();

  const res = await fetch(`${API_BASE}/knowledge/clear`, {
    method: "DELETE",
  });

  return parseResponse(res);
}

export async function sendVisionQuestion({
  image,
  question,
  targetLanguage = "en",
  history = "",
}) {
  const API_BASE = getApiBase();

  const formData = new FormData();

  formData.append("image", image);
  formData.append("question", question);
  formData.append("target_language", targetLanguage);
  formData.append("history", history);

  const res = await fetch(`${API_BASE}/vision`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(res);
}

export async function transcribeVoice(audioBlob) {
  const API_BASE = getApiBase();

  const formData = new FormData();
  formData.append("file", audioBlob, "voice.webm");

  const res = await fetch(`${API_BASE}/voice/transcribe`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(res);
}