# Ariba Security Platform

> An open-source, modular EDR, XDR, SIEM, threat detection, and incident response platform.

Ariba Security Platform is being developed to help security teams collect endpoint and infrastructure telemetry, detect suspicious activity, investigate alerts, manage incidents, and coordinate response from one centralized interface.

The project follows a component-based architecture inspired by established security platforms, while implementing its own manager, event schema, detection rules, APIs, agent, response workflow, and dashboard.

> [!IMPORTANT]
> Ariba Security Platform is currently under active development. It is not yet recommended for production security monitoring or automated response.

## Vision

The long-term goal is to provide a transparent and extensible security platform that can operate as:

- **EDR** — Endpoint Detection and Response
- **XDR** — Extended Detection and Response across endpoint, network, identity, cloud, and application sources
- **SIEM** — Centralized log collection, search, correlation, alerting, and reporting
- **Incident Response Platform** — Investigation, escalation, evidence, response, and audit workflows

## Core Capabilities

### SIEM

- Centralized event and log ingestion
- HTTP API and Syslog TCP/UDP collection
- Structured event normalization
- YAML-based detection rules
- Multi-event correlation
- Alert suppression and deduplication
- Full-text and field-based event search
- Retention and index lifecycle management
- Security dashboards and operational reporting

### EDR

- Windows and Linux endpoint telemetry
- Agent enrollment and heartbeat monitoring
- File Integrity Monitoring (FIM)
- Process, service, port, user, and software inventory
- Authentication and privilege activity monitoring
- Local event buffering during connection loss
- Secure remote configuration
- Approved endpoint response actions

### XDR

- Endpoint, identity, network, application, firewall, DNS, web, and cloud telemetry
- Cross-source event correlation
- Threat-intelligence enrichment
- Asset and identity context
- MITRE ATT&CK mapping
- Attack-chain investigation
- Unified alert and incident timeline

### Security Operations

- Real-time alert monitoring
- Severity and risk scoring
- Alert ownership and analyst notes
- True Positive, False Positive, and Benign Positive verdicts
- L1-to-L2 escalation workflow
- Incident creation and alert linking
- SLA, MTTA, and MTTR measurement
- Email, Microsoft Teams, Slack, Telegram, and webhook notifications
- Complete administrative and analyst audit trail

## Platform Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         Data Sources                                │
│ Windows │ Linux │ Firewall │ MikroTik │ Apps │ APIs │ Cloud │ DNS │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Ariba Agent / Ingestion Gateway                  │
│              Enrollment │ HTTP Events │ Syslog │ Webhooks           │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Queue / Event Buffer                          │
│                    Redis Streams → Apache Kafka                     │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Ariba Manager                               │
│ Validate → Decode → Normalize → Enrich → Detect → Correlate → Alert │
└───────────────┬────────────────────────┬────────────────────────────┘
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

## Components

| Component | Responsibility | Primary technology |
|---|---|---|
| **Ariba Agent** | Collect endpoint logs, inventory, FIM, and telemetry | Python for MVP; Go/Rust may be evaluated later |
| **Ariba Manager** | Decode, normalize, enrich, detect, correlate, and create alerts | Python, FastAPI, Celery |
| **Ariba Indexer** | Store, search, aggregate, and retain security events | OpenSearch |
| **Ariba Dashboard** | Monitoring, hunting, investigation, and administration | Next.js, TypeScript |
| **Ariba Response** | Manage approved manual and automated response actions | Python, FastAPI |
| **Ariba Ruleset** | Store decoders, detection rules, correlation rules, and schemas | YAML, JSON Schema |

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

## Example Normalized Event

```json
{
  "@timestamp": "2026-09-06T14:30:00Z",
  "event": {
    "id": "01KEXAMPLEEVENT",
    "category": "web",
    "type": "access",
    "action": "http_request",
    "outcome": "blocked"
  },
  "agent": {
    "id": "001",
    "name": "web-server-01",
    "ip": "10.24.66.20"
  },
  "source": {
    "ip": "10.24.50.129"
  },
  "destination": {
    "ip": "10.24.66.20",
    "port": 443
  },
  "http": {
    "request": {
      "method": "GET"
    },
    "url": "/products?id=1%27%20OR%201=1",
    "response": {
      "status_code": 403
    }
  },
  "observer": {
    "product": "nginx"
  }
}
```

## Example Detection Rule

```yaml
id: ARIBA-WEB-1001
name: Possible SQL Injection Attempt
version: 1
enabled: true
severity: high

match:
  all:
    - field: event.category
      operator: equals
      value: web
    - field: http.url
      operator: regex
      value: "(?i)(union\\s+select|or\\s+1=1|sleep\\(|information_schema)"

groups:
  - web_attack
  - sqli
  - owasp

mitre:
  tactic: Initial Access
  technique_id: T1190

actions:
  create_alert: true
  notify: false
```

## Repository Structure

```text
ariba-security-platform/
├── ariba-manager/          # Detection engine and management API
├── ariba-indexer/          # OpenSearch templates, pipelines, and policies
├── ariba-dashboard/        # SOC web interface
├── ariba-agent/            # Windows/Linux endpoint agent
├── ariba-ruleset/          # Decoders, detection, and correlation rules
├── ariba-response/         # Approved response-action service
├── deployment/             # Docker, Nginx, systemd, and Kubernetes files
├── monitoring/             # Prometheus and Grafana configuration
├── scripts/                # Setup, migration, backup, and maintenance tools
├── docs/                   # Architecture and operational documentation
├── tests/                  # Integration, security, performance, and E2E tests
├── docker-compose.yml
├── .env.example
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Project Status

The project is in the **architecture and early implementation stage**.

The first supported end-to-end milestone is:

```text
Agent/API
  → Event ingestion
  → Nginx/JSON/Syslog decoder
  → Common event normalization
  → YAML rule engine
  → SQL injection alert
  → OpenSearch indexing
  → Alert query API
```

### Current priorities

- [ ] Repository and development environment
- [ ] Manager health and readiness APIs
- [ ] PostgreSQL, Redis, and OpenSearch integration
- [ ] Agent enrollment and authentication
- [ ] Single and bulk event ingestion
- [ ] Decoder registry and normalized event schema
- [ ] YAML rule schema, loader, and matcher
- [ ] Alert generation and indexing
- [ ] Initial alert API
- [ ] Automated tests and example event generator

## Quick Start

Quick-start commands will become available after the first runnable release.

The planned local workflow is:

```bash
git clone https://github.com/OWNER/ariba-security-platform.git
cd ariba-security-platform
cp .env.example .env
docker compose up -d --build
```

Planned service endpoints:

| Service | Default local endpoint |
|---|---|
| Dashboard | `https://localhost:8443` |
| Manager API | `https://localhost:8500/api/v1` |
| API documentation | `https://localhost:8500/docs` |
| OpenSearch | Internal network only |
| PostgreSQL | Internal network only |

Replace `OWNER` and verify the release documentation before using these commands. Default ports and commands may change before the first stable release.

## Planned API

```text
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh

POST   /api/v1/agents/enroll
POST   /api/v1/agents/heartbeat
GET    /api/v1/agents
GET    /api/v1/agents/{agent_id}

POST   /api/v1/events
POST   /api/v1/events/bulk
GET    /api/v1/events
GET    /api/v1/events/{event_id}

GET    /api/v1/alerts
GET    /api/v1/alerts/{alert_id}
PATCH  /api/v1/alerts/{alert_id}

GET    /api/v1/rules
POST   /api/v1/rules
PUT    /api/v1/rules/{rule_id}
POST   /api/v1/rules/validate

GET    /api/v1/incidents
POST   /api/v1/incidents
PATCH  /api/v1/incidents/{incident_id}

POST   /api/v1/hunting/search
GET    /api/v1/health
GET    /api/v1/ready
```

## Security Model

Security is a core product requirement, not an optional add-on.

Planned controls include:

- TLS between the dashboard, manager, indexer, and supporting services
- mTLS or rotatable credentials for agent identity
- Argon2id password hashing
- Short-lived access tokens and refresh-token rotation
- Role-Based Access Control (RBAC)
- Organization and business-unit data scopes
- API rate limiting and payload-size controls
- Replay protection and event timestamp validation
- Signed agent updates and response commands
- Full audit logs for configuration, rule, user, and response changes
- Private indexer and database networks
- Default-deny active-response policy
- Human approval for disruptive production actions

See `SECURITY.md` for vulnerability reporting instructions when that document becomes available.

## Detection Engineering Principles

Ariba rules should be:

- Readable and version controlled
- Validated against a published schema
- Tested with positive and negative samples
- Mapped to relevant MITRE ATT&CK techniques
- Accompanied by investigation guidance
- Tunable without modifying engine source code
- Reviewed for performance and false-positive risk

Every production rule should include an ID, title, description, version, severity, data-source requirement, conditions, MITRE mapping, test samples, and recommended investigation steps.

## Alert and Incident Workflow

Alert lifecycle:

```text
New → Acknowledged → Investigating → Escalated → Resolved → Closed
```

Supported analyst verdicts:

```text
Undetermined | True Positive | False Positive | Benign Positive
```

Incident lifecycle:

```text
New → Assigned → Investigating → Contained → Eradicated
    → Recovered → Resolved → Closed
```

## Roadmap

### Phase 1 — Manager Core

- FastAPI management service
- Agent enrollment
- Event ingestion
- Initial decoders and normalizers
- YAML detection engine
- Alert creation and OpenSearch indexing
- Automated tests

### Phase 2 — SOC Dashboard

- Authentication and RBAC
- Overview and platform health
- Agent inventory
- Event search and threat hunting
- Alert investigation
- Rule management
- Live alert notifications

### Phase 3 — Incident Operations

- Alert-to-incident linking
- Ownership, comments, evidence, and timeline
- L1/L2 escalation
- SLA, MTTA, and MTTR
- Email, Teams, Slack, and webhook integration

### Phase 4 — Endpoint Visibility

- Windows and Linux agent services
- File Integrity Monitoring
- Process, port, service, user, and software inventory
- Agent groups and signed remote configuration
- Secure local event spool

### Phase 5 — XDR and Advanced Detection

- Time-window correlation
- Cross-source attack-chain rules
- Threat-intelligence enrichment
- MITRE ATT&CK coverage
- Alert suppression and deduplication
- Detection testing framework

### Phase 6 — Vulnerability and Response

- Vulnerability feed ingestion
- Asset/software-to-CVE correlation
- Risk-based vulnerability prioritization
- Approved active response
- Response rollback and auditing

### Phase 7 — Scale and Resilience

- Kafka event pipeline
- Horizontally scalable manager workers
- OpenSearch clustering and hot/warm storage
- High availability
- Backup and disaster recovery
- Multi-tenancy and data isolation
- Performance and security assessments

## Contributing

Contributions will be welcome after the initial repository standards and contributor workflow are published.

Expected contribution areas include:

- Python manager and API development
- Windows/Linux agent development
- Next.js dashboard development
- Detection rules and decoders
- OpenSearch performance and lifecycle management
- Security review and threat modeling
- Documentation and translations
- Automated testing

Before submitting a contribution:

1. Open or select an issue describing the change.
2. Discuss major architectural changes before implementation.
3. Create a focused branch.
4. Add or update relevant tests.
5. Run formatting, linting, unit, and security checks.
6. Submit a pull request with the reason, approach, tests, and security impact.

Detailed instructions will be maintained in `CONTRIBUTING.md`.

## Responsible Use

Ariba Security Platform is intended for systems and environments that you own or are explicitly authorized to monitor and administer.

Do not use the software to collect data, execute response actions, access systems, or monitor users without appropriate authorization. Operators are responsible for complying with applicable privacy, employment, security, and data-retention requirements.

## Vulnerability Reporting

Please do not publish suspected security vulnerabilities in public issues. A private reporting channel will be documented in `SECURITY.md` before the first public release.

Until that channel is available, do not deploy the project in a production environment or expose its services to the public internet.

## License

The project is intended to be released as open-source software. **Apache License 2.0** is the proposed license because it supports commercial and non-commercial use while providing explicit patent terms.

The repository's final licensing terms are controlled by the committed `LICENSE` file. Until that file is added, no license grant should be assumed.

## Documentation

Planned documentation:

- Architecture and threat model
- Development environment setup
- Docker deployment
- Agent enrollment
- Event schema reference
- Decoder development
- Rule development and testing
- Index lifecycle and retention
- Incident workflow
- Active-response safety
- Backup and disaster recovery
- API reference

## Acknowledgements

The project learns from open security standards and the broader open-source security community, including MITRE ATT&CK, Sigma, OpenSearch, FastAPI, PostgreSQL, and other defensive-security ecosystems.

Ariba Security Platform is an independent project and is not affiliated with or endorsed by those projects or organizations.

---

**Current release status:** Pre-alpha / architecture and implementation in progress.
