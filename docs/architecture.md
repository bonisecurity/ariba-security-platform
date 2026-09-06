# Ariba Security Platform - Architecture

## Overview

Aria Security Platform is a modular, enterprise-grade security platform designed for endpoint detection, investigation, and response. The platform follows a component-based architecture that collects telemetry, detects threats, and enables coordinated incident response.

## Component Diagram

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        Data Sources                                 │
│ Windows │ Linux │ Firewall │ MikroTik │ Apps │ APIs │ Cloud │ DNS │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Ariba Agent / Ingestion Gateway                  │
│              Enrollment │ HTTP Events │ Syslog │ Webhooks           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Queue / Event Buffer                          │
│                    Redis Streams → Apache Kafka                     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Ariba Manager                                 │
│ Validate → Decode → Normalize → Enrich → Detect → Correlate → Alert │
└───────────────┬───────────────────────┬────────────────────────────┘
                │                        │
                ▼                        ▼
┌──────────────────────────┐  ┌──────────────────────────────────────┐
│      Ariba Indexer       │  │             PostgreSQL               │
│ Events │ Alerts │ Search │  │ Users │ Config │ Workflow │ Audit    │
└───────────────┬──────────┘  └──────────────────┬───────────────────┘
                │                                │
                └────────────────┬───────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Ariba Dashboard                             │
│ Overview │ Hunting │ Alerts │ Incidents │ Agents │ Rules │ Reports │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Ariba Response                              │
│          Approval │ Block IP │ Isolate Host │ Quarantine            │
└─────────────────────────────────────────────────────────────────────┘
```

## Core Components

| Component | Responsibility | Primary Technology |
|---|---|---|
| **Ariba Agent** | Collect endpoint logs, inventory, FIM, and telemetry | Python for MVP; Go/Rust may be evaluated later |
| **Ariba Manager** | Decode, normalize, enrich, detect, correlate, and create alerts | Python, FastAPI, Celery |
| **Ariba Indexer** | Store, search, aggregate, and retain security events | OpenSearch |
| **Ariba Dashboard** | Monitoring, hunting, investigation, and administration | Next.js, TypeScript |
| **Ariba Response** | Manage approved manual and automated response actions | Python, FastAPI |
| **Ariba Ruleset** | Store decoders, detection rules, correlation rules, and schemas | YAML, JSON Schema |

## Event Processing Pipeline

```text
Receive
  → Authenticate source
  → Validate payload
  → Preserve raw event
  → Select decoder
  → Normalize fields
  → Enrich asset, identity, and threat context
  → Evaluate detection rules
  → Run time-window correlation
  → Suppress or deduplicate
  → Generate alert
  → Index event and alert
  → Notify or request response approval
```

## Technology Stack

| Layer | Technology |
|---|---|
| API and manager | Python 3.12, FastAPI, Pydantic |
| Database access | SQLAlchemy, Alembic |
| Background processing | Celery |
| Message queue | Redis Streams initially; Kafka for higher scale |
| Relational data | PostgreSQL |
| Event search and analytics | OpenSearch |
| Web dashboard | Next.js, TypeScript, Tailwind CSS |
| Live updates | WebSocket |
| Reverse proxy | Nginx |
| Platform monitoring | Prometheus, Grafana |
| Deployment | Docker Compose; Kubernetes planned |