# ClientIQ Project Phase Plan

This plan reflects the current build decisions for ClientIQ after development/debugging updates.

Current decision: **external workflow automation is not part of the MVP runtime.** Post-call email and SMS delivery are handled directly by FastAPI services using Gmail SMTP and Twilio REST API.

---

## Product Flow

Architecture diagram:

- `docs/langgraph-architecture.md`
- `docs/langgraph-architecture.svg`

```text
Public Website
-> Twilio inbound call
-> xAI/Grok realtime voice agent
-> FastAPI backend tools
-> LangGraph post-call intelligence
-> SQLite persistence
-> dashboard route
-> direct Gmail + Twilio SMS delivery
```

Core order:

```text
save first -> dashboard second -> delivery third
```

---

## Phase 1 - Premium Frontend

### Goal
Create the premium public web experience and dashboard UI.

### Scope
- Next.js JavaScript app
- Tailwind CSS
- dark premium Apple-like visual style
- strong hero section
- visible phone number CTA
- feature sections
- dashboard preview
- `/dashboard/[client-slug]` UI that handles partial data

### Excludes
- live backend integration
- Twilio call handling
- realtime voice
- SQLite persistence
- Gmail/SMS sends

### Completion Criteria
- homepage and core pages load
- phone CTA is visible
- dashboard UI renders gracefully with mock or missing data
- layout works on desktop/mobile

---

## Phase 2 - Realtime Voice Agent Foundation

### Goal
Build the backend foundation for a realtime inbound business intelligence voice agent.

### Scope
- FastAPI app structure
- Twilio inbound webhook
- Twilio media WebSocket
- xAI/Grok realtime session scaffold
- runtime prompt loaded from `backend/prompts/grok-voice-system-prompt.md`
- one Supervisor Voice Agent
- tool registry and dispatch
- `save_dashboard_data`
- `save_call_transcript`
- `create_dashboard_payload`
- `generate_dashboard_slug`
- `analyze_official_page`
- SQLite tables for call sessions, transcripts, client profiles, dashboard payloads
- public/internal data split

### Live Voice Behavior
- ask one question at a time
- be concise and human
- handle barge-in/interruption
- research official public website quietly
- share one useful public observation during the call
- do not mention scraping/tools/internal mechanics

### Excludes
- Gmail/SMS as finished delivery flow
- CRM
- payment
- booking
- multi-agent live orchestration

### Completion Criteria
- inbound call reaches agent
- agent can gather business details
- website URL can be analyzed
- dashboard data can be saved
- transcript can be stored

---

## Phase 3 - Integrated Product Flow

### Goal
Connect frontend, voice, backend, database, dashboard, and direct delivery into one working product.

### Scope
- frontend dashboard route reads real backend data
- Twilio inbound call connected to xAI bridge
- Grok tool calls saved through FastAPI
- LangGraph runs behind live call path
- SQLite stores call session, transcript, profile, public dashboard payload, internal payload
- local JSON output saved after each call
- direct Gmail email sends dashboard link
- direct Twilio SMS sends dashboard link
- delivery records use idempotency keys
- failed/skipped delivery can be retried

### Excludes
- external workflow automation
- CRM
- payment
- booking
- outbound campaign logic
- advanced analytics admin panel

### Completion Criteria
- call creates dashboard slug
- `/dashboard/[client-slug]` renders saved data
- dashboard link can be emailed
- dashboard link can be texted
- public dashboard does not expose internal data
- one delivery channel failing does not destroy the dashboard flow

---

## Phase 4 - Development, Debugging, and Demo Readiness

### Goal
Stabilize the system for repeatable demos and early testing.

### Scope
- validate ngrok + Twilio webhook setup
- validate xAI realtime call behavior
- validate barge-in and no double-speaking
- validate live official website analysis
- validate the agent uses research in conversation
- validate dashboard creation and lookup
- validate local output JSON
- validate Gmail credentials and email delivery
- validate Twilio trial/A2P/verified recipient constraints
- validate SMS delivery and duplicate-send prevention
- validate retry behavior for skipped/failed delivery
- validate frontend routes and responsive UI

### Excludes
- large new feature work
- CRM/payment/booking/outbound
- reintroducing external workflow automation

### Completion Criteria
- repeated test calls work
- agent gives at least one grounded live company observation
- dashboard link opens
- email/SMS delivery works or logs clear safe failures
- logs show root cause for failures
- demo can be run from clean startup instructions

---

## Bob Development Rules

- Always identify active phase first.
- Keep changes phase-scoped.
- Inspect code before editing.
- Do not hardcode secrets.
- Update `.env.example` when adding env variables.
- Keep provider logic isolated in services.
- Keep live call path thin.
- Keep LangGraph behind the live path.
- Keep public and internal data separate.
- Do not reintroduce external workflow automation unless explicitly requested.
- Validate after changes and report what was tested.
