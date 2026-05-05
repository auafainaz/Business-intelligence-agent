# Fainaz ClientIQ LangGraph Architecture

This document shows the current end-to-end architecture as a LangGraph-style flow.

Runtime rule: this graph describes the product architecture. The live call path must stay thin; heavy intelligence runs behind the live voice layer.

![Fainaz ClientIQ LangGraph Architecture](./langgraph-architecture.svg)

```mermaid
flowchart TD
    A[Public Website<br/>Premium phone CTA]
    B[Twilio Inbound Voice<br/>Webhook + media stream]
    C[xAI/Grok Realtime<br/>Supervisor Voice Agent]
    D[Official Website Live Research<br/>Public page analysis only]
    E[FastAPI Tool Processing<br/>save_dashboard_data + tools]
    F[LangGraph Post-Call Intelligence<br/>transcript + enrichment + recommendations]
    G[SQLite Persistence<br/>public and internal records separated]
    H[Dashboard Route<br/>/dashboard/client-slug]
    I[Direct Delivery<br/>Gmail SMTP + Twilio SMS]
    J[Local JSON Output<br/>backend/outputs/calls]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J
```

## LangGraph Modules

Backend graph files:

- `backend/app/graph/workflow.py`  
  Runtime intelligence graph used by save/transcript flows.

- `backend/app/graph/architecture.py`  
  Project architecture graph used for planning, documentation, and architecture validation.

## Runtime Intelligence Graph

```mermaid
flowchart TD
    A[transcript_intelligence]
    B[business_enrichment]
    C[dashboard_payload]
    D[END]

    A --> B --> C --> D
```

## Project Architecture Graph Nodes

1. `public_website`
2. `twilio_inbound`
3. `realtime_voice`
4. `live_research`
5. `backend_tools`
6. `intelligence_workflow`
7. `sqlite_persistence`
8. `dashboard_route`
9. `direct_delivery`
10. `local_output`

## Validation Command

From `backend`:

```powershell
@'
from app.graph.architecture import run_project_architecture_graph

result = run_project_architecture_graph()
print(result["stage_log"])
print("dashboard_ready:", result["public_dashboard_ready"])
print("internal_ready:", result["internal_record_ready"])
print("delivery_ready:", result["delivery_ready"])
'@ | .\.venv\Scripts\python.exe -
```
