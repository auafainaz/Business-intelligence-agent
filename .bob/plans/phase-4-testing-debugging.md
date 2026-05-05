# Phase 4 - Testing and Debugging Plan

## Goal

Stabilize ClientIQ for repeatable demos and early user testing.

## Full Chain To Validate

Use `docs/langgraph-architecture.md` and `docs/langgraph-architecture.svg` as the expected architecture map.

```text
Frontend
-> Twilio inbound call
-> xAI/Grok realtime Supervisor Voice Agent
-> live official website analysis
-> FastAPI + LangGraph save pipeline
-> SQLite persistence
-> dashboard route
-> direct Gmail email
-> direct Twilio SMS
-> local JSON output
```

## Testing Areas

### Frontend
- homepage loads
- phone CTA visible
- dashboard valid slug renders
- dashboard invalid slug renders gracefully
- mobile/desktop responsive

### Twilio
- correct voice webhook URL
- ngrok public URL works
- call metadata reaches backend
- media WebSocket opens
- trial/A2P/verified-number limitations understood

### Voice Agent
- answers once
- natural greeting
- one question at a time
- no double talking
- barge-in works
- company name/website captured
- official website analysis happens
- agent says one specific research-based observation live

### Backend Save
- transcript saved
- profile saved
- dashboard slug generated
- public payload saved
- internal payload saved
- local JSON output saved

### Dashboard
- route loads from SQLite-backed data
- company analysis appears
- pain points appear
- improvement tips appear
- no raw transcript public leak

### Direct Delivery
- Gmail app password configured
- email sends to saved recipient
- Twilio SMS sends to saved phone/caller fallback
- duplicate sends are prevented
- skipped/failed sends can retry

## Debug Commands

Backend:

```powershell
cd backend
uvicorn app.main:app --reload
```

Frontend:

```powershell
cd frontend
npm run dev
```

Check dashboard API:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/dashboard/CLIENT-SLUG
```

## Common Failure Causes

- backend not restarted after `.env` change
- ngrok URL not updated in Twilio or `.env`
- Twilio trial recipient not verified
- US SMS requires A2P 10DLC for reliable sending
- Gmail app password has spaces or wrong account
- caller did not provide usable email/phone
- spoken email detected as website URL
- frontend/backend running on different base URLs

## Done When

- three repeated calls succeed
- website research happens during call
- agent uses research naturally
- dashboard link opens
- local JSON explains call result
- email and SMS either send or fail safely with clear logs
- no stale external workflow automation requirements exist in active MVP docs/code
