# Phase 2 - Realtime Voice Agent Plan

## Goal

Build the backend foundation for the realtime inbound Supervisor Voice Agent.

## Stack

- FastAPI
- xAI/Grok realtime voice
- Twilio inbound voice/media stream
- LangGraph behind live path
- SQLite

## Scope

- FastAPI app structure
- Twilio inbound webhook
- Twilio media WebSocket
- xAI realtime session configuration
- runtime prompt loading from `backend/prompts/grok-voice-system-prompt.md`
- tool registry
- `save_dashboard_data`
- `save_call_transcript`
- `create_dashboard_payload`
- `generate_dashboard_slug`
- `analyze_official_page`
- SQLite call/transcript/profile/dashboard records
- public/internal data separation

## Voice Requirements

- one Supervisor Voice Agent only
- warm and human
- ask one question at a time
- handle barge-in
- do public website research quietly
- share one grounded observation while live
- do not mention scraping/tools

## Excludes

- direct Gmail/SMS as final product delivery
- external workflow automation
- CRM
- payment
- booking
- multi-agent live orchestration

## Done When

- inbound call reaches agent
- agent can capture transcript
- official website can be analyzed
- dashboard data can be saved
- SQLite records are linked

