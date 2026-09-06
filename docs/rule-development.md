# Ariba Security Platform - Rule Development

## Detection Rule Format

Detection rules are defined in YAML format and follow a structured schema. Every rule should include the following fields:

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

## Rule Components

### ID
- Format: `ARIBA-{CATEGORY}-{4-digit-number}`
- Must be unique across the ruleset
- Use sequential numbering or UUIDs for new rules

### Name
- Descriptive title of the detection
- Should be clear and actionable
- Avoid cryptic abbreviations

### Version
- Starts at `1`
- Increment for any changes to the rule
- Follow semantic versioning for breaking changes

### Enabled
- `true` - Rule is active
- `false` - Rule is disabled (commented out or disabled field)

### Severity
- `low` - Informational, low impact
- `medium` - Potential threat, investigate
- `high` - Likely threat, immediate action
- `critical` - Confirmed attack, immediate response required

### Match Conditions

Rules use a matching engine that supports:

```yaml
match:
  all:  # All conditions must be true
  any:  # At least one condition must be true

  # Individual condition
  - field: event.category
    operator: equals
    value: web

  # Supported operators:
  - equals
  - not_equals
  - regex
  - contains
  - not_contains
  - exists
  - missing
  - less_than
  - greater_than
  - in_list
  - not_in_list
```

### Groups
- Categorize rules for filtering and reporting
- Example groups: `web_attack`, `sqli`, `xss`, `brute_force`, `persistence`
- Use consistent naming conventions

### MITRE Mapping
- `tactic`: MITRE ATT&CK tactic (e.g., `Initial Access`, `Persistence`, `Discovery`)
- `technique_id`: MITRE technique ID (e.g., `T1190`, `T1059`)

### Actions
- `create_alert`: Boolean to control alert generation
- `notify`: Boolean to control notifications (email, Teams, Slack, Telegram)
- Additional actions can be defined for automated response

## Rule Development Workflow

### 1. Identify the Threat
- Review MITRE ATT&CK techniques
- Understand the attack pattern
- Identify relevant log sources

### 2. Define the Data Source
- Determine which fields are available in the normalized event
- Check existing decoders for your log source
- Ensure the fields you need are normalized correctly

### 3. Write the Rule
- Start with the `match` section
- Use appropriate operators for your data type
- Test with positive and negative samples

### 4. Test the Rule
```bash
# Test with sample events
python -m ariba-manager.rules.rule_validator --rule rules/web/sql-injection.yml --samples tests/

# Run unit tests
pytest ariba-manager/tests/ -k rule -v
```

### 5. Add to Ruleset
- Place the YAML file in the appropriate directory
- `ariba-ruleset/rules/web/sql-injection.yml`
- `ariba-ruleset/rules/linux/ssh.yml`
- etc.

### 6. Document the Rule
- Add description and investigation guidance
- Include test samples
- Map to MITRE techniques
- Note any tuning considerations

## Rule Schema Validation

Rules are validated against the JSON schema at `ariba-ruleset/schemas/rule.schema.json`. Validation includes:

- Required fields present
- Valid severity values
- Valid operator types
- Correct field names matching the event schema
- MITRE tactic and technique format

## Best Practices

1. **Keep rules focused** - One detection per rule when possible
2. **Use specific fields** - Avoid matching on broad categories
3. **Test thoroughly** - Include both positive and negative test cases
4. **Map to MITRE** - Every production rule should have ATT&CK mapping
5. **Include investigation guidance** - Help analysts understand what to look for
6. **Tune for false positives** - Adjust operators or conditions as needed
7. **Version your rules** - Increment version on any changes
8. **Use meaningful IDs** - Make IDs descriptive and unique

## Example Rules

### SQL Injection Detection
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

### Brute Force Detection
```yaml
id: ARIBA-AUTH-2001
name: Possible Brute Force Attack
version: 1
enabled: true
severity: high

match:
  all:
    - field: event.type
      operator: equals
      value: authentication
    - field: event.outcome
      operator: equals
      value: failure
    - field: source.ip
      operator: greater_than
      value: 100

groups:
  - authentication
  - brute_force

mitre:
  tactic: Credential Access
  technique_id: T1110

actions:
  create_alert: true
  notify: true
```