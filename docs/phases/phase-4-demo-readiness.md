# Phase 4 - Development, Debugging, and Demo Readiness

## Goal

Stabilize the MVP so it can be tested repeatedly and shown to a client with clear setup steps, logs, and known limitations.

Phase 4 is not for adding major new product features. It is for proving that the current system works reliably enough for demos and early feedback.

## Scope

- Repeat live call tests
- Validate ngrok and Twilio webhook setup
- Validate xAI/Grok realtime behavior
- Improve voice naturalness
- Validate barge-in/interruption handling
- Prevent double-speaking and repeated greetings
- Validate official website live research
- Confirm the agent shares one grounded company observation during the call
- Validate dashboard generation from transcript and research
- Validate local JSON output
- Validate Gmail credentials and email delivery
- Validate Twilio SMS delivery
- Document Twilio trial and A2P 10DLC limitations
- Validate delivery retry and duplicate-send prevention
- Validate frontend/backend startup documentation

## Current Relevant Files

- `backend/README.md`
- `frontend/README.md`
- `backend/app/services/xai_twilio_bridge.py`
- `backend/app/services/xai_realtime.py`
- `backend/app/services/official_page_research.py`
- `backend/app/services/delivery_service.py`
- `backend/app/services/local_call_output.py`
- `backend/app/services/post_call_service.py`
- `backend/app/services/integration_logger.py`
- `backend/prompts/grok-voice-system-prompt.md`
- `frontend/app/dashboard/[client-slug]/page.js`

## Demo Checklist

Before a client demo:

- Backend is running
- Frontend is running
- ngrok points to backend port
- Twilio Voice webhook points to ngrok `/api/twilio/inbound`
- Twilio call status callback points to ngrok `/api/twilio/status`
- `PUBLIC_BASE_URL` or backend public URL is current
- `FRONTEND_BASE_URL` points to the dashboard frontend URL
- xAI API key is present
- Twilio credentials are present
- Gmail app password settings are present if email delivery is being demoed
- Twilio SMS limitations are understood for trial or unregistered numbers

## Things To Validate In A Live Call

- Caller hears the agent
- Agent does not repeat the opening
- Agent asks one question at a time
- Caller can interrupt and agent listens
- Company name or website is captured correctly
- Official website is analyzed during the call
- Agent shares one specific public observation
- Agent connects the observation to a pain point
- Agent saves dashboard data
- Dashboard link opens after the call
- Email/SMS result is visible in logs

## Logs To Inspect

Required logs or inspectable events:

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

## Known Platform Notes

- Twilio trial accounts may restrict calls and SMS to verified recipients.
- US SMS may require A2P 10DLC registration for production sending.
- Gmail SMTP requires a Google app password, not the normal account password.
- ngrok URLs can change unless using a reserved domain.
- Dashboard links sent to real clients should use a reachable public frontend URL, not `127.0.0.1`.

## Excludes

- CRM integration
- payment flow
- meeting booking
- outbound campaigns
- external workflow automation
- advanced analytics admin panel
- large redesigns

## Acceptance Criteria

- A fresh local startup can be followed from README instructions
- Repeated test calls produce stable logs
- At least one call produces a dashboard URL
- Dashboard renders public-safe data
- Local call JSON is saved
- Email and SMS either send or fail safely with clear reasons
- The demo story is explainable without exposing internal implementation details
