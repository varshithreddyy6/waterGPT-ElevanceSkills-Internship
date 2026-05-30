"use client";

export default function PromptCards({ prompts = [], onPromptClick }) {
  if (!prompts.length) return null;

  return (
    <div className="prompt-card-grid">
      {prompts.map((prompt, index) => (
        <button
          key={index}
          className="prompt-card"
          type="button"
          onClick={() => onPromptClick(prompt)}
        >
          <span>{String(index + 1).padStart(2, "0")}</span>
          <strong>{prompt}</strong>
        </button>
      ))}
    </div>
  );
}