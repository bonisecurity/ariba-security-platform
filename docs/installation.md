# Ariba Security Platform - Installation

## Prerequisites

- Docker and Docker Compose
- Git
- At least 4GB RAM available
- Ports 80, 443, 5432, 5433, 5434, 5435, 9200, 9400 available

## Quick Start

```bash
# Clone the repository
git clone https://github.com/boniyeamincse/ariba-security-platform.git
cd ariba-security-platform

# Copy environment example
cp .env.example .env

# Edit .env with your configuration
# - Edit database passwords, OpenSearch credentials, etc.

# Start the platform
docker compose up -d --build
```

## Services

| Service | Default Endpoint | Port |
|---|---|---|
| Dashboard | `https://localhost:8443` | 8443 |
| Manager API | `https://localhost:8500/api/v1` | 8500 |
| API Documentation | `https://localhost:8500/docs` | 8500 |
| OpenSearch | Internal network only | 9200 |
| PostgreSQL | Internal network only | 5432 |

## Development Environment

```bash
# Install Python dependencies
pip install -e ariba-manager/

# Install Node.js dependencies for dashboard
cd ariba-dashboard && npm install

# Set up environment variables
cp .env.example .env
# Configure:
# - DATABASE_URL
# - OPENSEARCH_HOSTS
# - SECRET_KEY
# - ALGORITHM
# - ACCESS_TOKEN_EXPIRE_MINUTES
```

## Production Deployment

For production environments:

1. Use proper TLS certificates (see `deployment/certificates/`)
2. Configure Nginx reverse proxy
3. Set up regular backups
4. Configure resource limits in Docker Compose
5. Enable monitoring and alerting