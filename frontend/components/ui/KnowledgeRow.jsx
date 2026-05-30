export default function KnowledgeRow({ num, name, active, onClick }) {
  return (
    <div className="knowledge-row" onClick={onClick}>
      <div className="row-left">
        <span className="row-num">{num}</span>
        <span className="row-slash">/</span>
        <span className="row-name">{name}</span>
      </div>

      <span className="row-arrow">{active ? "●" : "→"}</span>
    </div>
  );
}