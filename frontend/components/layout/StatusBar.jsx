export default function StatusBar({
  mode = "GENERAL CHAT",
  language = "ENGLISH",
  sentiment = "neutral",
  documents = null,
}) {
  return (
    <div className="status-bar">
      {documents !== null ? (
        <>
          MODE: {mode} · {Number(documents).toLocaleString()} DOCUMENTS
        </>
      ) : (
        <>
          MODE: {mode} · {language} ·{" "}
          <span className={`dot ${sentiment}`}></span>
          {sentiment.toUpperCase()}
        </>
      )}
    </div>
  );
}