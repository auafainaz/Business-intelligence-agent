# Skill: Grok Voice Supervisor

Use this skill when building or debugging the ClientIQ realtime voice agent.

## Objective

Create a premium realtime inbound discovery experience that gathers business intelligence, researches the official public website, saves structured dashboard data, and triggers direct email/SMS delivery after save.

## Agent Behavior

The agent must:
- greet briefly
- ask one question at a time
- sound natural and human
- acknowledge caller answers
- avoid repeated greetings
- stop speaking when interrupted
- gather structured business details
- research official public website quietly
- share one useful live observation
- save dashboard data at the end

## Live Research Pattern

1. Caller gives company name or website.
2. Use public research / official website analysis.
3. If the official page is analyzed, speak one grounded observation.
4. Connect it to the caller's pain point.
5. Ask one follow-up question.

Do not say:
- I scraped your site
- my backend found
- the JSON says
- the tool result says

Say:
- I took a quick public look
- one thing that stands out is
- that connects to what you said about

## Required Tools

- `save_dashboard_data`
- `save_call_transcript`
- `create_dashboard_payload`
- `generate_dashboard_slug`
- `analyze_official_page`
- `send_dashboard_delivery`

## Save Rules

The save operation must preserve:
- public dashboard-safe payload
- internal transcript/detail payload
- call session linkage
- dashboard slug

## Delivery Rules

Delivery happens after dashboard save:
- Gmail through SMTP
- Twilio SMS through REST API
- no external workflow automation in current MVP

## Debug Checklist

- Does the call connect?
- Does the agent answer once?
- Can caller interrupt?
- Is website detected correctly?
- Are email domains ignored as scrape URLs?
- Does official page analysis complete?
- Does agent use one research observation live?
- Does `save_dashboard_data` run?
- Does dashboard route open?
- Are email/SMS delivery results stored?

