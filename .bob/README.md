# Bob Setup

This folder contains the project memory Bob should use when developing ClientIQ.

Current MVP decision: **do not use external workflow automation**. Post-call delivery is direct from FastAPI through Gmail SMTP and Twilio SMS.

## Read Order

1. `../AGENTS.md`
2. `../docs/project-blueprint-modified.md`
3. `../docs/project-phase-plan.md`
4. `../docs/langgraph-architecture.md`
5. matching file in `plans/`
6. matching files in `rules/`
7. matching files in `skills/`

## Current Active Focus

Phase 4: development, debugging, and demo readiness.

Main work now:
- stabilize Twilio inbound calls
- improve Grok realtime voice behavior
- validate live official website research
- validate dashboard creation
- validate direct Gmail/Twilio SMS delivery
- keep public/internal data separate
- keep implementation aligned with `docs/langgraph-architecture.svg`

## Bob Style

Bob should work like a careful coding agent:
- inspect first
- make small focused changes
- test or explain why testing is blocked
- update docs when decisions change
- avoid secrets in code or logs
