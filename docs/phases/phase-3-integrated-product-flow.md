# Phase 3 - Integrated Product Flow

## Goal

Connect the frontend, Twilio, xAI/Grok realtime voice layer, FastAPI backend, LangGraph, SQLite, dashboard route, Gmail, and Twilio SMS into one working MVP flow.

Current decision: no external workflow automation in the MVP runtime. Email and SMS are sent directly from backend services after the dashboard payload and slug are safely saved.

## Target Flow

```text
Public Website
-> Twilio inbound call
-> xAI/Grok Supervisor Voice Agent
-> FastAPI tool processing
-> LangGraph post-call orchestration
-> SQLite persistence
-> dashboard slug creation
-> dashboard route rendering
-> direct Gmail email
-> direct Twilio SMS
-> local JSON call output
```

## Scope

- Connect frontend dashboard route to real saved backend data
- Persist call sessions, transcripts, client profiles, public dashboard payloads, and internal payloads
- Generate and save dashboard slug
- Run LangGraph post-call intelligence after data is safe
- Save local call JSON under `backend/outputs/calls`
- Send dashboard link by Gmail SMTP
- Send dashboard link by Twilio SMS
- Use idempotency to avoid duplicate successful delivery sends
- Allow delivery retry when credentials or recipient data are fixed
- Preserve partial value when one delivery channel fails

## Current Relevant Files

- `frontend/app/dashboard/[client-slug]/page.js`
- `frontend/.env.example`
- `backend/app/routers/dashboard.py`
- `backend/app/routers/delivery.py`
- `backend/app/routers/twilio.py`
- `backend/app/routers/tools.py`
- `backend/app/services/dashboard_service.py`
- `backend/app/services/post_call_service.py`
- `backend/app/services/delivery_service.py`
- `backend/app/services/local_call_output.py`
- `backend/app/services/official_page_research.py`
- `backend/app/services/transcript_service.py`
- `backend/app/services/slug_service.py`
- `backend/app/db/repository.py`
- `backend/app/db/schema.sql`
- `backend/app/graph/workflow.py`

## Save Order

The product should follow this order:

```text
save first -> dashboard second -> delivery third
```

Delivery must not run before:

- transcript/profile data is accepted
- dashboard payload is saved
- dashboard slug is created
- dashboard URL can be formed

## Delivery Rules

Gmail email should include:

- thank-you note
- dashboard link
- short summary
- quick wins
- next-step CTA

Twilio SMS should include:

- short thank-you
- dashboard link

If email fails, SMS may still send. If SMS fails, email may still send. Failures should be logged safely without deleting dashboard data.

## Environment Variables

Backend delivery uses:

```text
DELIVERY_ENABLED
PUBLIC_BASE_URL
FRONTEND_BASE_URL
GMAIL_USERNAME
GMAIL_APP_PASSWORD
GMAIL_FROM_EMAIL
GMAIL_SMTP_HOST
GMAIL_SMTP_PORT
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER
```

No secrets should be committed.

## Excludes

- external workflow automation
- CRM
- payments
- meeting booking
- outbound campaign logic
- advanced analytics admin panel

## Acceptance Criteria

- A completed call creates a dashboard slug
- `/dashboard/[client-slug]` renders SQLite-backed dashboard data
- Local JSON output is written after the call
- Gmail sends dashboard link or logs a clear safe failure
- Twilio SMS sends dashboard link or logs a clear safe failure
- Duplicate successful sends are avoided
- Public dashboard does not leak internal transcript or private notes
- Official website research appears in dashboard payload when available

## Validation

Run backend and frontend, expose backend through ngrok, configure Twilio Voice webhook, then make a test call.

After the call, verify:

- backend logs show call start/end
- SQLite has call session, transcript, profile, and dashboard payload
- local JSON exists in `backend/outputs/calls`
- dashboard URL opens in frontend
- email delivery result is logged
- SMS delivery result is logged
