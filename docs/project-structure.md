# Tor VPN System Project Structure

This document provides a comprehensive overview of the Tor VPN System project structure.

## Table of Contents

- [Root Directory](#root-directory)
- [Python Scripts](#python-scripts)
- [Shell Scripts](#shell-scripts)
- [Configuration Files](#configuration-files)
- [Documentation](#documentation)
- [Wiki](#wiki)
- [Tests](#tests)
- [Diagnostics](#diagnostics)
- [Git Configuration](#git-configuration)

---

## Root Directory

```
tor_vpn/
├── README.md                   # Main project README
├── CONTRIBUTING.md              # Contributing guidelines
├── INSTALL.md                   # Installation guide
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
├── SECURITY.md                  # Security policy
├── CODE_OF_CONDUCT.md           # Community guidelines
├── requirements.txt            # Python dependencies
├── requirements-dev.txt         # Development dependencies
├── .gitignore                   # Git ignore patterns
├── pytest.ini                   # Pytest configuration
├── docs/                        # Documentation directory
├── wiki/                        # GitHub wiki
├── tests/                       # Test suite
└── [Python Scripts]            # Main application scripts
```

---

## Python Scripts

### Core Application Scripts

```
tor_vpn_beta.py                 # Main GUI application (518 lines)
├── Purpose: Primary GUI for Tor VPN management
├── Dependencies: tkinter, stem, psutil
├── Features:
│   ├── Country selection for exit nodes
│   ├── Connect/Disconnect functionality
│   ├── Real-time status display
│   └── Configuration management
└── Security: Uses hashed password authentication

tor_custom_config.py             # Custom configuration generator (161 lines)
├── Purpose: Generate custom torrc configuration files
├── Dependencies: subprocess, os, shutil
├── Features:
│   ├── Password hashing with tor --hash-password
│   ├── Secure file permissions (600/700)
│   ├── User/group ownership management
│   └── Logging to create_torrc.log
└── Security: Hashes passwords, sets restricted permissions

tor_auto_torrc_config.py         # Automated setup script (188 lines)
├── Purpose: Automated Tor installation and configuration
├── Dependencies: subprocess, platform, os
├── Features:
│   ├── Cross-platform Tor installation
│   ├── Automatic directory setup
│   ├── Default configuration generation
│   └── Service management (systemd, init.d, launchd)
└── Security: Generates hashed control password

tor_diagnostic_repair.py        # Diagnostic and repair tool (509 lines)
├── Purpose: Diagnose and repair Tor issues
├── Dependencies: subprocess, psutil, argparse
├── Features:
│   ├── Init system detection (systemd, sysvinit, manual)
│   ├── Tor configuration validation
│   ├── Process management
│   ├── Service restart
│   └── Diagnostic data collection
└── Security: Validates sudo password securely

tor_network_test.py              # Network connectivity tester (221 lines)
├── Purpose: Test Tor network connectivity
├── Dependencies: stem, socket, requests, psutil
├── Features:
│   ├── Tor status checking
│   ├── Control port detection
│   ├── Password detection
│   ├── Authentication testing
│   ├── Latency measurement
│   └── Exit IP identification
└── Security: Tests authentication methods

tor_route_traffic_setup.py      # Transparent proxy setup (230 lines)
├── Purpose: Set up transparent proxy for all traffic
├── Dependencies: subprocess, os, pwd
├── Features:
│   ├── Root privilege check
│   ├── Tor process management
│   ├── Custom torrc generation
│   ├── iptables configuration
│   └── Connection verification
└── Security: Requires root, sets up iptables rules

tor_vpn_inclued.py               # Tor startup validation (156 lines)
├── Purpose: Validate Tor startup and configuration
├── Dependencies: subprocess, os, getpass, platform
├── Features:
│   ├── Tor running status check
│   ├── Password hashing
│   ├── Manual Tor startup
│   ├── Configuration validation
│   └── Platform-specific paths
└── Security: Secure password prompting
```

---

## Shell Scripts

```
setup_tor_custom.sh             # Bash setup script (107 lines)
├── Purpose: System-level Tor configuration setup
├── Dependencies: bash, tor, sudo
├── Features:
│   ├── Tor installation check
│   ├── Configuration directory setup
│   ├── Custom torrc generation
│   ├── Service management
│   └── Error handling
└── Security: Requires sudo, sets permissions

tor_auto_proxy.sh               # Proxy management GUI (119 lines)
├── Purpose: Zenity-based GUI for proxy management
├── Dependencies: bash, zenity, tor
├── Features:
│   ├── Country selection GUI
│   ├── Proxy enable/disable
│   ├── Status display
│   └── Error handling
└── Security: Runs as user, not root

tor_bash_gui.sh.py              # Empty placeholder (0 lines)
├── Purpose: Placeholder for future bash GUI
└── Status: Not implemented
```

---

## Configuration Files

```
requirements.txt                # Python dependencies
├── stem~=1.8.2                # Tor control library
└── psutil~=7.0.0              # System utilities

requirements-dev.txt            # Development dependencies
├── pytest                      # Testing framework
├── pytest-cov                  # Coverage plugin
├── flake8                      # Linter
├── black                       # Code formatter
├── mypy                        # Type checker
└── pylint                      # Linter

.gitignore                       # Git ignore patterns
├── .venv/                      # Virtual environment
├── __pycache__/                # Python cache
├── *.pyc                       # Compiled Python files
├── diagnostics/                # Diagnostic outputs
├── *.log                       # Log files
└── tor_bash_gui.sh.py          # Placeholder files

pytest.ini                       # Pytest configuration
├── Test path configuration
├── Marker definitions
├── Coverage settings
└── Warning filters
```

---

## Documentation

```
docs/
├── INDEX.md                     # Documentation index
├── README.md                    # Main documentation
├── CONTRIBUTING.md              # Contributing guidelines
├── INSTALL.md                   # Installation guide
├── DEVELOPMENT.md               # Development guide
├── CODE_OF_CONDUCT.md           # Community guidelines
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
├── SECURITY.md                  # Security policy
├── architecture.md              # System architecture
├── configuration-files.md      # Configuration documentation
├── python-scripts.md           # Python scripts documentation
└── shell-scripts.md            # Shell scripts documentation
```

---

## Wiki

```
wiki/
├── Home.md                      # Wiki home page
├── Installation.md              # Installation instructions
├── User-Guide.md                # User guide
├── Configuration.md             # Configuration guide
├── Troubleshooting.md          # Troubleshooting guide
├── Developer-Guide.md           # Developer guide
├── API-Reference.md            # API documentation
├── Security.md                  # Security documentation
└── FAQ.md                       # Frequently asked questions
```

---

## Tests

```
tests/
├── __init__.py                  # Test package init
├── utils.py                     # Test utilities
├── fixtures/
│   ├── __init__.py              # Fixtures package init
│   └── conftest.py              # Pytest fixtures (100+ fixtures)
├── unit/                        # Unit tests
│   ├── __init__.py
│   ├── test_tor_vpn_beta.py     # Main GUI tests (50+ tests)
│   ├── test_tor_custom_config.py # Config generator tests (50+ tests)
│   ├── test_tor_auto_torrc_config.py # Auto config tests (50+ tests)
│   ├── test_tor_diagnostic_repair.py # Diagnostic tests (50+ tests)
│   ├── test_tor_network_test.py  # Network test tests (50+ tests)
│   ├── test_tor_route_traffic_setup.py # Proxy setup tests (50+ tests)
│   ├── test_tor_vpn_inclued.py  # Startup validation tests (50+ tests)
│   ├── test_shell_scripts.py     # Shell script tests
│   ├── test_windows_platform.py  # Windows-specific tests
│   └── test_macos_platform.py   # macOS-specific tests
└── integration/                 # Integration tests
    ├── __init__.py
    ├── test_full_workflow.py    # Full workflow tests
    ├── test_cross_platform.py   # Cross-platform tests
    └── test_end_to_end.py       # End-to-end workflow tests
```

---

## Diagnostics

```
diagnostics/                      # Diagnostic outputs (gitignored)
├── torrc                        # Tor configuration snapshot
├── system_info.txt              # System information
├── network_info.txt             # Network information
└── logs/                        # Diagnostic logs
```

---

## Git Configuration

```
.git/                            # Git repository
├── HEAD                         # Current branch reference
├── config/                      # Repository configuration
├── objects/                     # Git objects
├── refs/                        # Branch and tag references
└── hooks/                       # Git hooks
```

---

## File Size Summary

```
Python Scripts:
├── tor_vpn_beta.py:              ~20 KB (518 lines)
├── tor_custom_config.py:         ~6 KB (161 lines)
├── tor_auto_torrc_config.py:     ~7 KB (188 lines)
├── tor_diagnostic_repair.py:    ~20 KB (509 lines)
├── tor_network_test.py:         ~8 KB (221 lines)
├── tor_route_traffic_setup.py:  ~9 KB (230 lines)
└── tor_vpn_inclued.py:          ~6 KB (156 lines)

Shell Scripts:
├── setup_tor_custom.sh:          ~4 KB (107 lines)
└── tor_auto_proxy.sh:            ~4 KB (119 lines)

Tests:
├── Unit tests:                   ~160 KB (500+ tests)
├── Integration tests:            ~80 KB (100+ tests)
├── Fixtures:                    ~25 KB (100+ fixtures)
└── Utils:                       ~17 KB

Documentation:
├── docs/:                        ~200 KB
├── wiki/:                        ~400 KB
└── Root docs:                    ~50 KB
```

---

## Platform-Specific Paths

### Linux
- Tor binary: `/usr/bin/tor` or `/usr/local/bin/tor`
- Config: `/etc/tor/torrc` or `~/.tor_config/torrc`
- Data: `/var/lib/tor` or `~/.tor_config/data`
- Logs: `/var/log/tor/` or `~/.tor_config/logs`
- Service: systemd (`systemctl`) or init.d (`service`)

### macOS
- Tor binary: `/usr/local/bin/tor` (Homebrew) or `/opt/homebrew/bin/tor`
- Config: `/usr/local/etc/tor/torrc` or `~/.tor_config/torrc`
- Data: `/usr/local/var/lib/tor` or `~/.tor_config/data`
- Logs: `/usr/local/var/log/tor/` or `~/Library/Logs/tor`
- Service: launchd (`launchctl`)

### Windows
- Tor binary: `C:\Program Files\Tor\tor.exe`
- Config: `C:\Program Files\Tor\torrc` or `%APPDATA%\tor\torrc`
- Data: `C:\Program Files\Tor\Data` or `%APPDATA%\tor\data`
- Logs: `C:\Program Files\Tor\Logs` or `%APPDATA%\tor\logs`
- Service: Windows Service (`sc.exe`)

---

## Network Configuration

### Tor Ports
- **Control Port**: 9051 (Tor control interface)
- **Socks Port**: 9050 (SOCKS proxy)
- **TransPort**: 9040 (Transparent proxy)
- **DNS Port**: 5353 (DNS proxy)

### iptables Rules (Linux)
- NAT table for transparent proxy
- Filter table for owner-based routing
- DNS redirection to Tor DNS port

### pf Rules (macOS)
- Packet Filter for transparent proxy
- DNS redirection rules
- Port forwarding configuration

### Windows Firewall
- Inbound rules for Tor ports
- Outbound rules for Tor traffic
- DNS exception rules

---

## Security Architecture

### Authentication
- Hashed control passwords (using `tor --hash-password`)
- Authentication cookie support
- Password prompting with `getpass`

### File Permissions
- torrc files: 600 (owner read/write only)
- Config directories: 700 (owner read/write/execute only)
- Data directories: 700 (owner read/write/execute only)

### Known Security Issues
- Hardcoded default passwords (to be removed)
- Sudo requirement for some operations
- Tor should not run as root (except for iptables setup)

---

## Development Workflow

1. **Setup**: Clone repository, create virtual environment, install dependencies
2. **Development**: Write code, run tests, update documentation
3. **Testing**: Run unit tests, integration tests, and coverage reports
4. **Review**: Code review, security audit, documentation review
5. **Release**: Update version, create changelog, tag release

---

## Dependencies

### Python Dependencies
- `stem~=1.8.2` - Tor control library
- `psutil~=7.0.0` - System and process utilities

### Development Dependencies
- `pytest` - Testing framework
- `pytest-cov` - Coverage plugin
- `flake8` - Linter
- `black` - Code formatter
- `mypy` - Type checker

### System Dependencies
- Tor 0.4.x+
- Python 3.10+
- tkinter (for GUI)
- zenity (for shell GUI on Linux/macOS)
- iptables (for transparent proxy on Linux)

---

## Supported Countries

The system supports exit node selection for the following countries:

- **us** - United States
- **de** - Germany
- **gb** - United Kingdom
- **fr** - France
- **jp** - Japan

Additional countries can be added to the `SERVERS` dictionary in `tor_vpn_beta.py`.

---

## Logging

### Log Files
- `vpn_app_advanced.log` - Advanced application logs
- `logfile.log` - General application logs
- `create_torrc.log` - Configuration generation logs
- `setup_tor.log` - Setup script logs
- `tor_management_gui.log` - GUI management logs

### Log Rotation
- Python `RotatingFileHandler` for log rotation
- Maximum size: 1,000,000 bytes
- Backup count: 5 files

---

## Testing Coverage

### Unit Tests (500+ tests)
- All Python scripts
- Platform-specific functionality
- Security features
- Error handling

### Integration Tests (100+ tests)
- Full workflows
- Cross-platform compatibility
- End-to-end scenarios

### Test Fixtures (100+ fixtures)
- Mock objects
- Temporary directories
- Configuration mocks
- Platform mocks

---

## Version Information

- **Current Version**: Unreleased
- **Python Version**: 3.10+
- **Tor Version**: 0.4.x+
- **Stem Version**: 1.8.2+
- **psutil Version**: 7.0.0+

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

---

## Support

- Documentation: [docs/INDEX.md](docs/INDEX.md)
- Wiki: [wiki/Home.md](wiki/Home.md)
- Issues: GitHub Issues
