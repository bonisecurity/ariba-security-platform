# Ariba Security Platform - Architecture

## Overview

Ariba Security Platform is a modular, enterprise-grade security platform designed for endpoint detection, investigation, and response. The platform follows a component-based architecture that collects telemetry, detects threats, and enables coordinated incident response.

## Architecture Diagram - Ariba SIEM

```text
               ┌──────────────────────────────────────────────────────────────┐
               │                    Data Sources                                │
               │ Windows │ Linux │ Firewall │ MikroTik │ Apps │ APIs │ Cloud │
               └──────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
               ┌──────────────────────────────────────────────────────────────┐
               │                    Ariba Agent                                 │
               │   Windows/Linux Enrollment │ HTTP Events │ Syslog │ Webhooks │
               └─────────────────────►──────────────────────────────────────┘
                                  │
                                  ▼
               ┌──────────────────────────────────────────────────────────────┐
               │                       Queue / Event Buffer                   │
               │                    Redis Streams → Apache Kafka              │
               └─────────────────────►──────────────────────────────────────┘
                                  │
                                  ▼
               ┌──────────────────────────────────────────────────────────────┐
               │                       Ariba Manager                            │
               │  │           │           │           │           │           │  │
               │  │           │           │           │           │           │  │
               │  ▼           ▼           ▼           ▼           ▼           ▼  │
               │┌────────────┐┌────────────┐┌────────────┐┌────────────┐┌────────────┐│
               ││Agent Mgr   ││Event Rcvr  ││Norm Engine ││Decoder Eng ││Detect Eng  ││
               │├────────────┤├────────────┤├────────────┤├────────────┤├────────────┤│
               │││Event Norm  │││Decoder Eng │││Risk Engine │││Correlation │││Alert Mgr   ││
               │├────────────┤├────────────┤├────────────┤├────────────┤├────────────┤│
               │││Detection   │││Risk Engine │││MITRE ATT&CK│││Incident Mgr│││Response/   ││
               │├────────────┤├────────────┤├────────────┤├────────────┤├────────────┤│
               ││Engine      │││MITRE ATT&CK│││Threat Intl │││Automation  │││Engine      ││
               │└────────────┘└────────────┘└────────────┘└────────────┘└────────────┘│
               │  │           │           │           │           │           │  │
               │  └───────►────►───────►──────►──────►──────►──────►──────┘  │
               │                       Event Flow                               │
               └──────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
               ┌──────────────────────────────────────────────────────────────┐
               │                       Ariba Indexer                            │
               │              OpenSearch / ClickHouse                           │
               │              Events │ Alerts │ Incidents                      │
               └─────────────────────►──────────────────────────────────────┘
                                  │
                                  ▼
               ┌──────────────────────────────────────────────────────────────┐
               │                       Ariba Dashboard                            │
               │  ┌─────────────┼─────────────┐ ┌─────────────┼─────────────┐ │
               │  │             │             │ │             │             │ │
               │  │  Alerts     │ Threat Hunt │ │  Reports    │  Analytics  │ │
               │  └─────────────┼─────────────┘ └─────────────┼─────────────┘ │
               │               │                       │             │       │
               └──────────────────────────────────────────────────────────────┘
```

## Component-Wise Language Recommendations

| Ariba Component | Recommended Language | Rationale |
|---|---|---|
| **Ariba Agent** | **Rust** | Memory safety, cross-platform binary, low resource footprint, FIM performance |
| **Ariba Manager** | **Go** | Concurrency, microservices, fast compilation, built-in HTTP server, easy deployment |
| **Ariba Detection Engine** | **Go** | High-performance rule matching, concurrent rule evaluation, easy deployment |
| **Ariba Decoders** | **Go + YAML** | Fast log parsing, YAML rule integration, native Go performance, simple deployment |
| **Ariba Rules** | **YAML** | Human-readable, version-controlled, easy modification without code changes, schema validation |
| **Ariba Correlation Engine** | **Go** | Time-window correlation, attack-chain detection, high-performance event processing |
| **Ariba Indexer** | **OpenSearch/ClickHouse** (initially) | Distributed search, scalability, time-series data handling, SQL on ClickHouse |
| **Ariba Dashboard** | **Next.js + React + TypeScript** | Modern web UI, reactive components, TypeScript safety, ecosystem maturity |
| **Ariba API** | **Go** | Consistent with manager, fast HTTP routing, built-in OpenAPI generation |
| **AI/ML Engine** | **Python** | Rich ML ecosystem (scikit-learn, tensorflow, pytorch), easy prototyping, Jupyter integration |
| **Database metadata** | **PostgreSQL** | Relational data, ACID transactions, JSONB for flexible schemas, mature ecosystem |
| **Message Queue** | **NATS / Kafka** | High-performance pub/sub, Kafka for enterprise scale, NATS for simpler deployments |
| **Wazuh → Ariba mapping** | **Go** | Protocol conversion, maintainability, performance |
| **Wazuh Agent → Ariba Agent** | **Rust** | Memory safety, cross-platform, low footprint |
| **Wazuh Manager → Ariba Manager** | **Go** | Microservices alignment, concurrent processing |
| **Wazuh Indexer → Ariba Indexer** | **OpenSearch** | Data pipeline compatibility |
| **Wazuh Dashboard → Ariba Dashboard** | **Next.js** | UI framework consistency |
| **Wazuh Rules → Ariba Rules** | **YAML** | Rule format continuity |
| **Wazuh Decoders → Ariba Decoders** | **Go + YAML** | Decoder format continuity |

## Modular Ariba Manager Architecture

The Ariba Manager is **not** a simple Wazuh clone. It is a independently designed, modular component:

```text
┌──────────────────────────────────────────────────────────────┐
│                    Ariba Manager (Modular)                   │
│                                                              │
│  ├── Agent Manager           │ Manages agent enrollment,       │
│  │                           │    heartbeat, config,          │
│  │                           │    security (mTLS, JWT)       │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Event Receiver          │ Receives events from:         │
│  │                           │  - Ariba Agent (HTTP/Syslog)  │
│  │                           │  - Wazuh Manager (conversion) │
│  │                           │  - Syslog UDP/TCP             │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Event Normalizer        │ Standardizes events to        │
│  │                           │  Ariba event schema           │
│  │                           │  - Field mapping              │
│  │                           │  - Data enrichment            │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Decoder Engine          │ Parses raw logs using:        │
│  │                           │  - YAML-based decoder configs │
│  │                           │  - JSON, Syslog, Linux auth   │
│  │                           │  - Windows Event, nginx, etc. │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Detection Engine        │ Evaluates detection rules:    │
│  │                           │  - YAML rule matching         │
│  │                           │  - Regex, contains, exists    │
│  │                           │  - Positive/negative samples  │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Risk Engine             │ Calculates risk scores:       │
│  │                           │  - Based on severity, MITRE   │
│  │                           │  - Asset criticality, time    │
│  │                           │  - Correlation factors        │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Correlation Engine      │ Runs time-window correlation: │
│  │                           │  - Attack-chain detection     │
│  │                           │  - Event grouping             │
│  │                           │  - Deduplication              │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Alert Manager           │ Creates and manages alerts:   │
│  │                           │  - Alert generation           │
│  │                           │  - Severity calculation       │
│  │                           │  - Notification (email, Teams│
│  │                           │    Slack, Telegram)           │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Incident Manager        │ Creates and manages incidents:│
│  │                           │  - Alert-to-incident linking  │
│  │                           │  - Ownership, comments,       │
│  │                           │  - Evidence, timeline         │
│  │                           │  - L1/L2 escalation workflow  │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── Threat Intelligence     │ Enriches events with:         │
│  │                           │  - OTX, VirusTotal, MISP      │
│  │                           │  - IP reputation, geolocation │
│  │                           │  - CVE, exploit info          │
│  └───────────────►──────────┘                              │
│                                                              │
│  ├── MITRE ATT&CK Engine     │ Maps detections to:           │
│  │                           │  - Tactics and techniques     │
│  │                           │  - ATT&CK IDs (T1059, T1190) │
│  │                           │  - Mitigation mappings        │
│  └───────────────►──────────┘                              │
│                                                              │
│  └── Response/Automation Engine │ Executes approved actions:   │
│                                   │  - Block IP, isolate host     │
│                                   │  - Kill process, disable user │
│                                   │  - Dry-run mode, audit log    │
│                                   └───────────────────────────────┘
└──────────────────────────────────────────────────────────────┘
```

## Key Differences from Wazuh

| Aspect | Wazuh | Ariba |
|---|---|---|
| **Architecture** | Monolithic (mostly) | Modular, microservice-inspired |
| **Language** | Primarily Go + some Python | Go for services, Rust for agent, Python for AI/ML |
| **Agent** | C-based | Rust (memory safety, cross-platform) |
| **Rules** | XML/SOML/YAML | YAML with comprehensive schema |
| **Indexer** | Elasticsearch | OpenSearch + ClickHouse option |
| **Dashboard** | Custom React | Next.js + React + TypeScript |
| **Deployment** | Docker/K8s | Docker Compose + Kubernetes planned |
| **Extensibility** | Plugins | Modular components, well-defined interfaces |
| **MITRE Mapping** | Built-in | Comprehensive engine with validation |

## Technology Stack Summary

| Layer | Technology |
|---|---|
| API and manager | Python 3.12, FastAPI, Pydantic (initial), Go (modular) |
| Database access | SQLAlchemy, Alembic |
| Background processing | Celery |
| Message queue | Redis Streams initially; NATS/Kafka for higher scale |
| Relational data | PostgreSQL |
| Event search and analytics | OpenSearch, ClickHouse |
| Web dashboard | Next.js, TypeScript, Tailwind CSS |
| Live updates | WebSocket |
| Reverse proxy | Nginx |
| Platform monitoring | Prometheus, Grafana |
| Deployment | Docker Compose; Kubernetes planned |
| Agent | Rust (cross-platform, memory-safe) |
| AI/ML | Python (scikit-learn, tensorflow, pytorch) |

## Getting Started

### Quick Start

```bash
# Clone the repository
git clone https://github.com/bonisecurity/ariba-security-platform.git
cd ariba-security-platform

# Copy environment example
cp .env.example .env

# Start the platform
docker compose up -d --build
```

### Development Workflow

1. **Add a new decoder** - Create YAML config in `ariba-ruleset/decoders/` and Python module in `ariba-manager/decoders/`
2. **Create a detection rule** - Add YAML rule to `ariba-ruleset/rules/` with schema validation
3. **Extend the manager** - Add new modular component following the architecture above
4. **Update the dashboard** - Add new views in `ariba-dashboard/src/`
5. **Run tests** - `pytest ariba-manager/tests/ -v`

## Future Enhancements

- [ ] gRPC communication between manager components
- [ ] WebAssembly (Wasm) for edge/deployable rules
- [ ] Service mesh (Istio/Linkerd) for component communication
- [ ] Plugin system for third-party integrations
- [ ] Advanced AI/ML threat detection pipeline
- [ ] Multi-tenant isolation at component level