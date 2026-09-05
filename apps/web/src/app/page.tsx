const capabilities = [
  {
    icon: "discover",
    title: "Discover",
    description: "Find relevant jobs based on approved goals.",
  },
  {
    icon: "analyze",
    title: "Analyze",
    description: "Extract and understand job requirements.",
  },
  {
    icon: "data",
    title: "Use Your Data",
    description: "Work from approved evidence and Google Drive content.",
  },
  {
    icon: "prepare",
    title: "Prepare",
    description: "Generate resumes, cover letters, and application answers.",
  },
  {
    icon: "verify",
    title: "Verify",
    description: "Check accuracy, consistency, evidence, and compliance.",
  },
  {
    icon: "submit",
    title: "You Submit",
    description: "Review and submit only when the packet is ready.",
  },
] as const;

const workflowSteps = [
  "Discover Jobs",
  "Extract Requirements",
  "Retrieve Facts",
  "Match & Analyze",
  "Draft Content",
  "Verify & Check",
  "Assemble Packet",
  "You Review",
] as const;

const trustCards = [
  {
    icon: "people",
    title: "For Job Seekers",
    body: "A serious system for organizing a job search around truthful evidence, clear decisions, and human control.",
    link: "Learn more",
    href: "#workflow",
  },
  {
    icon: "shield",
    title: "Trust & Safety",
    body: "No invented applicant facts, no employer outreach, and no automatic submission. Every output stays reviewable.",
    link: "Our commitments",
    href: "#trust",
  },
  {
    icon: "growth",
    title: "Guided by You",
    body: "Agentic AI handles preparation inside explicit boundaries while final judgment and final submission remain human.",
    link: "See the vision",
    href: "#about",
  },
] as const;

type CapabilityIconName = (typeof capabilities)[number]["icon"];
type TrustIconName = (typeof trustCards)[number]["icon"];

function BrandMark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <svg viewBox="0 0 64 42" focusable="false">
        <path d="M3 37 22 8l8 12L39 3l22 34H3Z" />
        <path d="m19 32 6-9 5 7 9-15 12 17H19Z" className="brand-mark-snow" />
      </svg>
    </span>
  );
}

function CapabilityIcon({ name }: Readonly<{ name: CapabilityIconName }>) {
  if (name === "discover") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="21" cy="21" r="11" />
        <path d="m29 29 11 11" />
      </svg>
    );
  }

  if (name === "analyze") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M13 7h17l7 7v27H13V7Z" />
        <path d="M30 7v8h8M18 23h14M18 30h14" />
      </svg>
    );
  }

  if (name === "data") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <ellipse cx="24" cy="11" rx="13" ry="6" />
        <path d="M11 11v12c0 3 6 6 13 6s13-3 13-6V11M11 23v12c0 3 6 6 13 6s13-3 13-6V23" />
      </svg>
    );
  }

  if (name === "prepare") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="24" cy="24" r="7" />
        <path d="M24 5v7M24 36v7M5 24h7M36 24h7M11 11l5 5M32 32l5 5M37 11l-5 5M16 32l-5 5" />
      </svg>
    );
  }

  if (name === "verify") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M24 5 39 11v11c0 10-6 17-15 21C15 39 9 32 9 22V11l15-6Z" />
        <path d="m17 24 5 5 10-11" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <circle cx="24" cy="24" r="17" />
      <path d="m15 24 6 6 13-15" />
    </svg>
  );
}

function TrustIcon({ name }: Readonly<{ name: TrustIconName }>) {
  if (name === "people") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="18" cy="16" r="6" />
        <circle cx="32" cy="18" r="5" />
        <path d="M7 38c1-9 6-13 11-13s10 4 11 13M27 38c0-7 4-11 9-11 4 0 7 3 8 11" />
      </svg>
    );
  }

  if (name === "shield") {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M24 5 39 11v11c0 10-6 17-15 21C15 39 9 32 9 22V11l15-6Z" />
        <path d="m17 24 5 5 10-11" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <path d="M8 39h32M12 34l8-10 7 6 10-17" />
      <path d="M31 13h6v6" />
    </svg>
  );
}

function DriveMark() {
  return (
    <span className="drive-mark" aria-hidden="true">
      <span className="drive-mark-top" />
      <span className="drive-mark-left" />
      <span className="drive-mark-right" />
    </span>
  );
}

export default function HomePage() {
  return (
    <>
      <header className="site-header">
        <div className="site-shell header-inner">
          <a className="brand" href="#home" aria-label="AJAS home">
            <BrandMark />
            <span className="brand-copy">
              <strong>AJAS</strong>
              <small>Automated Job Application System</small>
            </span>
          </a>

          <nav className="primary-nav" aria-label="Primary navigation">
            <a href="#home">Home</a>
            <a href="#workflow">How It Works</a>
            <a href="#job-search">Job Search</a>
            <a href="#drive">Google Drive</a>
            <a href="#trust">Security</a>
            <a href="#faq">FAQ</a>
            <a href="#about">About</a>
          </nav>

          <div className="header-actions">
            <a className="ui-button ui-button-secondary" href="#account-preview">
              Sign In
            </a>
            <a className="ui-button ui-button-primary" href="#account-preview">
              Create Account
            </a>
          </div>
        </div>
      </header>

      <main id="home">
        <section className="hero-section" aria-labelledby="hero-title">
          <div className="site-shell hero-grid">
            <div className="hero-copy">
              <p className="eyebrow">Powered by Agentic AI. Guided by You. Built Through Trust.</p>
              <h1 id="hero-title">AJAS</h1>
              <p className="hero-product-name">Automated Job Application System</p>
              <p className="hero-summary">
                Discover opportunities. Build from evidence. Prepare truthful applications. Always
                human-approved.
              </p>

              <div className="hero-rule" />

              <div className="human-boundary">
                <h2>Human-Only Submissions</h2>
                <p>
                  AJAS searches, organizes, analyzes, drafts, and verifies. Final application
                  submission always belongs to the human applicant.
                </p>
              </div>
            </div>

            <section
              className="auth-preview ui-card"
              id="account-preview"
              aria-labelledby="auth-title"
            >
              <div className="auth-tabs" aria-label="Account preview">
                <span className="auth-tab auth-tab-active">Create Account</span>
                <span className="auth-tab">Sign In</span>
              </div>

              <div className="auth-preview-body">
                <div className="section-heading-row">
                  <div>
                    <p className="preview-kicker">Personal Alpha preview</p>
                    <h2 id="auth-title">Get Started with AJAS</h2>
                  </div>
                  <span className="ui-chip">M2</span>
                </div>

                <p>
                  Account creation and secure sign-in arrive in Milestone 2. No credentials are
                  accepted by the Milestone 1C product shell.
                </p>

                <fieldset className="preview-fields" disabled>
                  <label>
                    <span>Full name</span>
                    <input className="ui-input" type="text" placeholder="Full name" />
                  </label>
                  <label>
                    <span>Email address</span>
                    <input className="ui-input" type="email" placeholder="Email address" />
                  </label>
                  <label>
                    <span>Password</span>
                    <input className="ui-input" type="password" placeholder="Create a password" />
                  </label>
                  <button className="ui-button ui-button-primary ui-button-block" type="button">
                    Create Account — M2
                  </button>
                </fieldset>

                <p className="preview-note" role="status">
                  Preview only. Authentication is intentionally disabled until the approved M2
                  backend exists.
                </p>
              </div>
            </section>
          </div>
        </section>

        <section className="capability-strip" aria-label="AJAS capabilities">
          <div className="site-shell capability-grid">
            {capabilities.map((capability) => (
              <article className="capability-item" key={capability.title}>
                <span className="capability-icon">
                  <CapabilityIcon name={capability.icon} />
                </span>
                <h2>{capability.title}</h2>
                <p>{capability.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="story-section" id="workflow">
          <div className="site-shell story-grid">
            <article className="story-copy">
              <p className="section-kicker">Evidence before automation</p>
              <h2>A Smarter Way to Apply</h2>
              <p>
                AJAS is a practical, evidence-grounded system for discovering opportunities and
                preparing application materials with agentic AI operating inside explicit
                boundaries.
              </p>

              <ul className="check-list">
                <li>Find and organize relevant job opportunities.</li>
                <li>Build from approved evidence, not guesswork.</li>
                <li>Create tailored, truthful application materials.</li>
                <li>Maintain sources, verification, and an audit trail.</li>
                <li>Stop autonomous authority before final submission.</li>
              </ul>

              <a className="ui-button ui-button-primary" href="#job-search">
                See How It Works <span aria-hidden="true">→</span>
              </a>
            </article>

            <article className="workflow-panel" aria-labelledby="workflow-title">
              <p className="section-kicker">Deterministic production path</p>
              <h2 id="workflow-title">The AJAS Workflow</h2>

              <ol className="workflow-list">
                {workflowSteps.map((step, index) => (
                  <li key={step}>
                    <span className="workflow-number">{index + 1}</span>
                    <span>{step}</span>
                  </li>
                ))}
              </ol>

              <p className="workflow-caption">
                From job discovery to a review-ready packet, AJAS follows a transparent process and
                stops before final submission.
              </p>
            </article>

            <aside className="drive-panel ui-card" id="drive" aria-labelledby="drive-title">
              <div className="drive-heading">
                <DriveMark />
                <div>
                  <p className="preview-kicker">User-controlled evidence</p>
                  <h2 id="drive-title">Google Drive</h2>
                </div>
                <span className="ui-chip">M3</span>
              </div>

              <h3>Your Data. Your Control.</h3>
              <p>
                Milestone 3 connects explicitly approved Drive sources for facts, resumes,
                supporting documents, and review-ready outputs.
              </p>

              <button
                className="ui-button ui-button-secondary ui-button-block"
                type="button"
                disabled
              >
                Connect Google Drive — M3
              </button>
              <button className="text-button" type="button" disabled>
                Manual upload becomes available after sign-in
              </button>

              <p className="preview-note">
                No Drive authorization or file access occurs on this Milestone 1C shell.
              </p>
            </aside>
          </div>
        </section>

        <section className="job-search-section" id="job-search" aria-labelledby="job-search-title">
          <div className="site-shell">
            <div className="section-intro">
              <div>
                <p className="section-kicker">A visible shell for the later agent workflow</p>
                <h2 id="job-search-title">Job Search Agent</h2>
              </div>
              <span className="ui-chip">M4 discovery · M6 scheduling</span>
            </div>

            <div className="search-preview ui-card">
              <div className="search-preview-grid">
                <section className="search-preview-block">
                  <h3>Roles / Titles</h3>
                  <div className="tag-list" aria-label="Example role controls">
                    <span className="ui-chip ui-chip-neutral">Azure MLOps Engineer</span>
                    <span className="ui-chip ui-chip-neutral">Machine Learning Engineer</span>
                    <span className="ui-chip ui-chip-neutral">Applied Data Scientist</span>
                  </div>
                  <p className="preview-note">
                    These are interface examples only, not active searches or applicant records.
                  </p>
                </section>

                <section className="search-preview-block">
                  <h3>Location Preferences</h3>
                  <div className="option-grid" aria-label="Example location preferences">
                    <span>Remote</span>
                    <span>Hybrid</span>
                    <span>California</span>
                    <span>United States</span>
                  </div>
                </section>

                <section className="search-preview-block">
                  <h3>Search Schedule</h3>
                  <div className="schedule-grid">
                    <div className="ui-stat">
                      <span>Cadence</span>
                      <strong>Twice daily</strong>
                    </div>
                    <div className="ui-stat">
                      <span>Example times</span>
                      <strong>6:00 AM · 6:00 PM</strong>
                    </div>
                  </div>
                </section>

                <section className="search-preview-block">
                  <h3>Result Limits</h3>
                  <div className="schedule-grid">
                    <div className="ui-stat">
                      <span>Minimum valid jobs</span>
                      <strong>5</strong>
                    </div>
                    <div className="ui-stat">
                      <span>Maximum per search</span>
                      <strong>25</strong>
                    </div>
                  </div>
                </section>
              </div>

              <div className="search-preview-footer">
                <div>
                  <strong>No searches have run.</strong>
                  <p>
                    M4 owns job discovery. M6 owns recurring schedules, batching, deduplication, and
                    queue limits.
                  </p>
                </div>
                <div className="search-preview-actions">
                  <button className="ui-button ui-button-primary" type="button" disabled>
                    Search Now — M4
                  </button>
                  <button className="ui-button ui-button-secondary" type="button" disabled>
                    Save Profile
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="trust-section" id="trust" aria-labelledby="trust-title">
          <div className="site-shell trust-grid">
            <article className="trust-lead" id="about">
              <p className="section-kicker">Human-centered by design</p>
              <h2 id="trust-title">Built for Real People</h2>
              <p>
                AJAS follows a clear boundary: truthful evidence, no employer outreach, no automatic
                submission, and no invented applicant information.
              </p>
              <a className="text-link" href="#faq">
                Learn about the approach <span aria-hidden="true">→</span>
              </a>
            </article>

            {trustCards.map((card) => (
              <article className="trust-card ui-card" key={card.title}>
                <span className="trust-icon">
                  <TrustIcon name={card.icon} />
                </span>
                <h3>{card.title}</h3>
                <p>{card.body}</p>
                <a className="text-link" href={card.href}>
                  {card.link} <span aria-hidden="true">→</span>
                </a>
              </article>
            ))}
          </div>
        </section>

        <section className="faq-section" id="faq" aria-labelledby="faq-title">
          <div className="site-shell">
            <div className="section-intro">
              <div>
                <p className="section-kicker">Clear boundaries before feature depth</p>
                <h2 id="faq-title">What AJAS Does — and Does Not Do</h2>
              </div>
            </div>

            <div className="faq-grid">
              <article className="ui-card">
                <h3>Does AJAS submit applications?</h3>
                <p>
                  No. Autonomous authority stops at a review-ready packet. Final employer-system
                  interaction and final submission remain human-only.
                </p>
              </article>
              <article className="ui-card">
                <h3>Where do applicant facts come from?</h3>
                <p>
                  Only approved or sourced evidence may support applicant claims. Missing evidence
                  becomes a named gap rather than invented content.
                </p>
              </article>
              <article className="ui-card">
                <h3>Are Sign In, Drive, and Job Search live?</h3>
                <p>
                  Not yet. Milestone 1C intentionally presents the future product shell without
                  accepting credentials, Drive access, or live job-search instructions.
                </p>
              </article>
            </div>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="site-shell footer-inner">
          <a className="brand footer-brand" href="#home" aria-label="AJAS home">
            <BrandMark />
            <span className="brand-copy">
              <strong>AJAS</strong>
              <small>Automated Job Application System</small>
            </span>
          </a>

          <nav className="footer-nav" aria-label="Footer navigation">
            <a href="#home">Home</a>
            <a href="#workflow">How It Works</a>
            <a href="#job-search">Job Search</a>
            <a href="#drive">Google Drive</a>
            <a href="#trust">Security</a>
            <a href="#faq">FAQ</a>
          </nav>

          <p>Powered by Agentic AI. Guided by You. Built Through Trust.</p>
        </div>
      </footer>
    </>
  );
}
