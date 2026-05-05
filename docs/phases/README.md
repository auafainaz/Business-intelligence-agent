# ClientIQ Phase Documents

These files split the project plan into detailed implementation phases for client handoff and future development.

Read in this order:

1. `phase-1-frontend.md`
2. `phase-2-realtime-voice-agent.md`
3. `phase-3-integrated-product-flow.md`
4. `phase-4-demo-readiness.md`

Use these together with:

- `../project-blueprint-modified.md`
- `../project-phase-plan.md`
- `../langgraph-architecture.md`
- `../../AGENTS.md`

Current MVP decision: external workflow automation is not part of runtime. Post-call delivery is handled directly by FastAPI through Gmail SMTP and Twilio SMS.
