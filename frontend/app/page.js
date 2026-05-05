import HeroIntelligenceScene from "@/components/HeroIntelligenceScene";

const phoneDisplay = process.env.NEXT_PUBLIC_TWILIO_PHONE_NUMBER || "+1 (888) 555-0198";
const phoneHref = `tel:${phoneDisplay.replace(/[^\d+]/g, "")}`;

const trustItems = [
  "Realtime AI Voice",
  "Business Intelligence Layer",
  "Dashboard-Driven Workflow",
  "Built for Scale"
];

const features = [
  {
    title: "Inbound AI conversation",
    copy: "A premium voice experience gathers the right business context without forcing prospects through static forms."
  },
  {
    title: "Public signal research",
    copy: "The system uses public business context to make the conversation more relevant, grounded, and useful."
  },
  {
    title: "Structured client profile",
    copy: "Every call can become organized intelligence: company summary, needs, signals, quick wins, and next steps."
  },
  {
    title: "Dashboard-ready output",
    copy: "The result is designed for a clean client-specific dashboard delivered after the conversation."
  }
];

const steps = [
  "Visitor calls the visible number",
  "AI starts a focused business conversation",
  "Public signals enrich the understanding",
  "A thoughtful dashboard is prepared"
];

const opportunities = [
  "Clarify service positioning above the fold",
  "Improve local discoverability signals",
  "Create a sharper follow-up offer",
  "Turn call notes into next-step recommendations"
];

const industries = [
  "B2B services",
  "Agencies",
  "Consultants",
  "SaaS teams",
  "Local businesses",
  "Client acquisition teams"
];

function Nav() {
  return (
    <header className="fixed left-0 right-0 top-0 z-50 border-b border-white/10 bg-ink/80 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8">
        <a href="#top" className="flex items-center gap-3" aria-label="ClientIQ home">
        <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-cyan/30 bg-cyan/10 text-sm font-semibold text-cyan">
            CIQ
          </span>
          <span className="text-sm font-semibold tracking-wide text-white">ClientIQ</span>
        </a>
        <div className="hidden items-center gap-7 text-sm text-mist md:flex">
          <a className="transition hover:text-white" href="#features">What it does</a>
          <a className="transition hover:text-white" href="#process">How it works</a>
          <a className="transition hover:text-white" href="#dashboard">Dashboard</a>
        </div>
        <a
          href={phoneHref}
          className="rounded-full border border-white/15 bg-white px-4 py-2 text-sm font-semibold text-ink transition hover:bg-cyan"
        >
          {phoneDisplay}
        </a>
      </nav>
    </header>
  );
}

function HeroVisual() {
  return (
    <div className="relative mx-auto w-full max-w-xl">
      <div className="glass-panel relative overflow-hidden rounded-lg p-4 shadow-glow">
        <div className="rounded-lg border border-white/10 bg-graphite/95 p-4">
          <div className="flex items-center justify-between border-b border-white/10 pb-4">
            <div>
              <p className="text-xs uppercase tracking-[0.28em] text-cyan">Live profile</p>
              <h2 className="mt-2 text-xl font-semibold text-white">Client intelligence preview</h2>
            </div>
            <div className="rounded-full bg-cyan/10 px-3 py-1 text-xs font-semibold text-cyan">Preview</div>
          </div>
          <div className="grid gap-3 pt-4 sm:grid-cols-3">
            {["Call quality", "Fit signal", "Follow-up"].map((label, index) => (
              <div key={label} className="rounded-lg border border-white/10 bg-white/[0.04] p-3">
                <p className="text-xs text-mist">{label}</p>
                <p className="mt-3 text-2xl font-semibold text-white">{[94, 87, 91][index]}%</p>
              </div>
            ))}
          </div>
          <div className="mt-4 grid gap-3 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
              <p className="text-sm font-semibold text-white">Conversation summary</p>
              <p className="mt-3 text-sm leading-6 text-mist">
                Owner is exploring a better way to capture lead context, qualify fit, and turn first calls into useful
                recommendations without adding manual admin work.
              </p>
              <div className="mt-5 space-y-2">
                <div className="h-2 rounded-full bg-cyan/70" />
                <div className="h-2 w-4/5 rounded-full bg-white/20" />
                <div className="h-2 w-2/3 rounded-full bg-white/10" />
              </div>
            </div>
            <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
              <p className="text-sm font-semibold text-white">Opportunity areas</p>
              <div className="mt-3 space-y-3">
                {opportunities.slice(0, 3).map((item) => (
                  <div key={item} className="flex gap-3 text-sm text-mist">
                    <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-gold" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function DashboardPreview() {
  return (
    <section id="dashboard" className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
      <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.28em] text-cyan">Dashboard output</p>
          <h2 className="mt-5 text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            A polished intelligence view after the call.
          </h2>
          <p className="mt-5 max-w-xl text-lg leading-8 text-mist">
            The homepage shows the outcome without overpromising live generation. The dashboard is positioned as a
            thoughtful post-conversation deliverable built from call context and public business signals.
          </p>
        </div>
        <div className="glass-panel rounded-lg p-4">
          <div className="rounded-lg bg-[#080c13] p-5">
            <div className="flex flex-col gap-4 border-b border-white/10 pb-5 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="text-sm text-mist">Demo client</p>
                <h3 className="mt-1 text-2xl font-semibold text-white">Northline Advisory</h3>
              </div>
              <div className="rounded-full border border-cyan/25 bg-cyan/10 px-4 py-2 text-sm font-semibold text-cyan">
                Digital presence score 82
              </div>
            </div>
            <div className="grid gap-3 py-5 md:grid-cols-2">
              {[
                ["Company summary", "Growth advisory team serving founder-led service businesses."],
                ["Website notes", "Clear expertise, but service paths need sharper conversion cues."],
                ["Google presence", "Good branded visibility with room for stronger review signals."],
                ["Social footprint", "Credible LinkedIn activity, limited proof-led content cadence."]
              ].map(([title, copy]) => (
                <div key={title} className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
                  <p className="font-semibold text-white">{title}</p>
                  <p className="mt-2 text-sm leading-6 text-mist">{copy}</p>
                </div>
              ))}
            </div>
            <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
              <p className="font-semibold text-white">Selected quick wins</p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {opportunities.map((item) => (
                  <div key={item} className="flex gap-3 text-sm text-mist">
                    <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-cyan" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <main id="top" className="min-h-screen overflow-hidden bg-ink text-platinum">
      <Nav />

      <section className="relative min-h-screen pt-32 sm:pt-40">
        <HeroIntelligenceScene />
        <div className="absolute inset-x-0 top-20 z-0 h-[36rem] fine-grid opacity-20" />
        <div className="absolute inset-0 z-0 bg-gradient-to-r from-ink via-ink/80 to-ink/20" />
        <div className="relative z-10 mx-auto grid max-w-7xl gap-12 px-5 pb-20 sm:px-8 lg:grid-cols-[1fr_0.92fr] lg:items-center">
          <div>
            <div className="inline-flex items-center gap-3 rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-mist">
              <span className="h-2 w-2 rounded-full bg-cyan shadow-[0_0_20px_rgba(119,228,242,0.9)]" />
              Premium inbound call intelligence
            </div>
            <h1 className="mt-8 max-w-4xl text-5xl font-semibold tracking-tight text-white sm:text-7xl lg:text-8xl">
              Turn inbound calls into realtime business intelligence.
            </h1>
            <p className="mt-7 max-w-2xl text-lg leading-8 text-mist sm:text-xl">
              ClientIQ gives every caller a warm AI voice experience and prepares a structured dashboard from
              the conversation and public business context.
            </p>
            <div className="mt-9 flex flex-col gap-4 sm:flex-row">
              <a
                href={phoneHref}
                className="inline-flex items-center justify-center rounded-full bg-white px-6 py-4 text-base font-semibold text-ink transition hover:bg-cyan"
              >
                Call Now: {phoneDisplay}
              </a>
              <a
                href="#dashboard"
                className="inline-flex items-center justify-center rounded-full border border-white/15 px-6 py-4 text-base font-semibold text-white transition hover:border-cyan/60 hover:bg-cyan/10"
              >
                See Dashboard Preview
              </a>
            </div>
            <p className="mt-5 text-sm text-mist">
              A concise AI-led conversation, followed by a structured intelligence view your team can act on.
            </p>
          </div>
          <HeroVisual />
        </div>
      </section>

      <section className="border-y border-white/10 bg-white/[0.03]">
        <div className="mx-auto grid max-w-7xl gap-4 px-5 py-5 sm:grid-cols-2 sm:px-8 lg:grid-cols-4">
          {trustItems.map((item) => (
            <div key={item} className="rounded-lg border border-white/10 bg-white/[0.03] px-4 py-4 text-sm font-semibold text-white">
              {item}
            </div>
          ))}
        </div>
      </section>

      <section id="features" className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.28em] text-cyan">What it does</p>
          <h2 className="mt-5 text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            A call experience that captures context, not just contact details.
          </h2>
        </div>
        <div className="mt-12 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <article key={feature.title} className="rounded-lg border border-white/10 bg-white/[0.04] p-6">
              <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
              <p className="mt-4 text-sm leading-7 text-mist">{feature.copy}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="process" className="bg-white/[0.03]">
        <div className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="grid gap-10 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.28em] text-cyan">How it works</p>
              <h2 className="mt-5 text-4xl font-semibold tracking-tight text-white sm:text-5xl">
                Simple for the caller. Structured for the business.
              </h2>
              <p className="mt-5 text-lg leading-8 text-mist">
                The experience is designed to feel natural for the caller while giving your business cleaner context,
                clearer signals, and a more useful follow-up path.
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              {steps.map((step, index) => (
                <div key={step} className="rounded-lg border border-white/10 bg-ink/60 p-6">
                  <span className="text-sm font-semibold text-gold">0{index + 1}</span>
                  <p className="mt-5 text-xl font-semibold text-white">{step}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <DashboardPreview />

      <section className="mx-auto max-w-7xl px-5 pb-24 sm:px-8">
        <div className="grid gap-10 rounded-lg border border-white/10 bg-white/[0.04] p-6 sm:p-10 lg:grid-cols-[0.95fr_1.05fr] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.28em] text-cyan">Use cases</p>
            <h2 className="mt-5 text-4xl font-semibold tracking-tight text-white">
              Built for teams that need sharper first conversations.
            </h2>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {industries.map((industry) => (
              <div key={industry} className="rounded-lg border border-white/10 bg-ink/70 px-4 py-4 text-sm font-semibold text-white">
                {industry}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-white/10 bg-[#070b12]">
        <div className="mx-auto max-w-7xl px-5 py-20 text-center sm:px-8">
          <p className="text-sm font-semibold uppercase tracking-[0.28em] text-cyan">Call the AI agent</p>
          <h2 className="mx-auto mt-5 max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-6xl">
            Start with one conversation. Leave with clearer client intelligence.
          </h2>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-mist">
            A premium first conversation can capture the context, signals, and opportunities that usually disappear
            inside unstructured call notes.
          </p>
          <a
            href={phoneHref}
            className="mt-9 inline-flex items-center justify-center rounded-full bg-white px-7 py-4 text-base font-semibold text-ink transition hover:bg-cyan"
          >
            {phoneDisplay}
          </a>
        </div>
      </section>

      <footer className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-10 text-sm text-mist sm:px-8 md:flex-row md:items-center md:justify-between">
        <p className="font-semibold text-white">ClientIQ</p>
        <div className="flex flex-wrap gap-5">
          <a href="#features" className="hover:text-white">Features</a>
          <a href="#process" className="hover:text-white">How it works</a>
          <a href="#dashboard" className="hover:text-white">Dashboard</a>
          <a href="mailto:hello@fainazclientiq.com" className="hover:text-white">hello@fainazclientiq.com</a>
        </div>
      </footer>
    </main>
  );
}
