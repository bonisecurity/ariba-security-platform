# Ariba Security Platform - Development Roadmap

## Current Status

**Release**: Pre-alpha / architecture and implementation in progress

**Current priorities** (from README):
- [ ] Repository and development environment
- [ ] Manager health and readiness APIs
- [ ] PostgreSQL, Redis, and OpenSearch integration
- [ ] Agent enrollment and authentication
- [ ] Single and bulk event ingestion
- [ ] Decoder registry and normalized event schema
- [ ] YAML rule schema, loader, and matcher
- [ ] Alert generation and indexing
- [ ] Automated tests and example event generator

## Phase 1 — Manager Core (In Progress)

- [x] FastAPI management service
- [x] Agent enrollment
- [x] Event ingestion
- [x] Initial decoders and normalizers
- [x] YAML detection engine
- [x] Alert creation and OpenSearch indexing
- [ ] Automated tests

## Phase 2 — SOC Dashboard

- [ ] Authentication and RBAC
- [ ] Overview and platform health
- [ ] Agent inventory
- [ ] Event search and threat hunting
- [ ] Alert investigation
- [ ] Rule management
- [ ] Live alert notifications

## Phase 3 — Incident Operations

- [ ] Alert-to-incident linking
- [ ] Ownership, comments, evidence, and timeline
- [ ] L1/L2 escalation
- [ ] SLA, MTTA, and MTTR
- [ ] Email, Teams, Slack, and webhook integration

## Phase 4 — Endpoint Visibility

- [ ] Windows and Linux agent services
- [ ] File Integrity Monitoring
- [ ] Process, port, service, user, and software inventory
- [ ] Agent groups and signed remote configuration
- [ ] Secure local event spool

## Phase 5 — XDR and Advanced Detection

- [ ] Time-window correlation
- [ ] Cross-source attack-chain rules
- [ ] Threat-intelligence enrichment
- [ ] MITRE ATT&CK coverage
- [ ] Alert suppression and deduplication
- [ ] Detection testing framework

## Phase 6 — Vulnerability and Response

- [ ] Vulnerability feed ingestion
- [ ] Asset/software-to-CVE correlation
- [ ] Risk-based vulnerability prioritization
- [ ] Approved active response
- [ ] Response rollback and auditing

## Phase 7 — Scale and Resilience

- [ ] Kafka event pipeline
- [ ] Horizontally scalable manager workers
- [ ] OpenSearch clustering and hot/warm storage
- [ ] High availability
- [ ] Backup and disaster recovery
- [ ] Multi-tenancy and data isolation
- [ ] Performance and security assessments

## Phase 8 — Multi-Tenancy

- [ ] Tenant isolation at database level
- [ ] Organization-based data scoping
- [ ] Multi-tenant dashboard views
- [ ] Tenant-specific rule sets

## Phase 9 — Advanced Analytics

- [ ] Predictive threat scoring
- [ ] Anomaly detection using ML
- [ ] Timeline analysis and attack chain visualization
- [ ] Correlation across multiple data sources

## Phase 10 — Ecosystem Integrations

- [ ] SIEM federation (OpenTelemetry, QRadet integration)
- [ ] Ticketing system integration (Jira, ServiceNow)
- [ ] Threat intelligence platform connectors
- [ ] VirusTotal and OTX integration

## Phase 11 — Mobile and Remote Workforce

- [ ] Enhanced mobile agent support
- [ ] Remote work security monitoring
- [ ] Home office security assessment
- [ ] BYOD policy enforcement

## Phase 12 — Platform Resilience

- [ ] Active-active deployment patterns
- [ ] Geographic redundancy
- [ ] Disaster recovery automation
- [ ] Blue-green deployment strategies

## Documentation Roadmap

- [ ] Video tutorials and walkthroughs
- [ ] Interactive sandbox environment
- [ ] API client libraries (Python, Node, Go)
- [ ] Postman collection for all endpoints
- [ ] Sample rule library with 100+ rules

## Community & Governance Roadmap

- [ ] RFC process for major changes
- [ ] Contributor license agreement
- [ ] Release management pipeline
- [ ] Security policy and vulnerability reporting
- [ ] Code of conduct

## Version History

| Version | Date | Changes |
|---|---|---|
| `0.1.0` | 2026-09-06 | Initial roadmap, Pre-alpha status |
| `0.1.1` | 2026-09-XX | Phase 1 complete, Phase 2 started |
| `1.0.0` | TBD | Stable release, all phases complete |

## Getting Involved

### Contributing to Roadmap

1. **Feature requests** - Open an issue with `enhancement` label
2. **Voting** - React to feature requests to prioritize
3. **Contribution** - Volunteer for specific phases
4. **Feedback** - Review and comment on roadmap updates

### Phase Adoption

- Review the current phase objectives
- Check for open issues related to the phase
- Volunteer to implement specific features
- Help test existing implementations

## Milestones

### Milestone 1 — MVP Release

- Agent enrollment and heartbeat
- Single event ingestion
- Basic detection rules (SQLi, XSS)
- Dashboard overview
- Alert creation and notification

### Milestone 2 — Beta Release

- Bulk event ingestion
- Advanced detection rules
- Rule management UI
- Incident creation and linking
- Response actions (basic)

### Milestone 3 — Stable Release 1.0

- Multi-tenancy
- Advanced analytics
- Ecosystem integrations
- Performance optimizations
- Comprehensive documentation

---

*Roadmap is subject to change based on community feedback, security considerations, and technical feasibility.*