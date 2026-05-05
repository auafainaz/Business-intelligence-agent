# ClientIQ

Premium inbound call intelligence platform for converting phone conversations into structured business insights, client-specific dashboards, and direct follow-up by email/SMS.

## Architecture

```text
Public Website
-> Twilio inbound call
-> xAI/Grok realtime Supervisor Voice Agent
-> Official Website Live Research
-> FastAPI Tool Processing
-> LangGraph Post-Call Intelligence
-> SQLite Public/Internal Persistence
-> Dashboard Route
-> Direct Gmail/Twilio SMS Delivery
-> Local JSON Output
```

## Stack

- Frontend: Next.js, JavaScript, Tailwind CSS
- Backend: FastAPI, LangGraph, SQLite
- Realtime voice: xAI/Grok realtime
- Telephony/SMS: Twilio
- Email: Gmail SMTP
- Dashboard route: `/dashboard/[client-slug]`

## Project Docs

- `AGENTS.md` - development and architecture instructions
- `docs/project-blueprint-modified.md` - product blueprint
- `docs/project-phase-plan.md` - phased implementation plan
- `docs/phases/` - detailed phase-by-phase implementation documents
- `docs/langgraph-architecture.md` - architecture graph and Mermaid diagram
- `backend/README.md` - backend setup and run instructions
- `frontend/README.md` - frontend setup and run instructions

## Local Development

Backend:

```powershell
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Frontend:

```powershell
cd frontend
npm run dev
```

## Important

- Do not commit `backend/.env`.
- Do not commit SQLite data, call outputs, `.venv`, `.next`, or `node_modules`.
- Public dashboard data must remain separated from internal transcript and notes.
- External workflow automation is not used in this MVP; Gmail and SMS are sent directly from FastAPI services.
