# Business Intelligence Inbound Call Realtime Agent — Bob Setup Pack

This package contains the initial markdown and configuration files to set up IBM BoB for a business-intelligence-focused inbound realtime voice agent project.

## Included
- `AGENTS.md` — master project instructions
- `.bob/custom_modes.yaml` — custom Bob modes
- `.bob/mcp.json` — MCP starter configuration
- `.bob/rules/` — behavioral rules
- `.bob/skills/` — reusable project skills
- `.bob/plans/` — phased implementation blueprints

## How to Use
1. Copy these files into your project root.
2. Review `AGENTS.md` and replace any placeholders with your exact stack decisions.
3. Enable only the MCP servers you truly need.
4. Start in Plan mode and reference the relevant phase plan.
5. Approve the plan before switching to Code mode.

## Suggested First Prompt in Plan Mode
"Review `AGENTS.md` and `.bob/plans/01-phase-1-inbound-foundation.md`. Produce an implementation checklist for Phase 1 only, including files to create, test strategy, and assumptions to confirm before coding."
