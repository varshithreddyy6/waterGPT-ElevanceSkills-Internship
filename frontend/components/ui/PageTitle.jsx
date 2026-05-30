export default function PageTitle({ title, subtitle }) {
  return (
    <section className="page-heading">
      <div className="page-title">{title}</div>
      <div className="page-subtitle">{subtitle}</div>
    </section>
  );
}