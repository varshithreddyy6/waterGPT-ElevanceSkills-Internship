export default function SentimentCard({ label, value }) {
  return (
    <div className="sentiment-card">
      <div className="sentiment-label">
        <span className="dot"></span>
        {label}
      </div>

      <div className="sentiment-value">{value}%</div>
    </div>
  );
}