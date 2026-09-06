# Ariba Security Platform - Contributing Guide

Thank you for considering contributing to the Ariba Security Platform! This guide explains the workflow and standards for contributing to this project.

## 🌟 Ways to Contribute

Contributions are welcome in many forms:

- **Python manager and API development** - FastAPI endpoints, services, and infrastructure
- **Windows/Linux agent development** - Endpoint telemetry collection and FIM
- **Next.js dashboard development** - SOC web interface and hunting tools
- **Detection rules and decoders** - YAML rules, log parsers, and normalizers
- **OpenSearch performance and lifecycle management** - Index templates, pipelines, and retention policies
- **Security review and threat modeling** - Architecture reviews and risk assessments
- **Documentation and translations** - Guides, references, and multilingual support
- **Automated testing** - Unit, integration, and E2E tests

## 📋 Getting Started

### 1. Find or Create an Issue

Before starting work, check if there's an existing issue for your contribution:

- Browse open issues to find something that matches your interest
- If working on a new area, create an issue first to discuss scope and approach
- Label your issue appropriately (e.g., `good first issue`, `enhancement`, `bug`)

### 2. Discuss Major Changes

For significant architectural changes or new components:

- Open a discussion before implementing
- Get feedback from maintainers on your proposed approach
- Ensure alignment with the project roadmap and architecture

### 3. Set Up Development Environment

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/your-username/ariba-security-platform.git
   cd ariba-security-platform
   ```

2. Install dependencies:
   ```bash
   # From the ariba-security-platform directory
   pip install -e ariba-manager/
   # Install other components as needed
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the infrastructure:
   ```bash
   docker compose up -d --build
   ```

### 4. Create a Focused Branch

Always work on a dedicated branch:

```bash
git checkout -b feature/your-feature-name
# Or for bugs:
git checkout -b bugfix/issue-description
```

### 5. Make Your Changes

Follow the project's coding standards:

- **Python** - Follow PEP 8, use type hints, match existing code style
- **YAML rules** - Follow the schema in `ariba-ruleset/schemas/rule.schema.json`
- **TypeScript/Next.js** - Use existing patterns in `ariba-dashboard/`
- **Add tests** - Include unit tests for new functionality

### 6. Run Checks Before Submission

Before submitting a PR, ensure:

```bash
# Linting
pylint ariba-manager/  # or whatever linter is configured

# Unit tests
pytest ariba-manager/tests/ -v

# Format check
black --check ariba-manager/  # or prettier for TS

# Security checks (if applicable)
```

### 7. Submit a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a PR against the `main` branch of the upstream repository

3. Fill out the PR template with:
   - **Summary** - What does this change do and why?
   - **Approach** - How did you implement the change?
   - **Testing** - What tests did you run and what were the results?
   - **Security impact** - Any security considerations or implications?
   - **Screenshots** (if UI-related)

## 🔍 Code Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function signatures
- Write docstrings for all public modules/classes
- Use f-strings for string formatting
- Handle exceptions properly (no bare `except:`)

### YAML Detection Rules

Every rule should include:

```yaml
id: ARIBA-UNIQUE-ID-1001
name: Rule Title
version: 1
enabled: true
severity: medium  # low, medium, high, critical

match:
  all:  # or any
    - field: event.category
      operator: equals
      value: web
    - field: http.url
      operator: regex
      value: "(?i)sql injection"

groups:
  - web_attack
  - sqli

mitre:
  tactic: Initial Access
  technique_id: T1190

actions:
  create_alert: true
  notify: false
```

### Next.js Dashboard

- Follow existing component patterns in `ariba-dashboard/src/`
- Use TypeScript with strict mode
- Tailwind CSS for styling
- Keep components focused and reusable

## 🧪 Testing Guidelines

### Unit Tests

- Test individual functions and methods
- Use fixtures from `tests/conftest.py`
- Aim for high coverage on new code

### Integration Tests

- Test end-to-end flows (agent → manager → indexer → dashboard)
- Use Docker Compose for test environments
- Test with real event samples when possible

### Test Data

- Place test fixtures in appropriate `tests/` directories
- Use realistic but non-sensitive data
- Include both positive and negative test cases

## 📦 Branch Naming Conventions

- `feature/short-description` - New features
- `bugfix/short-description` - Bug fixes
- `docs/short-description` - Documentation improvements
- `hotfix/short-description` - Critical production fixes

## 📬 Communication

- **Questions?** Open a discussion on the issue tracker
- **Pull Requests** - Use the PR template, respond to reviewer feedback
- **Issues** - Label appropriately, provide reproducible steps for bugs

## 🙏 Recognition

Contributors will be acknowledged in:
- Release notes
- `ACKNOWLEDGMENTS` file (if created)
- Project website (with permission)

Thank you for helping make Ariba Security Platform better! 🚀

## Need Help?

- Check the [Roadmap](README.md#roadmap) for planned features
- Look at existing [issues](https://github.com/bonisecurity/ariba-security-platform/issues)
- Review the [architecture](README.md#platform-architecture) section
- Examine existing [detection rules](ariba-ruleset/rules/) for patterns