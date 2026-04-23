# Frequently Asked Questions

Common questions and answers about the Tor VPN System.

## Table of Contents

- [General Questions](#general-questions)
- [Installation Questions](#installation-questions)
- [Configuration Questions](#configuration-questions)
- [Usage Questions](#usage-questions)
- [Security Questions](#security-questions)
- [Troubleshooting Questions](#troubleshooting-questions)
- [Development Questions](#development-questions)

---

## General Questions

### What is the Tor VPN System?

The Tor VPN System is a comprehensive management tool for the Tor network that provides both graphical (GUI) and command-line (CLI) interfaces for configuring, managing, and routing traffic through Tor. It supports country-specific exit node selection, transparent proxy configuration, and includes diagnostic tools.

### What are the system requirements?

- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+), macOS 10.15+, Windows 10+
- **Python**: 3.10 or higher
- **RAM**: 2 GB minimum, 4 GB recommended
- **Disk Space**: 500 MB for installation, 1 GB for logs and data
- **Network**: Stable internet connection

See [Installation](Installation) for detailed requirements.

### Is this system free to use?

Yes, the Tor VPN System is released under the MIT License and is free to use, modify, and distribute. See the [LICENSE](../LICENSE) file for details.

### Is Tor VPN System affiliated with the Tor Project?

No, this is an independent project that uses the Tor network. It is not officially affiliated with the Tor Project, though it uses Tor's official software and follows Tor's guidelines.

### Can I use this for illegal activities?

No. This software is provided for legitimate purposes such as privacy protection, circumventing censorship, and security research. Misuse of this software for illegal activities is strictly prohibited and may violate local laws.

---

## Installation Questions

### How do I install the Tor VPN System?

See the detailed [Installation Guide](Installation) for step-by-step instructions for Linux, macOS, and Windows.

### Do I need to install Tor separately?

Yes, Tor must be installed separately. The installation guide provides instructions for installing Tor on each platform.

### Can I use a virtual environment?

Yes, using a virtual environment is recommended:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows
```

### What Python version do I need?

Python 3.10 or higher is required. Python 3.11+ is recommended for better performance and security.

### Can I install this on multiple systems?

Yes, you can install and use the system on multiple systems. Each installation will have its own configuration.

---

## Configuration Questions

### Where are configuration files stored?

Default locations:
- **Linux**: `~/.tor_config/torrc` or `~/.tor/torrc`
- **macOS**: `~/Library/Application Support/Tor/torrc`
- **Windows**: `%APPDATA%\tor\torrc`

See [Configuration](Configuration) for more details.

### How do I change the Tor control password?

Run the configuration script:

```bash
python tor_custom_config.py
```

It will prompt for a new password and update the configuration.

### Can I use a custom torrc file?

Yes, you can specify a custom torrc path:

```bash
python tor_auto_torrc_config.py /custom/data/dir /custom/log/dir /custom/torrc/path
```

### How do I select a specific country for the exit node?

In the GUI, click "Connect" and enter the two-letter country code (e.g., "us", "de", "gb").

Via command line:
```python
from tor_vpn_beta import connect_to_tor
connect_to_tor("us")
```

### What countries are supported?

The system supports exit nodes in 200+ countries. See the `SERVERS` dictionary in `tor_vpn_beta.py` for the complete list.

### Can I use multiple exit nodes?

You can specify multiple countries in torrc:

```
ExitNodes {us},{de},{gb}
```

However, Tor will select one at random from the specified set.

---

## Usage Questions

### How do I start the GUI application?

```bash
python tor_vpn_beta.py
```

### Can I use this without the GUI?

Yes, all functionality is available via command-line tools:
- `tor_network_test.py` - Test connection
- `tor_diagnostic_repair.py` - Diagnostics
- `tor_custom_config.py` - Configuration
- `tor_auto_torrc_config.py` - Automated setup

### How do I route all system traffic through Tor?

Use the transparent proxy setup:

```bash
sudo python tor_route_traffic_setup.py
```

⚠️ **Warning**: This routes ALL traffic through Tor. Use with caution.

### How do I configure my browser to use Tor?

**Firefox:**
1. Open Settings > Network Settings
2. Manual proxy configuration
3. SOCKS Host: 127.0.0.1, Port: 9050
4. SOCKS v5
5. Check "Proxy DNS when using SOCKS v5"

**Chrome:**
```bash
google-chrome --proxy-server="socks5://127.0.0.1:9050"
```

### How do I test if Tor is working?

Run the network test:

```bash
python tor_network_test.py
```

Or use curl:
```bash
curl --socks5 127.0.0.1:9050 https://check.torproject.org
```

### Can I use this with applications other than browsers?

Yes, configure the application to use SOCKS5 proxy at 127.0.0.1:9050, or set environment variables:

```bash
export http_proxy="socks5h://127.0.0.1:9050"
export https_proxy="socks5h://127.0.0.1:9050"
```

### How do I change my exit node?

Disconnect and reconnect with a different country code, or use the Stem API:

```python
from stem.control import Controller
from stem import Signal

with Controller.from_port(port=9051) as controller:
    controller.authenticate(password="your_password")
    controller.set_conf("ExitNodes", "{de}")
    controller.signal(Signal.NEWNYM)
```

---

## Security Questions

### Is this system secure?

The system has security considerations that need to be addressed. See the [Security Guide](Security) for detailed information on current security issues and best practices.

### What are the main security concerns?

Current concerns include:
- Hardcoded passwords in some scripts
- Limited input validation
- Password handling in some scripts
- Logging of potentially sensitive information

See [Security Guide](Security) for details and mitigation strategies.

### How do I secure my installation?

1. Change default passwords
2. Set proper file permissions (600 for torrc)
3. Use environment variables for sensitive data
4. Restrict log file access
5. Keep dependencies updated
6. Configure firewall rules

See [Security Guide](Security) for comprehensive security recommendations.

### Should I run Tor as root?

No, Tor should not be run as root. The system includes warnings about this. Run Tor as a dedicated user (typically `debian-tor` on Linux).

### Are my passwords stored securely?

Currently, passwords are stored as hashes in torrc files. However, the system has hardcoded passwords in some scripts that should be removed before production use. See [Security Guide](Security) for details.

### Can I use this on a public network?

Yes, Tor is designed to provide privacy even on public networks. However, ensure your local system is secure and follow best practices.

---

## Troubleshooting Questions

### Tor won't start. What should I do?

1. Check if Tor is installed: `tor --version`
2. Check service status: `sudo systemctl status tor`
3. Check logs: `sudo journalctl -xe | grep -i tor`
4. Validate configuration: `tor --verify-config`
5. See [Troubleshooting](Troubleshooting) for more details.

### I get "Control port not accessible" error. How do I fix it?

1. Verify Tor is running: `ps aux | grep tor`
2. Check if port is listening: `netstat -tulnp | grep 9051`
3. Check firewall settings
4. Verify torrc has ControlPort set
5. See [Troubleshooting](Troubleshooting) for more details.

### Authentication is failing. What should I check?

1. Verify password hash in torrc
2. Try regenerating password: `python tor_custom_config.py`
3. Check authentication method (password vs cookie)
4. Verify cookie file exists and has correct permissions
5. See [Troubleshooting](Troubleshooting) for more details.

### The GUI won't open. What should I do?

1. Install tkinter: `sudo apt install python3-tk`
2. Check display environment: `echo $DISPLAY`
3. Try running with explicit display: `export DISPLAY=:0`
4. See [Troubleshooting](Troubleshooting) for more details.

### Connection is very slow. How can I improve it?

1. Try different exit nodes (geographically closer)
2. Check your internet connection
3. Monitor exit node performance
4. Reduce circuit rebuild frequency
5. See [Performance Considerations](../docs/architecture.md#performance-considerations) for more tips.

### I'm getting permission errors. What should I do?

1. Run with sudo if required: `sudo python <script>`
2. Check file permissions: `ls -la ~/.tor_config/torrc`
3. Fix permissions: `chmod 600 ~/.tor_config/torrc`
4. Fix ownership: `chown $USER:$USER ~/.tor_config/torrc`
5. See [Troubleshooting](Troubleshooting) for more details.

---

## Development Questions

### How can I contribute to the project?

See the [Contributing Guidelines](../docs/CONTRIBUTING.md) for detailed information on contributing.

### What is the development workflow?

See the [Developer Guide](Developer-Guide) for development setup and workflow information.

### How do I set up a development environment?

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Install dev dependencies: `pip install -r requirements-dev.txt`
5. See [Developer Guide](Developer-Guide) for details.

### How do I run tests?

```bash
pytest
```

See [Developer Guide](Developer-Guide) for more information on testing.

### What coding standards should I follow?

Follow PEP 8 guidelines. Use the provided linters:

```bash
flake8 .
black --check .
mypy .
```

See [Developer Guide](Developer-Guide) for more details.

### How do I report a bug?

Create an issue on GitHub with:
- System information
- Error messages
- Steps to reproduce
- Expected vs actual behavior

See [Troubleshooting](Troubleshooting) for more details on reporting issues.

---

## Platform-Specific Questions

### Does this work on Windows?

Yes, but some features may be limited. The shell scripts are Linux/macOS specific. Use WSL for full functionality.

### Does this work on macOS?

Yes, but some shell scripts may require Homebrew for dependencies. See [Installation](Installation) for macOS-specific instructions.

### Which Linux distributions are supported?

Ubuntu, Debian, Fedora, Arch Linux, and other systemd-based distributions are supported. See [Installation](Installation) for distribution-specific instructions.

### Can I use this on a Raspberry Pi?

Yes, the system can run on Raspberry Pi with appropriate OS (Raspberry Pi OS). Ensure sufficient RAM and use lightweight configurations.

### Does this work with ARM architecture?

Yes, the Python scripts are architecture-independent. Tor is available for ARM on most Linux distributions.

---

## Legal and Ethical Questions

### Is using Tor legal?

Yes, using Tor is legal in most countries. However, some countries restrict or ban Tor. Check your local laws before using Tor.

### Can my ISP see that I'm using Tor?

Your ISP can see that you're connecting to Tor relays, but cannot see what you're doing through Tor.

### Can websites tell I'm using Tor?

Websites can see that you're using Tor based on your exit IP address, which is listed as a Tor exit node. Some websites may block Tor connections.

### Is this suitable for corporate use?

Additional security measures should be implemented for corporate use, including:
- Proper security auditing
- Compliance with corporate policies
- Integration with corporate security tools
- Custom security configurations

---

## Additional Questions

### Where can I find more documentation?

See the [Wiki Home](Home) for a complete list of documentation.

### How do I get help?

- Check the [Troubleshooting](Troubleshooting) page
- Review the [Documentation Index](../docs/INDEX.md)
- Search existing [GitHub Issues](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/issues)
- Create a new issue with details

### Is there a community forum?

Currently, use GitHub Issues and Discussions for community support. A dedicated forum may be added in the future.

### How often is the project updated?

See the [CHANGELOG](../CHANGELOG.md) for version history and planned updates.

### Can I request a feature?

Yes, feature requests can be submitted via GitHub Issues. Use the "enhancement" label.

### How do I stay updated on changes?

- Watch the GitHub repository
- Subscribe to releases
- Follow the [CHANGELOG](../CHANGELOG.md)

---

## Still Have Questions?

If your question isn't answered here:

1. Check the [Wiki Home](Home) for more documentation
2. Review [Troubleshooting](Troubleshooting) for common issues
3. Search existing [GitHub Issues](https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM/issues)
4. Create a new issue with your question

---

**Last Updated**: 2024-04-23
