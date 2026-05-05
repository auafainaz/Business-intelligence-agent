const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function getDashboard(slug) {
  try {
    const response = await fetch(`${apiBaseUrl}/api/dashboard/${slug}`, {
      cache: "no-store"
    });
    if (!response.ok) {
      return null;
    }
    return response.json();
  } catch {
    return null;
  }
}

function ListBlock({ title, items }) {
  const safeItems = Array.isArray(items) ? items.filter(Boolean) : [];
  if (!safeItems.length) {
    return (
      <section className="rounded-lg border border-white/10 bg-white/[0.04] p-5">
        <h2 className="text-lg font-semibold text-white">{title}</h2>
        <p className="mt-3 text-sm leading-6 text-mist">This section will populate as more call context is saved.</p>
      </section>
    );
  }
  return (
    <section className="rounded-lg border border-white/10 bg-white/[0.04] p-5">
      <h2 className="text-lg font-semibold text-white">{title}</h2>
      <div className="mt-4 space-y-3">
        {safeItems.map((item) => (
          <div key={item} className="flex gap-3 text-sm leading-6 text-mist">
            <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-cyan" />
            <span>{item}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export default async function ClientDashboard({ params }) {
  const resolvedParams = await params;
  const slug = resolvedParams["client-slug"];
  const dashboard = await getDashboard(slug);

  if (!dashboard) {
    return (
      <main className="min-h-screen bg-ink px-5 py-16 text-platinum sm:px-8">
        <div className="mx-auto max-w-4xl rounded-lg border border-white/10 bg-white/[0.04] p-8">
          <p className="text-sm font-semibold uppercase tracking-[0.28em] text-cyan">Dashboard unavailable</p>
          <h1 className="mt-4 text-4xl font-semibold text-white">We could not find this dashboard.</h1>
          <p className="mt-4 text-mist">
            The link may still be processing, or the dashboard slug may be incorrect.
          </p>
        </div>
      </main>
    );
  }

  const payload = dashboard.public_payload || {};
  const client = payload.client || {};
  const companyName = client.business_name || "Client dashboard";
  const summary = payload.company_summary || dashboard.conversation_summary || "Your call intelligence summary is ready.";
  const metrics = payload.safe_metrics || {};
  const companyAnalysis = payload.company_analysis || [];
  const painPoints = payload.key_pain_points || [];
  const improvementTips = payload.improvement_tips || payload.quick_wins || [];

  return (
    <main className="min-h-screen bg-ink text-platinum">
      <section className="border-b border-white/10 bg-[#070b12] px-5 py-16 sm:px-8">
        <div className="mx-auto max-w-7xl">
          <p className="text-sm font-semibold uppercase tracking-[0.28em] text-cyan">ClientIQ Dashboard</p>
          <div className="mt-6 grid gap-8 lg:grid-cols-[1fr_0.35fr] lg:items-end">
            <div>
              <h1 className="text-5xl font-semibold tracking-tight text-white sm:text-7xl">{companyName}</h1>
              <p className="mt-5 max-w-3xl text-lg leading-8 text-mist">{summary}</p>
            </div>
            <div className="rounded-lg border border-cyan/20 bg-cyan/10 p-5">
              <p className="text-sm text-mist">Dashboard slug</p>
              <p className="mt-2 break-words text-lg font-semibold text-cyan">{dashboard.dashboard_slug}</p>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-5 py-12 sm:px-8">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[
            ["Google rating", metrics.google_rating || "Pending"],
            ["Reviews", metrics.review_count || "Pending"],
            ["AI search", metrics.ai_search_status || "Pending"],
            ["Load speed", metrics.load_speed || "Pending"]
          ].map(([label, value]) => (
            <div key={label} className="rounded-lg border border-white/10 bg-white/[0.04] p-5">
              <p className="text-sm text-mist">{label}</p>
              <p className="mt-3 text-2xl font-semibold text-white">{value}</p>
            </div>
          ))}
        </div>

        <div className="mt-8 grid gap-4 lg:grid-cols-2">
          <ListBlock title="Digital Presence Notes" items={payload.digital_presence_notes} />
          <ListBlock title="Company Analysis" items={companyAnalysis} />
          <ListBlock title="Pain Points Heard" items={painPoints} />
          <ListBlock title="Improvement Tips" items={improvementTips} />
          <ListBlock title="Website Notes" items={payload.website_notes} />
          <ListBlock title="Google/Public Presence" items={payload.google_presence_notes} />
          <ListBlock title="Social Presence" items={payload.social_presence_notes} />
          <ListBlock title="Opportunity Areas" items={payload.main_opportunities} />
          <ListBlock title="Quick Wins" items={payload.quick_wins} />
        </div>

        <div className="mt-4">
          <ListBlock title="Recommended Next Steps" items={payload.next_steps} />
        </div>
      </section>
    </main>
  );
}
