# Development Guide

This guide provides comprehensive information for developers working on the Tor VPN System.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Code Organization](#code-organization)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Debugging](#debugging)
- [Building and Packaging](#building-and-packaging)
- [Continuous Integration](#continuous-integration)
- [Performance Profiling](#performance-profiling)
- [Security Development](#security-development)

---

## Development Environment Setup

### Prerequisites

- Python 3.10+
- Git
- Tor 0.4.x+
- IDE (VS Code, PyCharm, or similar)
- Virtual environment tool (venv, conda, etc.)

### Initial Setup

#### 1. Clone Repository

```bash
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
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

#### 3. Install Development Dependencies

```bash
# Install base dependencies
pip install -r requirements.txt

# Install development dependencies (create requirements-dev.txt if needed)
pip install pytest pytest-cov flake8 black mypy pylint
pip install pre-commit
```

#### 4. Install Tor

```bash
# Linux
sudo apt install tor  # Ubuntu/Debian
sudo dnf install tor  # Fedora
sudo pacman -S tor    # Arch

# macOS
brew install tor

# Windows
# Download from https://www.torproject.org/
```

#### 5. Configure Pre-commit Hooks

```bash
pre-commit install
```

#### 6. Run Initial Tests

```bash
python -m pytest
```

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
    "editor.rulers": [88, 120],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".venv": true
    }
}
```

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Python: Tor VPN Beta",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/tor_vpn_beta.py",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

#### PyCharm

1. Open project
2. File > Settings > Project > Python Interpreter
3. Add new interpreter using existing environment
4. Select `.venv` directory
5. Enable code style inspection (Settings > Tools > External Tools)

---

## Project Structure

```
tor_vpn/
├── docs/                          # Documentation
│   ├── INDEX.md                   # Documentation index
│   ├── README.md                  # Main documentation
│   ├── python-scripts.md          # Python scripts docs
│   ├── shell-scripts.md           # Shell scripts docs
│   ├── configuration-files.md     # Configuration docs
│   ├── architecture.md            # Architecture docs
│   ├── CONTRIBUTING.md            # Contributing guidelines
│   ├── INSTALL.md                 # Installation guide
│   └── DEVELOPMENT.md             # This file
├── diagnostics/                   # Diagnostic outputs
│   ├── logfile.log               # Diagnostic logs
│   ├── system_info.txt           # System information
│   └── torrc                     # Tor config snapshot
├── tests/                         # Test files (to be created)
│   ├── __init__.py
│   ├── test_tor_connection.py
│   ├── test_configuration.py
│   └── test_network_test.py
├── tor_vpn_beta.py               # Main GUI application
├── tor_custom_config.py          # Custom config generator
├── tor_auto_torrc_config.py      # Automated setup
├── tor_diagnostic_repair.py      # Diagnostic tool
├── tor_network_test.py           # Network tester
├── tor_route_traffic_setup.py    # Transparent proxy
├── tor_vpn_inclued.py            # Startup validation
├── setup_tor_custom.sh           # Bash setup script
├── tor_auto_proxy.sh             # Proxy GUI
├── tor_bash_gui.sh.py            # (placeholder)
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Dev dependencies (to be created)
├── .pre-commit-config.yaml       # Pre-commit hooks (to be created)
├── .gitignore                    # Git ignore (to be created)
└── LICENSE                       # License file (to be added)
```

---

## Code Organization

### Module Structure

#### Core Modules

- **tor_vpn_beta.py**: Main GUI application with Tkinter
- **tor_custom_config.py**: Configuration file management
- **tor_auto_torrc_config.py**: Automated setup and installation
- **tor_diagnostic_repair.py**: System diagnostics and repair
- **tor_network_test.py**: Network connectivity testing
- **tor_route_traffic_setup.py**: iptables and transparent proxy
- **tor_vpn_inclued.py**: Startup validation and management

#### Shell Scripts

- **setup_tor_custom.sh**: System-level Tor configuration
- **tor_auto_proxy.sh**: Proxy management with Zenity GUI

### Code Patterns

#### Configuration Management

```python
# Pattern for configuration loading
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".tor_config"
CONFIG_FILE = CONFIG_DIR / "torrc"

def load_config():
    """Load Tor configuration from file."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
    
    with open(CONFIG_FILE, 'r') as f:
        return f.read()
```

#### Logging Pattern

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(name, log_file):
    """Standard logging setup."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

#### Stem Controller Pattern

```python
from stem.control import Controller
from stem import Signal

def with_tor_controller(operation):
    """Context manager for Tor controller operations."""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=get_password())
            return operation(controller)
    except Exception as e:
        logging.error(f"Tor controller operation failed: {e}")
        raise

# Usage
def set_exit_node(country_code):
    def operation(controller):
        controller.set_conf("ExitNodes", f"{{{country_code}}}")
        controller.signal(Signal.NEWNYM)
    
    with_tor_controller(operation)
```

#### Error Handling Pattern

```python
import logging
from typing import Optional, TypeVar, Callable

T = TypeVar('T')

def handle_errors(
    operation: Callable[[], T],
    error_message: str,
    default: Optional[T] = None
) -> Optional[T]:
    """Standard error handling wrapper."""
    try:
        return operation()
    except FileNotFoundError as e:
        logging.error(f"{error_message}: File not found - {e}")
        return default
    except PermissionError as e:
        logging.error(f"{error_message}: Permission denied - {e}")
        return default
    except Exception as e:
        logging.error(f"{error_message}: Unexpected error - {e}")
        return default
```

---

## Development Workflow

### Feature Development

#### 1. Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

#### 2. Implement Feature

- Write code following project standards
- Add tests for new functionality
- Update documentation
- Follow security best practices

#### 3. Test Locally

```bash
# Run linters
flake8 .
black --check .
mypy .

# Run tests
pytest

# Run specific test
pytest tests/test_specific_feature.py

# Run with coverage
pytest --cov=. --cov-report=html
```

#### 4. Commit Changes

```bash
git add .
git commit -m "feat: description of your feature"
```

#### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

### Bug Fix Development

#### 1. Create Bugfix Branch

```bash
git checkout develop
git pull origin develop
git checkout -b bugfix/issue-number-description
```

#### 2. Implement Fix

- Reproduce the bug
- Write failing test
- Fix the bug
- Ensure test passes

#### 3. Test and Commit

```bash
pytest
git add .
git commit -m "fix: description of bug fix"
```

### Code Review Process

#### Before Submitting PR

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Security considerations addressed

#### During Review

- Respond to review comments promptly
- Make requested changes
- Update PR description if needed
- Keep commit history clean

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

### Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.unit` - Unit tests (fast, no external dependencies)
- `@pytest.mark.integration` - Integration tests (slower, may require external services)
- `@pytest.mark.tor` - Tests requiring Tor to be installed/running
- `@pytest.mark.network` - Tests requiring network access
- `@pytest.mark.root` - Tests requiring root privileges
- `@pytest.mark.gui` - Tests requiring GUI environment
- `@pytest.mark.slow` - Slow-running tests

### Writing Tests

#### Unit Tests

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

def test_generate_hashed_password_failure(mocker):
    """Test password hashing failure."""
    mocker.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd'))
    
    with pytest.raises(subprocess.CalledProcessError):
        generate_hashed_password("test_password")
```

#### Integration Tests

```python
import pytest
from stem.control import Controller

def test_tor_controller_connection():
    """Test actual Tor controller connection."""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            assert controller.is_alive()
    except Exception as e:
        pytest.skip(f"Tor not available: {e}")
```

#### Fixtures

```python
# conftest.py
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_config_dir():
    """Create temporary config directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        yield config_dir

@pytest.fixture
def mock_tor_controller(mocker):
    """Mock Tor controller for testing."""
    mock_controller = mocker.Mock(spec=Controller)
    mock_controller.is_alive.return_value = True
    return mock_controller
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_configuration.py

# Run specific test
pytest tests/test_configuration.py::test_generate_hashed_password

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run only failed tests from last run
pytest --lf

# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l
```

### Test Coverage

Aim for:
- **Overall coverage**: >80%
- **Critical security code**: >90%
- **Core functionality**: >85%

Generate coverage report:
```bash
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

---

## Debugging

### Python Debugging

#### Using pdb

```python
import pdb; pdb.set_trace()
```

#### Using VS Code Debugger

1. Set breakpoints by clicking line numbers
2. Press F5 to start debugging
3. Use debug panel to step through code

#### Logging for Debugging

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Debug statements
logger.debug(f"Variable value: {variable}")
logger.debug(f"Function called with args: {args}")
```

### Tor Debugging

#### Enable Tor Debug Logging

Add to torrc:
```
Log debug file /var/log/tor/debug.log
```

#### Check Tor Logs

```bash
# Linux
sudo journalctl -u tor -f

# Check Tor log file
tail -f /var/log/tor/notices.log
```

#### Test Tor Control Port

```python
from stem.control import Controller

try:
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        print("Connected to Tor controller")
        print(f"Tor version: {controller.get_version()}")
except Exception as e:
    print(f"Failed to connect: {e}")
```

### Common Debugging Scenarios

#### Connection Issues

```python
# Test Tor connectivity
def test_tor_connectivity():
    import socket
    try:
        sock = socket.create_connection(("127.0.0.1", 9051), timeout=5)
        sock.close()
        print("Tor control port is accessible")
    except socket.error:
        print("Tor control port is not accessible")
```

#### Permission Issues

```python
import os
import stat

def check_permissions(path):
    """Check file permissions."""
    mode = os.stat(path).st_mode
    print(f"Permissions: {stat.filemode(mode)}")
    print(f"Owner: {os.stat(path).st_uid}")
    print(f"Group: {os.stat(path).st_gid}")
```

#### Configuration Issues

```python
def validate_torrc(torrc_path):
    """Validate torrc configuration."""
    result = subprocess.run(
        ["tor", "--verify-config", "-f", torrc_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"Errors: {result.stderr}")
```

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
    entry_points={
        "console_scripts": [
            "tor-vpn=tor_vpn_beta:main",
        ],
    },
    python_requires=">=3.10",
)
```

Build package:
```bash
pip install build
python -m build
```

#### Using PyInstaller (for executables)

```bash
pip install pyinstaller

# Build single executable
pyinstaller --onefile tor_vpn_beta.py

# Build with windowed mode (no console)
pyinstaller --onefile --windowed tor_vpn_beta.py
```

### Docker Containerization

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# Install Tor
RUN apt-get update && apt-get install -y tor

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Expose Tor ports
EXPOSE 9050 9051

# Run application
CMD ["python", "tor_vpn_beta.py"]
```

Build and run:
```bash
docker build -t tor-vpn .
docker run -it --net=host tor-vpn
```

---

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/ci.yml`:
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Format check with black
      run: |
        black --check .
    
    - name: Test with pytest
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

### Pre-commit Configuration

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## Performance Profiling

### Profiling Python Code

#### Using cProfile

```python
import cProfile
import pstats

def profile_function():
    """Profile a function."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    result = some_function()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    return result
```

#### Using memory_profiler

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Profile memory usage."""
    # Your code here
    pass
```

Run with:
```bash
python -m memory_profiler your_script.py
```

### Profiling Tor Performance

#### Monitor Tor Resources

```python
import psutil

def monitor_tor_resources():
    """Monitor Tor process resources."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'tor':
            print(f"PID: {proc.info['pid']}")
            print(f"CPU: {proc.cpu_percent()}%")
            print(f"Memory: {proc.memory_info().rss / 1024 / 1024:.2f} MB")
            print(f"Threads: {proc.num_threads()}")
```

#### Measure Circuit Build Time

```python
import time
from stem.control import Controller

def measure_circuit_build_time():
    """Measure time to build Tor circuit."""
    start = time.time()
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        # Wait for circuit to build
        time.sleep(5)
    end = time.time()
    print(f"Circuit build time: {end - start:.2f} seconds")
```

---

## Security Development

### Secure Coding Practices

#### Input Validation

```python
def validate_country_code(country_code: str) -> str:
    """Validate and sanitize country code input."""
    if not isinstance(country_code, str):
        raise TypeError("Country code must be a string")
    
    if len(country_code) != 2:
        raise ValueError("Country code must be 2 characters")
    
    if not country_code.isalpha():
        raise ValueError("Country code must contain only letters")
    
    return country_code.lower()
```

#### Secret Management

```python
import os
from typing import Optional

def get_tor_password() -> str:
    """Get Tor password from environment variable."""
    password = os.environ.get("TOR_PASSWORD")
    if not password:
        raise ValueError("TOR_PASSWORD environment variable not set")
    return password

# Never hardcode secrets
# BAD: password = "hardcoded_password"
# GOOD: password = os.environ.get("TOR_PASSWORD")
```

#### Secure File Operations

```python
import os
import tempfile
from pathlib import Path

def secure_write_file(path: Path, content: str) -> None:
    """Securely write content to file."""
    # Write to temporary file first
    fd, temp_path = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        
        # Set permissions before moving
        os.chmod(temp_path, 0o600)
        
        # Atomic rename
        os.rename(temp_path, path)
    except Exception:
        # Clean up on failure
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise
```

### Security Testing

#### Dependency Scanning

```bash
pip install safety
safety check
```

#### Code Security Analysis

```bash
pip install bandit
bandit -r .
```

#### Secret Scanning

```bash
pip install truffleHog
trufflehog --regex --entropy=False /path/to/repo
```

---

## Additional Resources

### Documentation

- [Python Documentation](https://docs.python.org/3)
- [Stem Library](https://stem.torproject.org)
- [Tor Project Documentation](https://torproject.org/docs)
- [Project Documentation](docs/INDEX.md)

### Tools

- [Black](https://black.readthedocs.io/) - Code formatter
- [Flake8](https://flake8.pycqa.org/) - Linter
- [MyPy](https://mypy.readthedocs.io/) - Type checker
- [Pytest](https://docs.pytest.org/) - Testing framework
- [Pre-commit](https://pre-commit.com/) - Git hooks

### Best Practices

- [PEP 8](https://peps.python.org/pep-0008/) - Style guide
- [PEP 257](https://peps.python.org/pep-0257/) - Docstring conventions
- [The Zen of Python](https://www.python.org/dev/peps/pep-0020/)

---

For questions or issues, see [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue on the project repository.
