# ClientIQ Project Blueprint

## Current Product Definition

ClientIQ is a premium inbound call intelligence platform. A visitor calls a visible Twilio number, speaks with a realtime xAI/Grok Supervisor Voice Agent, receives a client-specific dashboard, and gets the dashboard link by email and SMS.

Current decision: **external workflow automation has been removed from the MVP.** Delivery is direct from the FastAPI backend through Gmail SMTP and Twilio SMS.

---

## Core Promise

Turn an inbound call into:
- structured client intelligence
- live public business context
- a client-safe dashboard
- practical improvement tips
- direct follow-up by Gmail and Twilio SMS

The public website should not promise that the full dashboard is built instantly while the call is still happening. The correct promise is that the AI gathers context, researches public information, and prepares a thoughtful dashboard after the conversation.

---

## Approved Runtime Architecture

Architecture diagram:

- `docs/langgraph-architecture.md`
- `docs/langgraph-architecture.svg`

```text
Frontend website
-> Twilio voice number
-> FastAPI Twilio inbound webhook
-> FastAPI media WebSocket
-> xAI/Grok realtime voice session
-> backend tool dispatch
-> LangGraph post-call intelligence
-> SQLite persistence
-> public dashboard lookup by slug
-> direct Gmail SMTP email
-> direct Twilio SMS
```

---

## Approved Stack

- Next.js JavaScript frontend
- Tailwind CSS
- FastAPI backend
- LangGraph backend orchestration
- xAI/Grok realtime voice
- Twilio Voice and SMS
- SQLite local database
- Gmail SMTP email
- local JSON call outputs

Not in MVP:
- external workflow automation
- CRM integration
- payment flow
- meeting booking
- outbound campaigns
- advanced analytics admin panel
- multi-agent live system

---

## Main User Journey

1. Visitor lands on premium website.
2. Visitor sees phone CTA.
3. Visitor calls Twilio number.
4. Twilio sends call to FastAPI webhook.
5. Twilio streams audio to backend WebSocket.
6. Backend bridges Twilio to xAI/Grok realtime.
7. Voice agent asks discovery questions.
8. Voice agent detects official website or company name.
9. Backend analyzes official public website.
10. Voice agent shares one grounded live observation.
11. Voice agent gathers pain points, goals, email, and context.
12. `save_dashboard_data` persists structured records.
13. SQLite stores public dashboard data and internal data separately.
14. Dashboard slug is generated.
15. Dashboard route loads saved data.
16. Backend sends Gmail email with dashboard link.
17. Backend sends Twilio SMS with dashboard link.
18. Local call JSON is saved for debugging.

---

## Voice Agent Blueprint

The voice agent is the **Supervisor Voice Agent**.

Personality:
- premium
- warm
- patient
- concise
- business-aware
- not salesy
- not robotic

Rules:
- ask one question at a time
- acknowledge answers before moving on
- use caller first name naturally
- stop when caller interrupts
- do not repeat the same greeting or question
- do not claim private data access
- do not mention backend tools or scraping
- do not hallucinate research findings

Live research behavior:
- use public official website only
- analyze quietly in background
- share one impressive but grounded observation
- connect observation to caller's pain point
- ask one follow-up question

---

## Backend Blueprint

FastAPI owns API routes, Twilio webhook/media WebSocket, tool dispatch, validation, SQLite access, dashboard lookup, and direct Gmail/Twilio delivery.

LangGraph owns transcript intelligence, enrichment, dashboard payload assembly, and next-step recommendations.

Realtime voice path owns low-latency conversation, barge-in behavior, prompt/tool registration, and handoff to backend tools.

Do not put heavy reasoning in the live audio bridge.

---

## Database Blueprint

SQLite should support:
- `call_sessions`
- `transcripts`
- `client_profiles`
- `dashboard_payloads`
- `delivery_records`
- optional generic internal event records

---

## Public Dashboard Rules

Route:

```text
/dashboard/[client-slug]
```

Public dashboard may show company summary, public website analysis, pain points heard, improvement tips, opportunities, quick wins, next steps, and safe metrics.

Public dashboard must not show raw transcript, internal notes, private qualification details, hidden prompts, secrets, or provider errors.

It must handle missing/partial data gracefully.

---

## Delivery Blueprint

Delivery happens after dashboard save.

Gmail email should include thank-you note, dashboard link, short summary, quick wins, and next-step CTA.

Twilio SMS should include short thank-you and dashboard link.

Delivery safety:
- do not send before dashboard slug exists
- avoid duplicate successful sends
- retry skipped/failed sends when credentials or recipient data are fixed
- preserve dashboard even if delivery fails

Environment variables live in `backend/.env`:

```text
GMAIL_USERNAME
GMAIL_APP_PASSWORD
GMAIL_FROM_EMAIL
GMAIL_SMTP_HOST
GMAIL_SMTP_PORT
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER
DELIVERY_ENABLED
```

---

## Phase Blueprint

- **Phase 1:** Premium frontend and dashboard UI.
- **Phase 2:** Realtime voice backend foundation.
- **Phase 3:** End-to-end integration without external workflow automation.
- **Phase 4:** Development, debugging, and demo readiness.

---

## Current Debug Priorities

- make the voice agent sound human and consultative
- ensure it does not talk twice or over the caller
- ensure spoken company websites are detected correctly
- prevent email addresses from becoming fake scrape URLs
- ensure official website analysis reaches the agent during the call
- ensure dashboard generation uses transcript + research
- ensure Gmail/SMS delivery can be retried
- ensure local JSON outputs explain what happened

---

## Bob Guidance

Bob should read project docs first, inspect code before editing, keep changes small, validate after changes, never hardcode secrets, report exact blockers, keep architecture clean, and never reintroduce external workflow automation unless the user explicitly asks.
