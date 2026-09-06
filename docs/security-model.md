# Ariba Security Platform - Security Model

## Overview

Ariba Security Platform implements a defense-in-depth security model protecting both the platform itself and the environments it monitors. Security is a core product requirement, not an optional add-on.

## Authentication Model

### Multi-Factor Authentication (MFA)

| Method | Supported | Notes |
|---|---|---|
| Password | Yes | Argon2id hashing, minimum 12 characters |
| TOTP (Google Authenticator, Authy) | Yes | QR code-based setup, 6-digit codes |
| SMS OTP | Yes | Rate limited, carrier-dependent |
| Push Notifications | Yes | App-based confirmation |
| WebAuthn/FIDO2 | Yes | Hardware keys, platform authenticators |
| Backup Codes | Yes | 8 single-use codes provided at enrollment |

### Session Management

```yaml
# Session configuration
session_lifetime_minutes: 43200  # 30 days maximum
refresh_token_lifetime_days: 30
max_concurrent_sessions: 3
session_regeneration_on_login: true
invalidate_on_password_change: true
invalidate_on_mfa_change: true
invalidate_on_logout: true
```

### Token Security

- **Access Tokens** - JWT, short-lived (default 30 minutes)
- **Refresh Tokens** - Opaque, rotated on use
- **Signed with** - Argon2id-derived key or RSA-2048
- **Scope-based** - Tokens have specific permissions
- **IP binding** - Optional, configurable

## Authorization Model

### Role-Based Access Control (RBAC)

| Role | Permissions |
|---|---|
| `super_admin` | All permissions, user management, system config |
| `security_analyst` | View alerts, incidents, agents; create alerts, add notes |
| `security_manager` | All analyst permissions + rule management, user management |
| `response_operator` | Execute approved response actions, view audit log |
| `view_only` | Read-only access to dashboards and reports |

### Permission Granularity

```yaml
# Example role definition
roles:
  security_analyst:
    - "alerts:read"
    - "alerts:create"
    - "alerts:update_verdict"
    - "incidents:read"
    - "agents:read"
    - "rules:read"
    - "dashboard:view"
  security_manager:
    - "*"  # All permissions
    - "users:manage"
    - "rules:manage"
    - "settings:edit"
```

### Organization Scoping

- Multi-tenant support via organization IDs
- Data isolation between organizations
- Role assignments per organization
- Cross-organization visibility controlled

## Data Protection

### Encryption at Rest

| Data Type | Encryption | Key Management |
|---|---|---|
| PostgreSQL data | AES-256 | AWS KMS or local HSM |
| OpenSearch indices | AES-256 | Index-level settings |
| Agent communications | TLS 1.3 | mTLS certificates |
| Backups | AES-256 | Separate key hierarchy |
| Logs | AES-256 | Rotated daily |

### Encryption in Transit

- **TLS 1.3+** for all HTTP connections
- **mTLS** for agent-to-manager communication
- **Redis TLS** for queue communications
- **OpenSearch HTTPS** for API access

### Key Rotation

- **Master key**: Annually
- **Data encryption keys**: Every 90 days
- **JWT signing keys**: Every 30 days
- **TLS certificate**: Yearly (Let's Encrypt or CA)

## Privacy Controls

### Data Minimization

- Collect only necessary telemetry
- Configureurable data retention policies
- PII masking and redaction
- User consent tracking

### Retention Policies

| Data Type | Default Retention | Configurable |
|---|---|---|
| Raw events | 90 days | 30-365 days |
| Normalized events | 180 days | 30-730 days |
| Alerts | 1 year | 30-2 years |
| Incidents | 2 years | 1-5 years |
| Audit logs | 7 years | 1-10 years (compliance) |
| Threat intelligence | 1 year | 30-5 years |

### PII Handling

- Automatic detection and masking
- Optional storage with encryption
- Export requests handled per privacy policy
- Data subject access requests (DSAR) supported

## Compliance Frameworks

### Supported Standards

| Framework | Controls Mapped | Status |
|---|---|---|
| **SOC 2 Type II** | CC6.1, CC6.6, CC7.2, CC7.3 | In progress |
| **ISO 27001** | A.8, A.9, A.10, A.12, A.13, A.14, A.15, A.16, A.18 | In progress |
| **NIST CSF** | All 5 Functions (Identify, Protect, Detect, Respond, Recover) | Aligned |
| **PCI DSS** | Requirement 10 (Audit Logging) | Scope-dependent |
| **GDPR** | Article 32 (Security), Article 33 (Breach), Article 35 (DPIA) | Features enabled |
| **HIPAA** | Security Rule, Breach Notification | Healthcare-specific config |

### Audit Capabilities

```yaml
# Audit logging configuration
audit:
  enable: true
  log_level: "INFO"
  include:
    - user_authentication
    - user_authorization
    - configuration_changes
    - alert_actions
    - agent_enrollment
    - response_actions
    - data_access
  exclude:
    - password_changes (hashed)
    - internal_health_checks
```

### Export & Reporting

- CSV/JSON export of audit logs
- Pre-built compliance reports
- Custom report builder
- Scheduled report generation
- Integration with GRC tools (ServiceNow, Jira, etc.)

## Threat Model

### Attack Surface

| Vector | Impact | Mitigation |
|---|---|---|
| API endpoints | Medium | Rate limiting, authentication, input validation |
| Agent enrollment | High | mTLS, secrets management, enrollment limits |
| Dashboard XSS | Low/Medium | Content Security Policy, input sanitization |
| Rule injection | Medium | YAML schema validation, MITRE mapping |
| Database access | High | Principle of least privilege, connection pooling |
| Supply chain | Medium | SBOM, dependency scanning, verified sources |

### Defense Layers

```text
┌──────────────────────────────────────────────────────────────┐
│                    Network Layer                              │
│  - Firewall rules                                              │
│  - Nginx reverse proxy with WAF                               │
│  - VPC/subnet isolation                                       │
│  - Network segmentation                                       │
├──────────────────────────────────────────────────────────────┤
│                    Application Layer                          │
│  - Authentication (Auth0/Okta integration)                   │
│  - Authorization (RBAC/ABAC)                                  │
│  - Input validation (Pydantic models)                       │
│  - Rate limiting (per-endpoint)                               │
│  - Request validation (JSON schema)                         │
├──────────────────────────────────────────────────────────────┤
│                    Data Layer                                 │
│  - Encryption at rest (AES-256)                              │
│  - Encryption in transit (TLS 1.3)                           │
│  - Key management (KMS/HSM)                                  │
│  - Access controls (PostgreSQL Row Level Security)           │
│  - Audit logging (immutable logs)                           │
└──────────────────────────────────────────────────────────────┘
```

### Security Hardening Checklist

#### Deployment hardening

- [ ] Change default passwords before first run
- [ ] Use TLS certificates (Let's Encrypt or CA-signed)
- [ ] Configure firewall rules (restrict ports)
- [ ] Disable unused API endpoints
- [ ] Set up monitoring and alerting on security events
- [ ] Enable audit logging
- [ ] Configure backup and recovery procedures
- [ ] Regular security updates and patching

#### Platform configuration

- [ ] Enable MFA for all user accounts
- [ ] Set up organization scoping for multi-tenant deployments
- [ ] Configure session timeouts and regeneration
- [ ] Define RBAC roles and permissions
- [ ] Configure data retention policies
- [ ] Enable threat intelligence integration
- [ ] Set up incident response playbooks

#### Agent security

- [ ] Deploy agents with mTLS certificates
- [ ] Secure agent secrets (vault, not in code)
- [ ] Regular agent software updates
- [ ] Monitor agent heartbeat and health
- [ ] Enforce least privilege on agents
- [ ] Secure communication channels

## Security Model Summary

Ariba Security Platform's security model follows these principles:

1. **Defense-in-Depth** - Multiple layers of security controls
2. **Least Privilege** - Minimum necessary access for each role
3. **Default-Deny** - Everything blocked unless explicitly allowed
4. **Assume Breach** - Designed assuming some compromise may occur
5. **Audit Everything** - Complete, immutable audit trail
6. **Privacy-First** - Data minimization and user privacy protection
7. **Compliance-Ready** - Designed to meet major regulatory frameworks

All security controls are configurable to match organizational requirements while maintaining baseline security standards.