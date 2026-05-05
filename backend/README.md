# ClientIQ Backend

FastAPI backend for the ClientIQ inbound realtime voice intelligence MVP.

Current runtime flow:

```text
Twilio inbound call
-> FastAPI Twilio webhook
-> Twilio media WebSocket
-> xAI/Grok realtime voice bridge
-> backend tool processing
-> LangGraph intelligence workflow
-> SQLite persistence
-> dashboard lookup API
-> direct Gmail email + Twilio SMS delivery
-> local JSON call output
```

Current decision: external workflow automation is not used in this MVP. Gmail and SMS delivery are sent directly by backend services after the dashboard payload and slug are saved.

## Implemented

- FastAPI app structure
- SQLite persistence for calls, transcripts, client profiles, dashboard payloads, and delivery records
- Twilio inbound webhook and bidirectional media stream bridge
- xAI/Grok realtime session configuration
- runtime prompt loading from `backend/prompts/grok-voice-system-prompt.md`
- realtime tool registry and dispatcher
- official public website analysis during calls
- LangGraph workflow behind the live voice path
- dashboard payload lookup by slug
- local call output JSON in `backend/outputs/calls`
- direct Gmail SMTP post-call email delivery
- direct Twilio SMS dashboard delivery
- delivery idempotency and retry for skipped/failed sends

## Not In MVP

- external workflow automation
- CRM integration
- payment flow
- booking flow
- outbound campaigns
- advanced analytics admin panel

## Local Run

Start the backend in one PowerShell terminal:

```powershell
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Start ngrok in a second PowerShell terminal. If you keep `ngrok.exe` in `C:\ngrok`, use:

```powershell
cd C:\ngrok
.\ngrok.exe http 8000
```

If you use the portable ngrok installed under your user profile, use:

```powershell
& "$env:LOCALAPPDATA\Programs\ngrok\ngrok.exe" http 8000
```

Copy the HTTPS forwarding URL from ngrok and set it in `backend/.env`:

```env
PUBLIC_BASE_URL=https://YOUR-NGROK-DOMAIN
```

Then set the Twilio voice webhook to:

```text
POST https://YOUR-NGROK-DOMAIN/api/twilio/inbound
```

The SQLite database is initialized on app startup.

## Required `.env` Values

Core:

```env
PUBLIC_BASE_URL=https://YOUR-NGROK-DOMAIN
FRONTEND_BASE_URL=http://127.0.0.1:3000
DATABASE_PATH=backend/data/clientiq.sqlite3
LOCAL_CALL_OUTPUT_DIR=backend/outputs/calls
XAI_API_KEY=
XAI_REALTIME_MODEL=grok-voice-think-fast-1.0
XAI_REALTIME_VOICE=ara
```

Twilio voice/SMS:

```env
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=+12295474585
```

Gmail delivery:

```env
GMAIL_USERNAME=
GMAIL_APP_PASSWORD=
GMAIL_FROM_EMAIL=
GMAIL_SMTP_HOST=smtp.gmail.com
GMAIL_SMTP_PORT=587
DELIVERY_ENABLED=true
```

Use a Google App Password without spaces. Do not use your normal Gmail password.

## Twilio Webhook

Set the Twilio voice webhook to:

```text
POST https://YOUR-NGROK-DOMAIN/api/twilio/inbound
```

Inbound SMS webhook is not required for current MVP dashboard delivery.

## Useful Endpoints

```text
GET  /api/health
GET  /api/realtime/session-config
POST /api/twilio/inbound
WS   /api/twilio/media
POST /api/tools/save-dashboard-data
GET  /api/dashboard/{dashboard_slug}
POST /api/automation/post-call
POST /api/delivery/send-email
POST /api/delivery/send-sms
POST /api/delivery/send-dashboard
GET  /api/delivery/{dashboard_slug}
```

## Local Call Outputs

After each completed realtime call, the backend saves a local JSON summary here:

```text
backend/outputs/calls/{call_session_id}.json
```

The file includes:
- call metadata
- captured transcript segments
- realtime tool results
- official page analysis results
- dashboard details
- delivery results when available

## Debug Notes

If dashboard works but email/SMS does not, check:
- backend restarted after `.env` changes
- Gmail app password has no spaces
- Twilio trial recipient is verified
- US SMS/A2P rules for reliable delivery
- delivery records at `/api/delivery/{dashboard_slug}`
- backend terminal logs for Gmail/Twilio send result
