# Rule: Core Bob Behavior

## Current Architecture Rule

ClientIQ uses direct backend delivery. Do not add external workflow automation unless the user explicitly reverses the decision.

## Core Rules

1. Identify the active phase before acting.
2. Check `docs/langgraph-architecture.md` before changing architecture or cross-layer flow.
3. Keep changes small and focused.
4. Work on one phase at a time.
5. Keep frontend, telephony, realtime AI, backend tools, storage, dashboard, and delivery separate.
6. Never expose credentials, secrets, or raw tokens.
7. Never invent caller or business details.
8. Validate structured outputs before saving.
9. Keep public dashboard data separate from internal transcript/details.
10. Prefer a working MVP over a large architecture.
11. Validate changes with commands whenever possible.

## Current Delivery Rule

Email and SMS are sent directly by FastAPI services after dashboard payload and slug are saved.
