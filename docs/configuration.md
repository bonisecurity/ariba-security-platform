# Ariba Security Platform - Configuration

## Environment Configuration

### `.env` File Variables

| Variable | Description | Default | Example |
|---|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | - | `postgresql://postgres:password@localhost:5432/ariba` |
| `OPENSEARCH_HOSTS` | OpenSearch cluster hosts | - | `["http://localhost:9200"]` |
| `OPENSEARCH_USER` | OpenSearch authentication user | - | `admin` |
| `OPENSEARCH_PASSWORD` | OpenSearch authentication password | - | `admin123` |
| `SECRET_KEY` | JWT and API signing key | - | `your-secret-key-min-32-chars` |
| `ALGORITHM` | JWT algorithm | `HS256` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry | `30` | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | `7` | `7` |
| `ENVIRONMENT` | Deployment environment | `development` | `development`, `production` |
| `LOG_LEVEL` | Logging verbosity | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### Ariba Manager Configuration

```python
# ariba_manager/app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ariba")
    OPENSEARCH_HOSTS: list = os.getenv("OPENSEARCH_HOSTS", "http://localhost:9200").split(",")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-min-32-chars")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"
```

### OpenSearch Configuration

#### `ariba-indexer/config/opensearch.yml`

```yaml
cluster.name: ariba-indexer
node.name: ${HOSTNAME}
path.data: /var/lib/opensearch
path.logs: /var/log/opensearch
path.plugins: /usr/share/opensearch/plugins

network.host: 0.0.0.0
http.port: 9200

discovery.type: single-node
xpack.security.enabled: false

# Index lifecycle policies
index.lifecycle.poll_interval: 1h
```

#### Index Templates

See `ariba-indexer/templates/` for event, alert, and incident templates.

### Redis Configuration (for queue/buffer)

```yaml
# If using Redis Streams
redis_host: localhost
redis_port: 6379
redis_db: 0
redis_password: null
```

### Nginx Reverse Proxy Configuration

See `deployment/nginx/` for complete configuration.

### TLS/SSL Configuration

#### `deployment/certificates/README.md`

Generated certificates for:
- Dashboard (`localhost` or your domain)
- Manager API
- Agent mTLS certificates

Use `scripts/create-certificates.sh` to generate self-signed certs for development.

## Feature Flags

| Feature | Description | Default |
|---|---|---|
| `ENABLE_AUTH` | Authentication middleware | `true` |
| `ENABLE_RATE_LIMIT` | API rate limiting | `true` |
| `ENABLE_AUDIT_LOG` | Audit trail logging | `true` |
| `ENABLE_WEBHOOKS` | Webhook notifications | `true` |
| `ENABLE_INCIDENT_LINKING` | Alert-to-incident linking | `true` |
| `ENABLE_THREAT_HUNTING` | Threat hunting endpoints | `false` (dev) |

## Database Migrations

### Alembic Configuration

```bash
# Create a new migration
cd ariba-manager
alembic revision --autogenerate -m "description of changes"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Seed Data

```bash
# Seed admin user
cd ariba-manager
python -m scripts.seed-admin
```

## Service Configuration

| Service | Environment File | Port | Notes |
|---|---|---|---|
| Manager API | `.env` | 8500 | FastAPI application |
| Dashboard | `.env` | 8443 | Next.js application |
| OpenSearch | `.env` | 9200 | Search and analytics |
| PostgreSQL | `.env` | 5432 | Relational data |
| Redis | `.env` | 6379 | Message queue |
| Nginx | `deployment/nginx/` | 80/443 | Reverse proxy |