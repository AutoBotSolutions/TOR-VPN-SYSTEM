# Tor VPN System

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)
![Tor](https://img.shields.io/badge/Tor-0.4.x+-purple.svg)

**A comprehensive Tor VPN management system with GUI and CLI interfaces**

[Documentation](docs/INDEX.md) • [Installation](docs/INSTALL.md) • [Contributing](CONTRIBUTING.md) • [Issues](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/issues)

</div>

## Overview

Tor VPN System is a comprehensive management tool for configuring, managing, and routing traffic through the Tor network. It provides both graphical (GUI) and command-line (CLI) interfaces, making it accessible for users of all technical levels.

### Key Features

- 🌍 **Country-specific Exit Nodes**: Support for 200+ countries with exit node selection
- 🔐 **Multiple Authentication Methods**: Password-based and cookie-based authentication
- 🔄 **Transparent Proxy**: System-wide traffic routing through Tor
- 💻 **Cross-platform Support**: Linux, macOS, and Windows compatibility
- 🛠️ **Diagnostic Tools**: Comprehensive system diagnostics and repair utilities
- 🖥️ **GUI and CLI Interfaces**: Both graphical and command-line interfaces
- 📊 **Network Testing**: Latency measurement and exit IP detection
- ⚙️ **Automated Setup**: One-click Tor configuration and installation

## Project Structure

```
tor_vpn/
├── docs/                          # Documentation
│   ├── INDEX.md                   # Documentation index
│   ├── README.md                  # Detailed documentation
│   ├── python-scripts.md          # Python scripts docs
│   ├── shell-scripts.md           # Shell scripts docs
│   ├── configuration-files.md     # Configuration docs
│   ├── architecture.md            # Architecture docs
│   ├── CONTRIBUTING.md            # Contributing guidelines
│   ├── INSTALL.md                 # Installation guide
│   ├── DEVELOPMENT.md             # Development guide
│   └── CODE_OF_CONDUCT.md         # Community guidelines
├── diagnostics/                   # Diagnostic outputs
├── tor_vpn_beta.py               # Main GUI application
├── tor_custom_config.py          # Configuration generator
├── tor_auto_torrc_config.py      # Automated setup
├── tor_diagnostic_repair.py      # Diagnostic tool
├── tor_network_test.py           # Network tester
├── tor_route_traffic_setup.py    # Transparent proxy
├── tor_vpn_inclued.py            # Startup validation
├── setup_tor_custom.sh           # Bash setup script
├── tor_auto_proxy.sh             # Proxy GUI
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── CHANGELOG.md                 # Version history
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Tor 0.4.x or higher
- pip (Python package manager)

### Installation

#### Clone the Repository

```bash
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
cd tor_vpn
```

#### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Install Tor

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

### Running the Application

#### GUI Application

```bash
python tor_vpn_beta.py
```

#### Automated Setup

```bash
python tor_auto_torrc_config.py
```

#### Network Testing

```bash
python tor_network_test.py
```

#### Diagnostic Tool

```bash
python tor_diagnostic_repair.py
```

## Documentation

Comprehensive documentation is available in the [docs/](./) directory:

- **[INDEX.md](INDEX.md)** - Documentation navigation index
- **[README.md](README.md)** - Detailed system documentation
- **[INSTALL.md](INSTALL.md)** - Detailed installation guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guidelines
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development setup guide
- **[python-scripts.md](python-scripts.md)** - Python scripts documentation
- **[shell-scripts.md](shell-scripts.md)** - Shell scripts documentation
- **[configuration-files.md](configuration-files.md)** - Configuration files documentation
- **[architecture.md](architecture.md)** - Architecture and workflow documentation

## Features in Detail

### Country-specific Exit Nodes

Select from 200+ countries for your Tor exit node:
- Afghanistan (af)
- United States (us)
- Germany (de)
- United Kingdom (gb)
- And many more...

See the complete list in `tor_vpn_beta.py`.

### Transparent Proxy

Route all system traffic through Tor using iptables rules:
```bash
python tor_route_traffic_setup.py
```

⚠️ **Warning**: This routes ALL traffic through Tor. Use with caution.

### Network Testing

Test your Tor connection with detailed metrics:
```bash
python tor_network_test.py
```

Output includes:
- Connection status
- Latency measurement
- Exit IP address
- Circuit information

### Diagnostic Tools

Automated diagnostic and repair:
```bash
python tor_diagnostic_repair.py
```

Features:
- Init system detection
- Tor process management
- Configuration validation
- Diagnostic report generation

## Configuration

### Tor Configuration

The system uses custom Tor configuration files:
- Default: `~/.tor_config/torrc`
- Platform-specific paths available

### Key Parameters

- **ControlPort**: 9051 (Tor control interface)
- **SocksPort**: 9050 (SOCKS proxy)
- **TransPort**: 9040 (Transparent proxy)
- **DNSPort**: 5353 (DNS resolver)

### Authentication

Supports multiple authentication methods:
- Password-based (HashedControlPassword)
- Cookie-based (CookieAuthentication)
- Default authentication

## Security Considerations

⚠️ **Important Security Notes**:

- The system uses hardcoded passwords in some scripts (to be addressed in future versions)
- Configuration files should have restricted permissions (600/700)
- Some scripts require root/sudo privileges
- Tor should not be run as root
- Review [architecture.md](docs/architecture.md#security-architecture) for detailed security information

**Recommended Actions**:
- Change default passwords before production use
- Use environment variables for sensitive data
- Review and restrict file permissions
- Keep dependencies updated
- Monitor logs for suspicious activity

## Troubleshooting

### Common Issues

1. **Tor not starting**
   ```bash
   sudo systemctl status tor  # Linux
   # Check logs for errors
   ```

2. **Control port not accessible**
   ```bash
   netstat -tulnp | grep 9051
   # Check firewall settings
   ```

3. **Permission errors**
   ```bash
   # Run with sudo if required
   sudo python tor_diagnostic_repair.py
   ```

4. **Configuration errors**
   ```bash
   # Run diagnostic tool
   python tor_diagnostic_repair.py
   ```

### Getting Help

- Check [documentation](INDEX.md)
- Review [troubleshooting section](README.md#troubleshooting)
- Run diagnostic tools
- Check existing [issues](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/issues)
- Create a new issue with details

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed development setup.

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linters
flake8 .
black --check .
mypy .
```

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for complete development guide.

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

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided for educational and research purposes. Use of Tor and this software should comply with local laws and regulations. The authors are not responsible for misuse of this software.

## Acknowledgments

- [Tor Project](https://www.torproject.org/) - The Tor anonymity network
- [Stem Library](https://stem.torproject.org/) - Python Tor control library
- All contributors to this project

## Contact and Support

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **Issues**: [GitHub Issues](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/discussions)
- **Email**: [To be added - replace with contact email]

## Code of Conduct

Please read and follow our [Code of Conduct](docs/CODE_OF_CONDUCT.md).

---

<div align="center">

**Made with ❤️ by the Tor VPN System community**

[Star](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM) • [Fork](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/fork) • [Docs](docs/INDEX.md) • [Issues](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/issues)

</div>
