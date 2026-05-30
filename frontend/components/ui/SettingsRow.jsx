export default function SettingsRow({ num, name, value, onClick }) {
  return (
    <div className="settings-row" onClick={onClick}>
      <div className="row-left">
        <span className="row-num">{num}</span>
        <span className="row-slash">/</span>
        <span className="row-name">{name}</span>
      </div>

      <div className="row-right">
        <span className="row-value">{value}</span>
        <span className="row-arrow">→</span>
      </div>
    </div>
  );
}