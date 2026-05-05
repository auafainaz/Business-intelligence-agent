# Phase 1 - Premium Frontend

## Goal

Build the public ClientIQ web experience and dashboard UI using Next.js, JavaScript, and Tailwind CSS.

The frontend should feel premium, dark, modern, and Apple-like. It should sell the idea of turning an inbound call into useful business intelligence without exposing backend internals.

## Scope

- Public homepage with strong hero section
- Visible phone number CTA
- Feature sections that explain the offer
- Dashboard preview section
- Responsive desktop and mobile layout
- `/dashboard/[client-slug]` route UI
- Graceful states for missing, loading, or partial dashboard data
- JavaScript only for frontend code
- Tailwind CSS for styling

## Current Relevant Files

- `frontend/app/page.js`
- `frontend/app/layout.js`
- `frontend/app/globals.css`
- `frontend/app/dashboard/[client-slug]/page.js`
- `frontend/components/HeroIntelligenceScene.js`
- `frontend/tailwind.config.js`
- `frontend/.env.example`
- `frontend/README.md`

## Design Requirements

- Dark premium visual system
- Clear first-viewport phone CTA
- Polished typography and spacing
- Responsive layout that works on phone and desktop
- Dashboard page should look credible even with partial data
- Avoid exposing transcript, internal notes, prompts, provider errors, or secrets

## Data Rules

During Phase 1, the dashboard can use mock or fallback UI states. Once integrated, it must fetch only public dashboard-safe data from the backend.

Public dashboard-safe data can include:

- company summary
- public website observations
- opportunity areas
- quick wins
- improvement tips
- next-step recommendations

Public dashboard must not include:

- raw transcript
- private caller notes
- hidden prompts
- provider errors
- credentials
- internal payloads

## Excludes

- Twilio call handling
- xAI/Grok realtime voice
- FastAPI persistence
- Gmail delivery
- Twilio SMS delivery
- CRM, payments, booking, outbound campaigns

## Acceptance Criteria

- Homepage loads locally
- Phone CTA is visible and correct
- Dashboard route renders at `/dashboard/[client-slug]`
- Missing dashboard data shows a polished unavailable/processing state
- UI is responsive on mobile and desktop
- No backend secrets or internal payloads are exposed in the frontend

## Validation

Run from `frontend/`:

```powershell
npm install
npm run dev
```

Then check:

- `http://127.0.0.1:3000`
- `http://127.0.0.1:3000/dashboard/example-client`
