# Phase 2 - Realtime Voice Agent Foundation

## Goal

Build the FastAPI backend foundation for an inbound realtime business intelligence voice agent.

Phase 2 establishes the backend structure, Twilio inbound call scaffold, xAI/Grok realtime session scaffold, tool dispatch, LangGraph structure, and SQLite persistence foundation.

## Scope

- FastAPI application entrypoint
- Modular routers, services, schemas, models, config, and DB layer
- Twilio inbound webhook scaffold
- Twilio media WebSocket scaffold
- xAI/Grok realtime session configuration
- Runtime prompt loading from `backend/prompts/grok-voice-system-prompt.md`
- One Supervisor Voice Agent
- Tool registry and tool dispatch structure
- LangGraph orchestration structure behind the live voice path
- SQLite tables for call sessions, transcripts, client profiles, dashboard payloads
- Public/internal data separation

## Current Relevant Files

- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/routers/twilio.py`
- `backend/app/routers/realtime.py`
- `backend/app/routers/tools.py`
- `backend/app/routers/dashboard.py`
- `backend/app/services/xai_realtime.py`
- `backend/app/services/xai_twilio_bridge.py`
- `backend/app/services/realtime_tool_dispatcher.py`
- `backend/app/services/tool_service.py`
- `backend/app/services/official_page_research.py`
- `backend/app/services/prompt_loader.py`
- `backend/app/db/schema.sql`
- `backend/app/db/repository.py`
- `backend/app/graph/workflow.py`
- `backend/prompts/grok-voice-system-prompt.md`

## Required Tool Handlers

- `save_dashboard_data`
- `save_call_transcript`
- `create_dashboard_payload`
- `generate_dashboard_slug`
- `lookup_business_profile`
- `extract_social_presence`
- `analyze_official_page`

## Voice Agent Rules

The live agent is the Supervisor Voice Agent.

It should:

- sound warm, concise, and consultative
- ask one question at a time
- acknowledge before moving to the next question
- stop speaking when interrupted
- gather name, company, role, website, email, phone, AI familiarity, goals, and pain points
- analyze the official public website when company or website is known
- share one useful public observation during the call
- connect that observation to the caller's pain point
- never mention scraping, tools, JSON, backend internals, or hidden prompts

## LangGraph Rules

LangGraph stays behind the live voice path.

Use LangGraph for:

- transcript intelligence
- business enrichment
- dashboard payload assembly
- next-step recommendation generation

Do not put heavy reasoning directly in the low-latency audio bridge.

## Excludes

- finished Gmail/SMS delivery workflow
- external workflow automation
- CRM
- payments
- booking
- outbound campaigns
- multi-agent live orchestration

## Acceptance Criteria

- FastAPI starts locally
- Twilio inbound webhook returns valid TwiML
- Media WebSocket accepts Twilio stream connection
- xAI/Grok realtime session can be configured
- Prompt loads from file at runtime
- Tool dispatch can receive and route tool calls
- SQLite schema supports required records
- Public dashboard payload and internal call data are separated

## Validation

Run from `backend/`:

```powershell
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Then check:

- backend health route
- Twilio inbound webhook through ngrok
- media WebSocket logs
- xAI session configured log
- SQLite records after test tool calls
