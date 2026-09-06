# Ariba Security Platform - Active Response

## Overview

Active Response enables approved manual and automated response actions to be executed against compromised or suspicious endpoints. All actions require approval and are logged for audit purposes.

## Approval Workflow

### Action Approval Tiers

| Tier | Description | Approval Required | Escalation |
|---|---|---|---|
| **Tier 1** | Informational, low impact | None | Log only |
| **Tier 2** | Service disruption, medium impact | Analyst approval | Team lead |
| **Tier 3** | Host isolation, high impact | Manager approval | CISO/Security Director |
| **Tier 4** | Production system impact, critical | Executive approval | Emergency response team |

### Approval Process

```text
1. Alert triggers potential response
2. Analyst reviews alert and selects action
3. System presents approval dialog with:
   - Action description
   - Target(s)
   - Impact assessment
   - Time window
4. Approver reviews and approves/rejects
5. Action executed on target
6. Outcome recorded in audit log
7. Notification sent to stakeholders
```

## Approved Response Actions

### Block IP

```http
POST /api/v1/response/actions/block_ip
Content-Type: application/json

{
  "agent_id": "001",
  "target_ip": "203.0.113.5",
  "duration_minutes": 3600,
  "approver_id": "analyst-01",
  "comment": "Blocking C2 server IP"
}
```

### Isolate Host

```http
POST /api/v1/response/actions/isolate_host
Content-Type: application/json

{
  "agent_id": "001",
  "duration_minutes": 1440,
  "approver_id": "manager-01",
  "comment": "Isolating compromised endpoint"
}
```

### Kill Process

```http
POST /api/v1/response/actions/kill_process
Content-Type: application/json

{
  "agent_id": "001",
  "process_id": 12345,
  "signal": "SIGTERM",
  "approver_id": "analyst-01",
  "comment": "Killing suspicious mining process"
}
```

### Disable User

```http
POST /api/v1/response/actions/disable_user
Content-Type: application/json

{
  "agent_id": "001",
  "username": "suspicious_user",
  "duration_hours": 24,
  "approver_id": "manager-01",
  "comment": "Disabling compromised account"
}
```

## Audit Logging

All active response actions are logged with:

```json
{
  "action_id": "resp-001",
  "action_type": "block_ip",
  "target": "203.0.113.5",
  "initiator": "analyst-01",
  "approver": "manager-01",
  "status": "completed",
  "timestamp": "2026-01-15T14:30:00Z",
  "result": {
    "success": true,
    "details": "IP blocked at firewall for 1 hour"
  },
  "evidence": {
    "screenshots": [],
    "output": "iptables -A INPUT -s 203.0.113.5 -j DROP",
    "logs": []
  }
}
```

## Response Action Safety Features

### Dry-Run Mode

```http
POST /api/v1/response/actions/block_ip
Content-Type: application/json

{
  "agent_id": "001",
  "target_ip": "203.0.113.5",
  "duration_minutes": 3600,
  "dry_run": true,
  "approver_id": "analyst-01"
}
```

- `dry_run: true` - Action is simulated, not executed
- Logs what would happen without actual impact
- Useful for testing and training

### Time-Limited Actions

All destructive actions must have a time limit:

```yaml
# Configuration example
max_isolation_duration: 48  # hours
max_ip_block_duration: 72   # hours
require_approval_above: 2   # severity threshold
```

### Multi-Party Approval

For critical actions, require multiple approvers:

```yaml
# Configuration
critical_actions_require: 2  # two approvers needed
critical_action_types: 
  - isolate_host
  - disable_user
  - block_ip (duration > 24h)
```

## Response Workflow Dashboard

The Ariba Dashboard provides:

1. **Pending Approvals** - List of actions awaiting approval
2. **Execution Status** - Real-time status of in-progress actions
3. **History** - Complete audit trail of all past actions
4. **Metrics** - Response times, success rates, action types
5. **Rollback** - Ability to reverse approved actions

## Security Model

### Principle of Least Privilege

- Agents only execute approved actions
- Actions are scoped to specific agents/hosts
- No wildcard permissions
- All actions logged and auditable

### Action Validation

Before execution, the system validates:

1. **Agent authentication** - Is the agent authorized?
2. **Action eligibility** - Is this action allowed for this agent?
3. **Target validity** - Does the target exist and are we allowed to act on it?
4. **Time constraints** - Is the action within allowed time windows?
5. **Approval status** - Has the action been properly approved?

### Fail-Safe Defaults

- If approval system is unavailable, actions are blocked
- If agent communication fails, actions are not executed
- If target is unreachable, action is marked as failed
- All failures alert security team

## Testing & Validation

### Unit Tests

```python
def test_block_ip_action():
    from ariba_response.app.actions.block_ip import block_ip
    
    # Test dry-run
    result = block_ip(dry_run=True)
    assert result["status"] == "dry_run"
    assert result["executed"] == False
    
    # Test actual execution
    result = block_ip(dry_run=False)
    assert result["status"] == "completed"
    assert result["executed"] == True
```

### Integration Tests

```bash
# Test end-to-end workflow
pytest ariba-response/tests/ -v

# Manual test flow
1. Create alert for suspicious activity
2. Select "Block IP" action
3. Approve action
4. Verify IP is blocked
5. Verify audit log entry created
6. Verify notification sent
```

## Best Practices

1. **Always use dry-run first** - Test actions before execution
2. **Set appropriate time limits** - Don't block IPs indefinitely
3. **Document every action** - Use meaningful comments
4. **Review approval logs** - Regular audit of who approved what
5. **Escalation paths** - Define clear escalation for critical actions
6. **Regular review** - Periodically review action effectiveness
7. **Training** - Ensure analysts understand action impacts