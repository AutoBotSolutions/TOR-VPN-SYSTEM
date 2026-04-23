# Tor VPN System Wiki

Welcome to the Tor VPN System documentation wiki. This comprehensive system provides tools for configuring, managing, and routing traffic through the Tor network with both GUI and CLI interfaces.

## Quick Navigation

- [Installation Guide](Installation) - Get started with installation
- [User Guide](User-Guide) - Learn how to use the system
- [Configuration](Configuration) - Configure Tor settings
- [Troubleshooting](Troubleshooting) - Solve common issues
- [Developer Guide](Developer-Guide) - Contribute to development
- [API Reference](API-Reference) - Python API documentation
- [Security](Security) - Security considerations
- [FAQ](FAQ) - Frequently asked questions

## Overview

The Tor VPN System is a comprehensive management tool for the Tor network that includes:

### Key Features

- 🌍 **Country-specific Exit Nodes** - Select from 200+ countries
- 🔐 **Multiple Authentication Methods** - Password and cookie-based
- 🔄 **Transparent Proxy** - System-wide traffic routing
- 💻 **Cross-platform Support** - Linux, macOS, Windows
- 🛠️ **Diagnostic Tools** - System health monitoring
- 🖥️ **GUI and CLI Interfaces** - Both graphical and command-line
- 📊 **Network Testing** - Latency and performance metrics
- ⚙️ **Automated Setup** - One-click configuration

## Components

### Python Scripts

- **tor_vpn_beta.py** - Main GUI application with country selection
- **tor_custom_config.py** - Custom configuration generator
- **tor_auto_torrc_config.py** - Automated setup script
- **tor_diagnostic_repair.py** - Diagnostic and repair tool
- **tor_network_test.py** - Network connectivity tester
- **tor_route_traffic_setup.py** - Transparent proxy setup
- **tor_vpn_inclued.py** - Tor startup validation

### Shell Scripts

- **setup_tor_custom.sh** - Bash setup script for custom configuration
- **tor_auto_proxy.sh** - Zenity-based proxy management GUI

## Quick Start

### Prerequisites

- Python 3.10+
- Tor 0.4.x+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
cd tor_vpn

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install Tor
sudo apt install tor  # Linux
brew install tor      # macOS
```

### Running the Application

```bash
# GUI application
python tor_vpn_beta.py

# Automated setup
python tor_auto_torrc_config.py

# Network test
python tor_network_test.py

# Diagnostics
python tor_diagnostic_repair.py
```

## Documentation Structure

### User Documentation

- **[Installation](Installation)** - Detailed installation instructions for all platforms
- **[User Guide](User-Guide)** - Comprehensive user guide with examples
- **[Configuration](Configuration)** - Configuration options and parameters
- **[Troubleshooting](Troubleshooting)** - Common issues and solutions
- **[FAQ](FAQ)** - Frequently asked questions

### Developer Documentation

- **[Developer Guide](Developer-Guide)** - Development setup and workflow
- **[API Reference](API-Reference)** - Python API documentation
- **[Contributing](../docs/CONTRIBUTING.md)** - Contribution guidelines
- **[Development](../docs/DEVELOPMENT.md)** - Development documentation

### System Documentation

- **[Security](Security)** - Security considerations and best practices
- **[Architecture](../docs/architecture.md)** - System architecture and workflows
- **[Python Scripts](../docs/python-scripts.md)** - Python scripts documentation
- **[Shell Scripts](../docs/shell-scripts.md)** - Shell scripts documentation

## System Requirements

### Minimum Requirements

- **OS**: Linux (Ubuntu 20.04+), macOS 10.15+, Windows 10+
- **Python**: 3.10 or higher
- **RAM**: 2 GB minimum, 4 GB recommended
- **Disk**: 500 MB for installation, 1 GB for logs and data

### Recommended Requirements

- **OS**: Linux (Ubuntu 22.04+), macOS 12+, Windows 11
- **Python**: 3.11 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk**: 2 GB for installation and data

## Supported Platforms

### Linux
- Ubuntu 20.04, 22.04+
- Debian 11+
- Fedora 36+
- Arch Linux
- Other systemd-based distributions

### macOS
- macOS 10.15 (Catalina) and later
- macOS 12 (Monterey) and later recommended

### Windows
- Windows 10 and later
- Windows 11 recommended
- WSL (Windows Subsystem for Linux) supported

## Dependencies

### Python Dependencies

```
stem~=1.8.2    # Tor control library
psutil~=7.0.0  # System utilities
```

### System Dependencies

- Tor (tor package)
- iptables (for transparent proxy on Linux)
- zenity (for GUI scripts on Linux)
- systemd or init.d (service management)

## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

## Support

- **Documentation**: Check the wiki pages
- **Issues**: [GitHub Issues](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/discussions)
- **Email**: [To be added]

## Contributing

We welcome contributions! See [Contributing Guidelines](../docs/CONTRIBUTING.md) for details.

## Roadmap

### Version 1.1.0 (Planned)
- Remove hardcoded passwords
- Implement proper key management
- Add automated testing suite
- Improve input validation

### Version 1.2.0 (Planned)
- Multi-user support
- Multiple Tor instances
- Load balancing
- Enhanced GUI features

### Version 2.0.0 (Planned)
- Complete security overhaul
- Plugin architecture
- REST API
- Web-based interface

See [CHANGELOG](../CHANGELOG.md) for complete version history.

## Community

- **Code of Conduct**: [CODE_OF_CONDUCT.md](../docs/CODE_OF_CONDUCT.md)
- **Contributors**: See [CONTRIBUTING.md](../docs/CONTRIBUTING.md)
- **Acknowledgments**: See main [README](../README.md)

## Quick Links

- [Main Repository](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM)
- [Documentation Index](../docs/INDEX.md)
- [Installation Guide](Installation)
- [API Reference](API-Reference)
- [Troubleshooting](Troubleshooting)

---

**Last Updated**: 2024-04-23
