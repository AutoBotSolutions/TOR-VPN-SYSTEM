# Contributing to Tor VPN System

Thank you for your interest in contributing to the Tor VPN System! This document provides guidelines and instructions for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

### Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or insults
- Public or private harassment
- Publishing others' private information
- Any other conduct that could be considered inappropriate

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Basic knowledge of Python, Bash, and Tor

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Fork the repository on GitHub
   git clone https://github.com/YOUR_USERNAME/tor_vpn.git
   cd tor_vpn
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install Tor**
   ```bash
   sudo apt install tor  # Linux
   brew install tor      # macOS
   ```

5. **Run tests** (if available)
   ```bash
   pytest
   ```

---

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `docs/*` - Documentation changes

### Creating a Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in your feature branch
2. Follow coding standards (see below)
3. Write/update tests
4. Update documentation
5. Commit your changes

### Commit Messages

Follow conventional commit format:

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(gui): add country search filter

Add a search box in the servers tab to filter countries
by name or code.

Closes #123
```

```
fix(auth): resolve password hashing error on macOS

The tor binary path was not correctly detected on macOS,
causing password hashing to fail. This fix adds proper
path detection for macOS.

Fixes #456
```

---

## Coding Standards

### Python Code Style

Follow PEP 8 guidelines:

```python
# Good
def connect_to_tor(country_code):
    """Connect to Tor using the specified country code."""
    if not country_code:
        raise ValueError("Country code is required")
    
    try:
        # Implementation
        pass
    except Exception as e:
        logging.error(f"Failed to connect: {e}")
        raise

# Bad
def connect(c):
    if not c: raise Exception()
    # Implementation
```

### Documentation Strings

Use Google style docstrings:

```python
def authenticate_to_tor(controller, password):
    """Authenticate to Tor controller using password.
    
    Args:
        controller (Controller): Stem controller instance
        password (str): Plain-text password for authentication
        
    Returns:
        bool: True if authentication successful, False otherwise
        
    Raises:
        AuthenticationError: If authentication fails
    """
    try:
        controller.authenticate(password=password)
        return True
    except Exception as e:
        raise AuthenticationError(f"Authentication failed: {e}")
```

### Error Handling

- Always handle exceptions appropriately
- Log errors with context
- Provide meaningful error messages
- Use custom exceptions for domain-specific errors

```python
# Good
try:
    result = subprocess.run(command, check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    logging.error(f"Command failed: {command}")
    logging.error(f"Error output: {e.stderr}")
    raise TorCommandError(f"Failed to execute command: {e}")
```

### Security Best Practices

⚠️ **CRITICAL:** Never commit:
- Hardcoded passwords
- API keys
- Private keys
- Sensitive configuration

**Use environment variables:**
```python
# Good
import os
password = os.environ.get("TOR_PASSWORD")
if not password:
    raise ValueError("TOR_PASSWORD environment variable not set")

# Bad
password = "hardcoded_password_123"
```

### Shell Script Style

Follow Google Shell Style Guide:

```bash
# Good
#!/bin/bash
set -euo pipefail

function setup_tor_config() {
    local config_dir="$1"
    
    if [[ -z "${config_dir}" ]]; then
        echo "Error: Config directory required" >&2
        return 1
    fi
    
    mkdir -p "${config_dir}"
    chmod 700 "${config_dir}"
}

# Bad
function setup(){
dir=$1
mkdir $dir
}
```

---

## Testing

### Writing Tests

Create tests for new features:

```python
# tests/test_tor_connection.py
import pytest
from tor_vpn_beta import connect_to_tor

def test_connect_to_tor_valid_country():
    """Test connection with valid country code."""
    result = connect_to_tor("us")
    assert result is True

def test_connect_to_tor_invalid_country():
    """Test connection with invalid country code raises error."""
    with pytest.raises(ValueError):
        connect_to_tor("invalid")
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/unit/test_tor_vpn_beta.py

# Run with verbose output
pytest -v

# Run with coverage and detailed report
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run tests matching a pattern
pytest -k "test_connect"

# Run tests excluding slow tests
pytest -m "not slow"

# Run tests requiring Tor (will be skipped if Tor not available)
pytest -m tor

# Run tests requiring root (will be skipped if not root)
pytest -m root
```

### Test Coverage

Aim for >80% code coverage for new features. Critical security components should have >90% coverage.

---

## Documentation

### Code Documentation

- Document all public functions with docstrings
- Document complex algorithms
- Add inline comments for non-obvious code
- Keep documentation in sync with code

### User Documentation

- Update README.md for user-facing changes
- Update relevant documentation in docs/
- Add examples for new features
- Update configuration file documentation

### API Documentation

If adding new APIs:
- Document all endpoints/functions
- Provide usage examples
- Document parameters and return values
- Include error conditions

---

## Submitting Changes

### Pull Request Process

1. **Update documentation**
   - Ensure README is updated
   - Add/update relevant docs
   - Update CHANGELOG.md

2. **Ensure tests pass**
   ```bash
   pytest
   ```

3. **Run linters**
   ```bash
   # If linters are configured
   flake8 .
   black --check .
   mypy .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Provide a clear description of changes
   - Reference related issues
   - Link to relevant documentation

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Commit messages follow conventional format
- [ ] No hardcoded secrets or sensitive data
- [ ] Changes are backwards compatible (if applicable)
- [ ] CHANGELOG.md updated

---

## Reporting Issues

### Bug Reports

When reporting bugs, include:

1. **Environment Information**
   - OS and version
   - Python version
   - Tor version
   - Stem version

2. **Steps to Reproduce**
   ```bash
   # Commands to reproduce
   python tor_vpn_beta.py
   # Click connect button
   # Enter country code: us
   # Error occurs
   ```

3. **Expected Behavior**
   - What should happen

4. **Actual Behavior**
   - What actually happens
   - Error messages/stack traces

5. **Additional Context**
   - Configuration files (sanitized)
   - Log files (relevant portions)
   - Screenshots if applicable

### Feature Requests

When requesting features:

1. **Describe the Feature**
   - Clear description of what you want
   - Why it's needed
   - Use cases

2. **Proposed Solution**
   - How you envision it working
   - API changes (if any)
   - UI changes (if any)

3. **Alternatives Considered**
   - Other approaches you considered
   - Why they were rejected

4. **Additional Context**
   - Related issues or PRs
   - Examples from other projects
   - Mockups or diagrams

---

## Security Issues

⚠️ **Security vulnerabilities should NOT be reported publicly.**

For security issues:
1. Send an email to the project maintainers
2. Include "SECURITY" in the subject line
3. Provide detailed description of the vulnerability
4. Wait for acknowledgment before disclosure
5. Follow the maintainers' guidance for disclosure

See [SECURITY.md](SECURITY.md) for more information.

---

## Getting Help

### Resources

- **Documentation**: See `/docs` directory
- **Wiki**: See `/wiki` directory
- **Issues**: Check existing issues on GitHub
- **Discussions**: Use project discussions for questions

### Asking Questions

When asking for help:

1. Search existing issues and discussions first
2. Provide context:
   - What you're trying to do
   - What you've tried
   - Expected vs actual behavior
   - Error messages
3. Include relevant code snippets
4. Be patient and respectful

---

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file (to be created)
- Release notes
- Project documentation

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

## Contact

- **Maintainers**: [To be added - replace with actual maintainers]
- **Email**: [To be added - replace with contact email]
- **Discord/Slack**: [To be added - if applicable]

---

Thank you for contributing to the Tor VPN System!
