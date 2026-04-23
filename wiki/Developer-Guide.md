# Developer Guide

This guide is for developers who want to contribute to the Tor VPN System.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Code Organization](#code-organization)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Building and Packaging](#building-and-packaging)
- [Contributing](#contributing)

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Tor 0.4.x+
- IDE (VS Code, PyCharm, or similar)
- Virtual environment tool (venv, conda, etc.)

### Initial Setup

#### 1. Clone Repository

```bash
git clone https://github.com/your-username/tor_vpn.git
cd tor_vpn
```

#### 2. Create Virtual Environment

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Using conda (alternative)
conda create -n tor_vpn python=3.11
conda activate tor_vpn
```

#### 3. Install Dependencies

```bash
# Base dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt
```

#### 4. Install Tor

```bash
# Linux
sudo apt install tor

# macOS
brew install tor

# Windows
# Download from https://www.torproject.org/
```

#### 5. Verify Setup

```bash
# Check Python version
python --version

# Check dependencies
pip list

# Check Tor
tor --version

# Run tests (if available)
pytest
```

---

## Development Environment

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120]
}
```

#### PyCharm

1. Open project
2. File > Settings > Project > Python Interpreter
3. Add new interpreter using existing environment
4. Select `.venv` directory
5. Enable code style inspection

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

Run hooks manually:
```bash
pre-commit run --all-files
```

---

## Project Structure

```
tor_vpn/
├── docs/                          # Documentation
├── wiki/                          # GitHub wiki
├── diagnostics/                   # Diagnostic outputs
├── tests/                         # Test files (to be created)
├── tor_vpn_beta.py               # Main GUI application
├── tor_custom_config.py          # Custom config generator
├── tor_auto_torrc_config.py      # Automated setup
├── tor_diagnostic_repair.py      # Diagnostic tool
├── tor_network_test.py           # Network tester
├── tor_route_traffic_setup.py    # Transparent proxy
├── tor_vpn_inclued.py            # Startup validation
├── setup_tor_custom.sh           # Bash setup script
├── tor_auto_proxy.sh             # Proxy GUI
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Dev dependencies
├── .gitignore                    # Git ignore
├── CHANGELOG.md                 # Version history
├── LICENSE                       # MIT License
└── README.md                     # Main README
```

---

## Code Organization

### Core Modules

- **tor_vpn_beta.py**: Main GUI application with Tkinter
- **tor_custom_config.py**: Configuration file management
- **tor_auto_torrc_config.py**: Automated setup and installation
- **tor_diagnostic_repair.py**: System diagnostics and repair
- **tor_network_test.py**: Network connectivity testing
- **tor_route_traffic_setup.py**: iptables and transparent proxy
- **tor_vpn_inclued.py**: Startup validation and management

### Shell Scripts

- **setup_tor_custom.sh**: System-level Tor configuration
- **tor_auto_proxy.sh**: Proxy management with Zenity GUI

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
- `style`: Code style changes
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

---

## Code Standards

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

---

## Testing

### Test Structure

```
tests/
├── __init__.py
├── utils.py                 # Test utilities and helpers
├── fixtures/
│   ├── __init__.py
│   └── conftest.py          # Pytest fixtures (100+ fixtures)
├── unit/                    # Unit tests for individual modules
│   ├── __init__.py
│   ├── test_tor_vpn_beta.py
│   ├── test_tor_custom_config.py
│   ├── test_tor_auto_torrc_config.py
│   ├── test_tor_diagnostic_repair.py
│   ├── test_tor_network_test.py
│   ├── test_tor_route_traffic_setup.py
│   └── test_tor_vpn_inclued.py
└── integration/             # Integration tests
    ├── __init__.py
    └── test_full_workflow.py
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

# Run tests requiring GUI (will be skipped if no GUI environment)
pytest -m gui

# Run tests requiring network (will be skipped if no network)
pytest -m network
```

### Test Coverage

The project aims for high test coverage:
- **Unit tests**: 350+ tests covering all Python modules
- **Integration tests**: 30+ tests for full workflows
- **Test fixtures**: 100+ fixtures for comprehensive mocking
- **Total**: 380+ tests

### Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.unit` - Unit tests (fast, no external dependencies)
- `@pytest.mark.integration` - Integration tests (slower, may require external services)
- `@pytest.mark.tor` - Tests requiring Tor to be installed/running
- `@pytest.mark.network` - Tests requiring network access
- `@pytest.mark.root` - Tests requiring root privileges
- `@pytest.mark.gui` - Tests requiring GUI environment
- `@pytest.mark.slow` - Slow-running tests

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

# Run tests requiring GUI (will be skipped if no GUI environment)
pytest -m gui

# Run tests requiring network (will be skipped if no network)
pytest -m network
```

### Writing Tests

```python
import pytest
from tor_custom_config import generate_hashed_password

def test_generate_hashed_password_success(mocker):
    """Test successful password hashing."""
    mock_result = mocker.Mock()
    mock_result.stdout = "16:ABCD1234"
    mocker.patch('subprocess.run', return_value=mock_result)
    
    result = generate_hashed_password("test_password")
    assert result == "16:ABCD1234"
```

### Test Coverage

Aim for:
- Overall coverage: >80%
- Critical security code: >90%
- Core functionality: >85%

---

## Building and Packaging

### Creating Distribution Packages

#### Using setuptools

Create `setup.py`:
```python
from setuptools import setup, find_packages

setup(
    name="tor-vpn",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "stem~=1.8.2",
        "psutil~=7.0.0",
    ],
    python_requires=">=3.10",
)
```

Build package:
```bash
pip install build
python -m build
```

#### Using PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile tor_vpn_beta.py
```

---

## Contributing

### Pull Request Process

1. Update documentation
2. Ensure tests pass
3. Run linters
4. Commit your changes
5. Push to your fork
6. Create Pull Request

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Security considerations addressed

### Code Review

- Respond to review comments promptly
- Make requested changes
- Update PR description if needed
- Keep commit history clean

---

## Additional Resources

- [Home](Home) - Wiki home page
- [Installation](Installation) - Installation guide
- [API Reference](API-Reference) - API documentation
- [Contributing Guidelines](../docs/CONTRIBUTING.md) - Detailed contributing guide
- [Development Documentation](../docs/DEVELOPMENT.md) - Comprehensive development guide

---

**Last Updated**: 2024-04-23
