# Ariba Security Platform - Agent Enrollment

## Overview

Agents are the primary data collection points for the Ariba Security Platform. They collect endpoint telemetry, logs, and security events and send them to the Ariba Manager for processing, normalization, and alert generation.

## Enrollment Process

### 1. Agent Registration

```http
POST /api/v1/agents/enroll
Content-Type: application/json

{
  "hostname": "web-server-01",
  "os": "linux",
  "os_version": "22.04",
  "ip_address": "10.24.66.20",
  "tags": ["web", "production"],
  "capabilities": ["linux_logs", "fim", "process_monitor"]
}
```

### 2. Authentication & Token Generation

Upon successful enrollment, the agent receives:

- **Access Token** - Used for authenticated API calls
- **Heartbeat Secret** - Used for heartbeat endpoint authentication
- **Agent ID** - Unique identifier for the agent

### 3. Agent Configuration

Agents must configure the following:

```yaml
# ariba-agent/agent/config.py
class AgentConfig:
    manager_url: "https://localhost:8500"
    agent_id: "001"
    agent_secret: "your-agent-secret-key"
    heartbeat_interval: 30  # seconds
    collector_config:
      linux_logs: true
      windows_events: false
      file_monitor: true
      process_monitor: true
      inventory: true
```

## Supported Platforms

### Linux Agents

- **Supported Distributions**: Ubuntu 20.04/22.04, Debian 11/12, CentOS 7/8, RHEL 7/8/9, Alpine Linux
- **Collection Methods**:
  - `/var/log/` file monitoring
  - System log collection (syslog/rsyslog)
  - Kernel event monitoring
  - Process tracking
  - FIM (File Integrity Monitoring)
  - Inventory enumeration

### Windows Agents

- **Supported Versions**: Windows 10/11, Windows Server 2016/2019/2022
- **Collection Methods**:
  - Windows Event Log (EVTX)
  - PowerShell Script Block Logging
  - API Monitoring
  - Registry change detection
  - File Integrity Monitoring
  - Process monitoring

### Docker/Kubernetes Agents

- **Sidecar deployment** pattern
- **DaemonSet** for cluster-wide coverage
- **FIM** on container filesystem changes
- **Log collection** from container stdout/stderr

## Enrollment Workflow

```text
1. Download Ariba Agent binary/package
2. Configure manager URL and credentials
3. Run enrollment command:
   - Linux: ./ariba-agent --enroll --manager https://localhost:8500
   - Windows: .\ariba-agent.exe --enroll --manager https://localhost:8500
4. Agent validates credentials with Manager API
5. Manager generates agent JWT token
6. Agent stores token securely
7. Agent begins sending heartbeats
8. Agent starts collecting and sending events
```

## Agent Heartbeat

```http
POST /api/v1/agents/heartbeat
Content-Type: application/json

{
  "agent_id": "001",
  "status": "healthy",
  "metadata": {
    "cpu_usage": 15.3,
    "memory_usage": 45.2,
    "loaded": true
  }
}
```

### Heartbeat Frequency

- **Default**: Every 30 seconds
- **Minimum**: 10 seconds
- **Maximum**: 60 seconds (recommended)
- **Loss threshold**: 3 missed heartbeats = agent marked as offline

## Agent Response Actions

Agents can receive and execute approved response actions:

```http
POST /api/v1/response/actions/{action_id}
Content-Type: application/json

{
  "agent_id": "001",
  "params": {
    "block_ip": "203.0.113.5",
    "duration": 3600
  }
}
```

### Supported Actions

| Action | Description | Parameters |
|---|---|---|
| `block_ip` | Block IP at firewall level | `ip`, `duration` |
| `isolate_host` | Isolate host from network | `host_id`, `duration` |
| `kill_process` | Kill suspicious process | `pid`, `signal` |
| `disable_user` | Disable user account | `user`, `duration` |

## Troubleshooting Enrollment

### Common Issues

1. **Connection refused** - Manager API not running or wrong URL
2. **Authentication failed** - Invalid agent ID or secret
3. **Timeout** - Network connectivity issues or firewall blocking
4. **Certificate error** - TLS certificate trust issues (see below)
5. **Rate limited** - Too many enrollment attempts (back off recommended)

### TLS Certificate Trust

For production environments with self-signed certificates:

```bash
# Linux agent
export ARBA_MANAGER_CERT=/path/to/ca-cert.pem
export ARBA_MANAGER_INSECURE=0

# Or add to system trust store
sudo cp /path/to/ca-cert.pem /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Or disable verification (development only)
export ARBA_MANAGER_INSECURE=1
```

## Agent Registration via Script

```bash
# Using the setup script
cd ariba-security-platform/scripts
./setup-dev.sh --enroll-agent --hostname "my-server" --os linux

# Or manually
docker exec -it ariba-manager python -c "
from ariba_manager.app.main import app
# Enroll agent via API
"
```

## Agent Removal/Deregistration

```http
DELETE /api/v1/agents/{agent_id}
```

or via CLI:

```bash
# Linux
./ariba-agent --deregister --agent-id 001

# Windows
.\ariba-agent.exe --deregister --agent-id 001
```

## Best Practices

1. **Secure agent secrets** - Store agent secrets in a password manager, not in plain text
2. **Regular heartbeats** - Ensure agents are configured with appropriate heartbeat intervals
3. **Tag agents** - Use tags for environment, role, or team segregation
4. **Monitor agent health** - Dashboard should show agent status (online/offline)
5. **Automatic reconnection** - Agents should automatically reconnect after network outages
6. **Least privilege** - Agents should only have permissions needed for data collection