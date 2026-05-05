# Phase 3 - Integrations Plan

## Goal

Connect all product layers into one working end-to-end MVP without external workflow automation.

## Current Architecture

Reference diagram:

- `docs/langgraph-architecture.md`
- `docs/langgraph-architecture.svg`

```text
Frontend
-> Twilio inbound call
-> xAI/Grok realtime voice
-> FastAPI tool processing
-> LangGraph post-call workflows
-> SQLite persistence
-> dashboard route
-> direct Gmail email
-> direct Twilio SMS
```

## Scope

### Frontend
- dashboard route `/dashboard/[client-slug]` loads saved backend data
- partial data renders gracefully
- premium UI is preserved

### Twilio
- inbound voice webhook connected
- media stream connected
- call metadata captured
- SMS dashboard delivery sent through backend service

### xAI/Grok
- realtime session configured
- prompt injected
- tools registered
- barge-in behavior supported
- official website analysis used live

### FastAPI
- routes and services connected
- `save_dashboard_data` persists full flow
- direct delivery endpoint available
- provider credentials read from `.env`

### LangGraph
- transcript intelligence
- enrichment
- dashboard payload assembly
- next-step recommendations
- stays behind live voice path

### SQLite
- call sessions
- transcripts
- client profiles
- dashboard payloads
- delivery records
- lookup dashboard by slug

### Direct Delivery
- Gmail SMTP email after dashboard save
- Twilio SMS after dashboard save
- no duplicate successful sends
- skipped/failed records can retry

## Excludes

- external workflow automation
- CRM
- payment
- booking
- outbound campaigns
- advanced analytics admin panel

## Required Logs

- call start/end
- transcript save
- official page research
- profile save
- dashboard slug
- dashboard payload save
- local call output
- Gmail send result
- Twilio SMS send result

## Done When

- call creates dashboard
- dashboard route opens
- local JSON output is saved
- email sends or logs clear failure
- SMS sends or logs clear failure
- public dashboard does not leak internal data

