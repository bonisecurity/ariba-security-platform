# Ariba Security Platform - API Reference

## Authentication

All API endpoints require authentication unless otherwise noted.

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

### Refresh Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOi..."
}
```

### Get Current User

```http
GET /api/v1/health
```

## Agent Management

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/agents/enroll` | Enroll a new agent |
| `POST` | `/api/v1/agents/heartbeat` | Send heartbeat from agent |
| `GET` | `/api/v1/agents` | List all agents |
| `GET` | `/api/v1/agents/{agent_id}` | Get agent details |

## Event Ingestion

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/events` | Submit a single event |
| `POST` | `/api/v1/events/bulk` | Submit events in bulk |

## Alert Management

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/alerts` | List all alerts |
| `GET` | `/api/v1/alerts/{alert_id}` | Get alert details |
| `PATCH` | `/api/v1/alerts/{alert_id}` | Update alert status/verdict |

## Rule Management

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/rules` | List all detection rules |
| `POST` | `/api/v1/rules` | Create a new rule |
| `PUT` | `/api/v1/rules/{rule_id}` | Update an existing rule |
| `POST` | `/api/v1/rules/validate` | Validate a rule YAML definition |

## Incident Management

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/incidents` | List all incidents |
| `POST` | `/api/v1/incidents` | Create a new incident |
| `PATCH` | `/api/v1/incidents/{incident_id}` | Update incident status |

## Hunting

```http
POST /api/v1/hunting/search
Content-Type: application/json

{
  "query": "...",
  "filters": {...}
}
```

## Health Checks

```http
GET /api/v1/health
GET /api/v1/ready
```