# Ariba Security Platform - Decoder Development

## Overview

Decoders convert raw log data from various sources into the Ariba Platform's normalized event format. This section covers decoder development, registration, and best practices.

## Decoder Format

Decoders are defined in YAML format and follow a structured schema. Every decoder should include:

```yaml
name: nginx access decoder
description: Decode nginx access log format
entry_point: nginx_access
```

## Decoder Components

### Name
- Human-readable name for the decoder
- Should describe the log source format
- Use singular nouns (e.g., `nginx access`, `windows event`)

### Description
- Brief explanation of what the decoder does
- What log format it handles
- Any important notes or limitations

### Entry Point
- Python module name that implements the decoding logic
- Must exist in `ariba-manager/decoders/` directory
- Follows the pattern: `{log_source}.py`

## Supported Decoder Types

### Base Decoder
All decoders inherit from the base decoder class:

```python
from ariba_manager.decoders.base import BaseDecoder

class NgxDecoder(BaseDecoder):
    def decode(self, raw_data: str) -> dict:
        # Parse raw log line
        # Return normalized event dict
        pass
```

### Specific Decoder Implementations

#### JSON Decoder
For JSON-formatted logs:

```yaml
name: json decoder
description: Decode JSON formatted logs
entry_point: json_decoder
```

#### Syslog Decoder
For syslog-formatted logs:

```yaml
name: syslog decoder
description: Decode syslog UDP/TCP messages
entry_point: syslog_decoder
```

#### Linux Auth Decoder
For Linux authentication logs:

```yaml
name: linux auth decoder
description: Decode Linux authentication events
entry_point: linux_auth
```

#### Windows Event Decoder
For Windows Event Log events:

```yaml
name: windows event decoder
description: Decode Windows Event Log events
entry_point: windows_event
```

#### Nginx Access Decoder
For nginx web server logs:

```yaml
name: nginx access decoder
description: Decode nginx access log format
entry_point: nginx_access
```

#### Apache Access Decoder
For Apache web server logs:

```yaml
name: apache access decoder
description: Decode Apache access log format
entry_point: apache_access
```

#### MikroTik Decoder
For MikroTik router logs:

```yaml
name: mikrotik decoder
description: Decode MikroTik router events
entry_point: mikrotik
```

#### Firewall Decoder
For firewall log formats:

```yaml
name: firewall decoder
description: Decode firewall log events
entry_point: firewall
```

## Decoder Registration

Decoders are automatically registered when the Ariba Manager starts. The registry scans the `ariba_manager/decoders/` directory for YAML configuration files and Python modules.

### Directory Structure

```
ariba-manager/
├── decoders/
│   ├── __init__.py
│   ├── registry.py
│   ├── base.py
│   ├── json_decoder.py
│   ├── syslog_decoder.py
│   ├── linux_auth.py
│   ├── windows_event.py
│   ├── nginx_access.py
│   ├── apache_access.py
│   ├── mikrotik.py
│   └── firewall.py
```

### Registry Configuration

The decoder registry (`registry.py`) loads all decoders at startup:

```python
from ariba_manager.decoders.registry import DecoderRegistry

registry = DecoderRegistry()
registry.load_all()
# Access decoders by name
decoder = registry.get("nginx access")
```

## Writing a Decoder

### 1. Define the YAML Configuration

Create a YAML file in `ariba_manager/decoders/`:

```yaml
name: custom log decoder
description: Decode custom application logs
entry_point: custom_log
```

### 2. Implement the Python Decoder

Create a Python file that inherits from `BaseDecoder`:

```python
from ariba_manager.decoders.base import BaseDecoder
import re

class CustomLogDecoder(BaseDecoder):
    """Decode custom application log format."""
    
    SUPPORTED_PATTERNS = [
        r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}",
    ]
    
    def decode(self, raw_data: str) -> dict:
        """Decode a single log line into a normalized event."""
        line = raw_data.strip()
        
        # Parse the log line here
        # Example: match = re.match(pattern, line)
        
        # Return normalized event
        return {
            "@timestamp": "2026-01-01T00:00:00Z",
            "event": {
                "id": "01CUSTOMEVENT",
                "category": "custom",
                "type": "log",
                "action": "log_entry",
            },
            "agent": {
                "id": "001",
                "name": "custom-server-01",
            },
            "source": {
                "ip": "10.0.0.1",
            },
            "custom": {
                "field": value_from_log,
            },
        }
```

### 3. Test the Decoder

```python
from ariba_manager.decoders.registry import DecoderRegistry

registry = DecoderRegistry()
decoder = registry.get("custom log")
event = decoder.decode("2026-01-01 12:00:00 custom log data")
assert event is not None
assert event["event"]["category"] == "custom"
```

## Decoder Best Practices

1. **Handle malformed input** - Decoders should not crash on unexpected formats
2. **Preserve raw data** - Keep the original raw event in a `raw_event` field if possible
3. **Set reasonable defaults** - Fill in missing fields with `null` or empty strings
4. **Use consistent field names** - Follow the event schema for field names
5. **Document edge cases** - Note any known limitations or quirks
6. **Test with real data** - Use actual log samples from the source
7. **Performance matters** - Decoders run on every incoming event; avoid expensive operations
8. **Error logging** - Log decoding errors for later analysis

## Event Schema Fields

Decoders should populate these core fields from the normalized event:

| Field | Description | Example |
|---|---|---|
| `@timestamp` | Event occurrence time | `2026-01-01T14:30:00Z` |
| `event.id` | Unique event ID | `01KEXAMPLEEVENT` |
| `event.category` | Event category | `web`, `authentication`, `linux`, etc. |
| `event.type` | Event type | `access`, `login`, `process`, etc. |
| `event.action` | Event action | `http_request`, `login_attempt`, etc. |
| `event.outcome` | Outcome of event | `allowed`, `blocked`, `failed`, etc. |
| `agent.id` | Agent identifier | `001` |
| `agent.name` | Agent hostname | `web-server-01` |
| `agent.ip` | Agent IP address | `10.24.66.20` |
| `source.ip` | Source IP address | `10.24.50.129` |
| `destination.ip` | Destination IP address | `10.24.66.20` |
| `destination.port` | Destination port | `443` |
| `http` | HTTP request details | method, url, response status, etc. |
| `observer` | Observer product | `nginx`, `apache`, `windows`, etc. |

## Decoder Testing

### Unit Tests

```python
import pytest
from ariba_manager.decoders.json_decoder import JsonDecoder

def test_json_decoder_basic():
    decoder = JsonDecoder()
    raw = '{"event": {"category": "web", "type": "access"}, "agent": {"id": "001"}}'
    event = decoder.decode(raw)
    assert event["event"]["category"] == "web"
```

### Integration Tests

```python
def test_decoder_registry_loads_all():
    from ariba_manager.decoders.registry import DecoderRegistry
    registry = DecoderRegistry()
    registry.load_all()
    assert len(registry.get_all()) > 0
    assert "nginx access" in registry.get_all()
```

### Sample Log Testing

Place sample log files in `tests/` directories and test decoders against them:

```bash
# Test with sample nginx logs
python -m pytest ariba-manager/tests/ -k decoder -v
```

## Adding a New Decoder

### 1. Create the YAML config

```yaml
name: new log decoder
description: Decode new log source format
entry_point: new_log
```

### 2. Create the Python module

Implement the `BaseDecoder` interface with `decode()` method.

### 3. Register and test

The decoder will be automatically discovered on next startup.

### 4. Add to documentation

Update `docs/decoder-development.md` with new decoder details.

## Troubleshooting

### Common Issues

1. **Decoder not loading** - Check YAML syntax and that `entry_point` matches a Python file
2. **Decoding returns null** - Check field names match the event schema
3. **Performance issues** - Optimize parsing logic, avoid regex compilation inside `decode()`
4. **Missing fields** - Ensure all required fields are populated

### Debug Mode

```python
import logging
logging.getLogger("ariba_manager.decoders").setLevel(logging.DEBUG)
```

This will output detailed decoding information for troubleshooting.