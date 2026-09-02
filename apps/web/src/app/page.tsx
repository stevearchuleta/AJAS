const prohibitedActions = [
  "Employer login",
  "Employer-form entry",
  "Employer file upload",
  "Attestation or consent",
  "Employer communication",
  "Application submission",
] as const;

export default function HomePage() {
  return (
    <main>
      <section className="card" aria-labelledby="page-title">
        <p className="eyebrow">Stage-0B scaffold</p>
        <h1 id="page-title">AJAS Personal</h1>
        <p className="summary">
          AJAS prepares truthful, evidence-grounded application packets. Autonomous authority ends
          at <code>READY_FOR_REVIEW</code>.
        </p>

        <h2>Human-only employer actions</h2>
        <ul>
          {prohibitedActions.map((action) => (
            <li key={action}>{action}</li>
          ))}
        </ul>

        <p className="status" role="status">
          Live sources, personal data, external accounts, and employer integrations are disabled.
        </p>
      </section>
    </main>
  );
}
