# AGENTS.md
## Project: ClientIQ
### Premium Inbound Call Intelligence Platform
### Current Operating Instructions for Development Agents

---

## 1. Product Identity

**ClientIQ** turns an inbound phone call into structured business intelligence, a public-safe client dashboard, and direct follow-up by email/SMS.

The product is not a generic chatbot. It is a premium realtime discovery experience:

```text
Public Website
-> Twilio inbound call
-> xAI/Grok realtime Supervisor Voice Agent
-> FastAPI + LangGraph backend tools
-> SQLite persistence
-> public dashboard route
-> direct Gmail email + Twilio SMS delivery
```

Current decision: **do not use external workflow automation**. Gmail and Twilio SMS are sent directly from the FastAPI backend after the dashboard payload and slug are safely saved.

---

## 2. Approved Stack

- **Frontend:** Next.js, JavaScript, Tailwind CSS
- **Telephony:** Twilio Voice + Twilio SMS
- **Realtime voice:** xAI/Grok realtime voice
- **Backend:** FastAPI
- **Orchestration:** LangGraph behind the live voice path
- **Storage:** SQLite
- **Email:** Gmail SMTP with app password
- **Dashboard:** `/dashboard/[client-slug]`
- **Automation:** direct backend delivery only for this MVP

No CRM, payments, booking, outbound campaigns, or advanced analytics panel in the current MVP.

---

## 3. Current Runtime Flow

```text
Visitor opens website
-> sees premium offer and phone CTA
-> calls Twilio number
-> Twilio streams call audio to FastAPI WebSocket
-> FastAPI bridges Twilio audio to xAI realtime
-> Grok Supervisor Voice Agent gathers discovery details
-> agent researches official public website during the call
-> agent shares 1 useful live observation and asks a sharp follow-up
-> save_dashboard_data persists transcript/profile/dashboard payload
-> SQLite stores public and internal records separately
-> dashboard slug becomes available
-> backend sends Gmail email and Twilio SMS with dashboard link
-> local JSON call summary is written to backend/outputs/calls
```

The live voice path stays thin. Heavy dashboard assembly, transcript intelligence, persistence, and delivery happen behind the live path.

---

## 4. Phase Model

### Phase 1 - Frontend
Build the premium public website and dashboard UI.

Includes:
- homepage, about, how-it-works
- visible phone CTA
- dashboard route UI
- premium dark Apple-like design
- responsive Tailwind layout

Excludes:
- real Twilio handling
- backend saves
- live AI voice
- email/SMS sending

### Phase 2 - Realtime Voice Agent Foundation
Build the inbound realtime voice foundation.

Includes:
- FastAPI backend structure
- Twilio inbound webhook and media stream
- xAI/Grok realtime session scaffold
- prompt loading from `backend/prompts/grok-voice-system-prompt.md`
- one Supervisor Voice Agent
- live official website research scaffold
- `save_dashboard_data` and related tools
- SQLite schema for calls, transcripts, profiles, dashboard payloads

Excludes:
- post-call delivery automation as a finished product
- CRM/payment/booking
- multi-agent live orchestration

### Phase 3 - Integrated Product Flow
Connect the product end to end without external workflow automation.

Includes:
- frontend dashboard loads real SQLite-backed payloads
- Twilio inbound connected to xAI bridge
- `save_dashboard_data` fully wired to persistence
- local output JSON generated after calls
- direct Gmail SMTP delivery
- direct Twilio SMS delivery
- idempotency to avoid duplicate sends
- public/internal data separation

Excludes:
- external workflow automation
- CRM
- payment
- meeting booking
- outbound campaigns

### Phase 4 - Development, Debugging, and Demo Readiness
Stabilize what exists.

Includes:
- repeated live call tests
- voice naturalness and barge-in behavior
- live research/wow moment validation
- dashboard validation
- Gmail/SMS delivery validation
- Twilio trial/A2P constraints documented
- logs and SQLite inspection
- retry and duplicate-send behavior
- frontend/backend startup documentation

Excludes:
- new major product features unless explicitly requested

---

## 5. Voice Agent Rules

The realtime agent is the **Supervisor Voice Agent**.

It must be warm, professional, concise, human-like, curious, non-pushy, and business-aware.

Conversation rules:
- ask one question at a time
- acknowledge before moving on
- use first name naturally when known
- if interrupted, stop speaking and listen
- do not repeat greetings or questions unnecessarily
- do not sound like a form
- do not over-explain technical internals

Opening should gather naturally:
- full name
- role
- company name
- website
- years in business
- email
- phone if needed
- AI familiarity
- pain points

Live research rule:
- when company name or website is known, research public official website quietly
- use official public page only, not broad scraping or private/internal sources
- share one specific public observation during the call
- connect that observation to the caller's pain point
- ask one useful follow-up question
- never mention scraping, JSON, backend tools, or internal mechanics

---

## 6. Data Rules

Always separate:

1. **Public dashboard-safe payload**
   - company summary
   - website observations
   - opportunity areas
   - selected recommendations
   - safe metrics
   - no raw transcript

2. **Internal payload**
   - full transcript
   - personal touch
   - detailed pain points/goals
   - tool results
   - call metadata

Never expose raw transcript, private notes, credentials, hidden prompts, or internal-only details on public dashboard pages.

---

## 7. Delivery Rules

Current MVP delivery is direct backend delivery.

Gmail uses:
- `GMAIL_USERNAME`
- `GMAIL_APP_PASSWORD`
- `GMAIL_FROM_EMAIL`
- SMTP host/port from `.env`

Twilio SMS uses:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- saved client phone or Twilio caller number fallback

Delivery must happen only after dashboard payload and slug are saved. If email fails, SMS may still send. If SMS fails, email may still send. Avoid duplicate successful sends.

---

## 8. Required Logs

Log or make inspectable:
- call start/end
- Twilio call SID
- xAI session configured
- transcript save result
- official page research result
- profile save result
- dashboard slug result
- dashboard payload save result
- local call output result
- Gmail send result
- Twilio SMS send result

Do not log secrets.

---

## 9. Development Agent Execution Rules

When a development agent works on this repo:

1. Identify active phase.
2. Read the matching phase plan.
3. Read `docs/langgraph-architecture.md` for the current product architecture graph.
4. Read this file for current decisions.
5. Inspect existing code before proposing changes.
6. Keep changes phase-scoped.
7. Preserve frontend/backend/voice/delivery boundaries.
8. Do not reintroduce external workflow automation unless the user explicitly changes the decision.
9. Use JavaScript for frontend.
10. Use modular Python services for backend.
11. Update docs and `.env.example` when environment variables change.
12. Validate with commands whenever possible.
13. Explain what was tested and what remains.

---

## 10. Current MVP Acceptance

The MVP is acceptable when:
- homepage displays premium phone CTA
- Twilio inbound call reaches Grok voice agent
- caller can interrupt agent and agent listens
- official website is analyzed during the call
- agent shares at least one grounded live company observation
- call transcript is captured
- dashboard payload is saved
- `/dashboard/[client-slug]` renders real data
- local JSON output is saved
- Gmail email sends or logs a safe failure
- Twilio SMS sends or logs a safe failure
- skipped/failed delivery can be retried
- public dashboard never leaks internal transcript
