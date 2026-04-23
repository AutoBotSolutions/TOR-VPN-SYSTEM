# Installation Guide

This guide provides step-by-step installation instructions for the Tor VPN System on various platforms.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation on Linux](#installation-on-linux)
- [Installation on macOS](#installation-on-macos)
- [Installation on Windows](#installation-on-windows)
- [Post-Installation Setup](#post-installation-setup)
- [Verification](#verification)
- [Uninstallation](#uninstallation)

---

## System Requirements

### Minimum Requirements

- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+, etc.), macOS 10.15+, Windows 10+
- **Python**: 3.10 or higher
- **RAM**: 2 GB minimum, 4 GB recommended
- **Disk Space**: 500 MB for installation, 1 GB for logs and data
- **Network**: Stable internet connection

### Recommended Requirements

- **Operating System**: Linux (Ubuntu 22.04+), macOS 12+, Windows 11
- **Python**: 3.11 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 2 GB for installation and data
- **Network**: High-speed internet connection

---

## Installation on Linux

### Ubuntu/Debian

#### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install System Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv tor iptables-persistent zenity
```

#### Step 3: Clone Repository
```bash
cd ~
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
cd tor_vpn
```

#### Step 4: Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Step 5: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Configure Tor
```bash
# Automated configuration
python tor_auto_torrc_config.py

# Or manual configuration
python tor_custom_config.py
```

#### Step 7: Start Tor Service
```bash
sudo systemctl start tor
sudo systemctl enable tor
```

### Fedora/RHEL

#### Step 1: Update System
```bash
sudo dnf update -y
```

#### Step 2: Install System Dependencies
```bash
sudo dnf install -y python3 python3-pip tor iptables zenity
```

#### Step 3: Clone Repository
```bash
cd ~
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
cd tor_vpn
```

#### Step 4: Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Step 5: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Configure Tor
```bash
python tor_auto_torrc_config.py
```

#### Step 7: Start Tor Service
```bash
sudo systemctl start tor
sudo systemctl enable tor
```

### Arch Linux

#### Step 1: Update System
```bash
sudo pacman -Syu
```

#### Step 2: Install System Dependencies
```bash
sudo pacman -S python python-pip tor iptables zenity
```

#### Step 3: Clone Repository
```bash
cd ~
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
cd tor_vpn
```

#### Step 4: Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
```

#### Step 5: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Configure Tor
```bash
python tor_auto_torrc_config.py
```

#### Step 7: Start Tor Service
```bash
sudo systemctl start tor
sudo systemctl enable tor
```

---

## Installation on macOS

### Using Homebrew (Recommended)

#### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install System Dependencies
```bash
brew install python@3.11 tor
brew install --cask zenity
```

#### Step 3: Clone Repository
```bash
cd ~/Documents
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
cd tor_vpn
```

#### Step 4: Create Virtual Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

#### Step 5: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Configure Tor
```bash
python tor_auto_torrc_config.py
```

#### Step 7: Start Tor
```bash
# Tor on macOS is typically started manually
tor -f ~/.tor/torrc
```

---

## Installation on Windows

### Using Python Installer

#### Step 1: Install Python
1. Download Python 3.11+ from https://www.python.org/downloads/
2. Run installer and check "Add Python to PATH"
3. Verify installation:
```cmd
python --version
pip --version
```

#### Step 2: Install Tor
1. Download Tor Expert Bundle from https://www.torproject.org/download/tor/
2. Extract to `C:\Tor`
3. Add `C:\Tor` to system PATH

#### Step 3: Clone Repository
```cmd
cd C:\Users\YourUser\Documents
git clone https://github.com/AutoBotSolutions/TOR-VPN-SYSTEM.git
cd tor_vpn
```

#### Step 4: Create Virtual Environment
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### Step 5: Install Python Dependencies
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Configure Tor
```cmd
python tor_auto_torrc_config.py
```

#### Step 7: Start Tor
```cmd
tor -f %APPDATA%\tor\torrc
```

### Using WSL (Windows Subsystem for Linux)

This provides a Linux environment on Windows, recommended for full functionality.

#### Step 1: Enable WSL
```powershell
wsl --install
```

#### Step 2: Install Ubuntu from Microsoft Store

#### Step 3: Follow Linux Installation Instructions
After WSL is set up, follow the Ubuntu/Debian installation instructions above.

---

## Post-Installation Setup

### Setting Environment Variables

#### Linux/macOS
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export TOR_PASSWORD="your_secure_password"
export TOR_CONFIG_DIR="/home/your-user/.tor_config"
```

#### Windows
Add to System Environment Variables:
```
TOR_PASSWORD=your_secure_password
TOR_CONFIG_DIR=C:\Users\YourUser\.tor_config
```

### Configuring Firewall

#### Linux (ufw)
```bash
# Allow Tor ports
sudo ufw allow 9050/tcp  # SOCKS port
sudo ufw allow 9051/tcp  # Control port
sudo ufw allow 9040/tcp  # Transparent proxy
sudo ufw allow 5353/udp  # DNS port
```

#### Linux (iptables)
```bash
# Allow Tor ports
sudo iptables -A INPUT -p tcp --dport 9050 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9051 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9040 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 5353 -j ACCEPT
```

#### macOS
```bash
# System Preferences > Security & Privacy > Firewall > Firewall Options
# Add Tor application and allow incoming connections
```

#### Windows
```
# Windows Firewall > Advanced Settings > Inbound Rules
# Add rules for ports 9050, 9051, 9040, 5353
```

### Setting Up Transparent Proxy (Linux Only)

If you want to route all system traffic through Tor:

```bash
sudo python tor_route_traffic_setup.py
```

⚠️ **Warning**: This routes ALL traffic through Tor. Use with caution.

### Configuring Browser Integration

#### Firefox
1. Open Firefox Settings > Network Settings
2. Select "Manual proxy configuration"
3. Set:
   - SOCKS Host: 127.0.0.1
   - Port: 9050
   - SOCKS v5
   - Check "Proxy DNS when using SOCKS v5"

#### Chrome
```bash
google-chrome --proxy-server="socks5://127.0.0.1:9050"
```

#### Chrome/Chromium with Extension
Install proxy switcher extension and configure:
- Proxy type: SOCKS5
- Host: 127.0.0.1
- Port: 9050
- DNS: Proxy DNS

---

## Verification

### Verify Tor Installation

```bash
tor --version
```

Expected output:
```
Tor version 0.4.x.x
```

### Verify Tor Service

```bash
# Linux
sudo systemctl status tor

# macOS
ps aux | grep tor

# Windows
tasklist | findstr tor
```

### Verify Python Dependencies

```bash
pip list
```

Check that these are installed:
- stem~=1.8.2
- psutil~=7.0.0

### Test Tor Connection

```bash
python tor_network_test.py
```

Expected output:
```
INFO - Tor service is running.
INFO - Control Port 9051 is accessible.
INFO - Tor is successfully routing traffic.
INFO - Exit IP detected: [IP address]
```

### Test GUI Application

```bash
python tor_vpn_beta.py
```

The GUI should open and display:
- Connection status
- Server list
- Connect/Disconnect buttons

### Test with curl

```bash
curl --socks5 127.0.0.1:9050 https://check.torproject.org
```

Should show "Congratulations. This browser is configured to use Tor."

---

## Uninstallation

### Linux

```bash
# Stop Tor service
sudo systemctl stop tor
sudo systemctl disable tor

# Remove Tor
sudo apt remove tor  # Ubuntu/Debian

# Remove project directory
rm -rf ~/tor_vpn

# Remove configuration (optional)
rm -rf ~/.tor_config
rm -rf /var/lib/tor
```

### macOS

```bash
# Stop Tor
pkill tor

# Remove Tor
brew uninstall tor

# Remove project directory
rm -rf ~/Documents/tor_vpn

# Remove configuration (optional)
rm -rf ~/.tor
rm -rf ~/Library/Application\ Support/Tor
```

### Windows

```cmd
# Stop Tor
taskkill /F /IM tor.exe

# Remove Tor installation
# Delete C:\Tor directory

# Remove project directory
rmdir /S C:\Users\YourUser\Documents\tor_vpn

# Remove configuration (optional)
rmdir /S %APPDATA%\tor
```

---

## Troubleshooting Installation

### Python Not Found

**Linux/macOS:**
```bash
# Install Python
sudo apt install python3  # Ubuntu/Debian
brew install python@3.11  # macOS
```

**Windows:**
- Ensure Python was installed with "Add to PATH" checked
- Restart command prompt after installation

### Tor Installation Fails

**Linux:**
```bash
# Add Tor repository (Ubuntu/Debian)
sudo apt install apt-transport-https
wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DD89F.asc | sudo apt-key add -
echo "deb https://deb.torproject.org/torproject.org $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/tor.list
sudo apt update
sudo apt install tor
```

**macOS:**
```bash
brew update
brew install tor
```

### Permission Denied Errors

```bash
# Run with sudo
sudo python tor_auto_torrc_config.py

# Or fix permissions
sudo chown -R $USER:$USER ~/.tor_config
chmod 700 ~/.tor_config
chmod 600 ~/.tor_config/torrc
```

### Virtual Environment Issues

```bash
# Deactivate and recreate
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Next Steps

After installation:

1. Read the [User Guide](User-Guide) for usage instructions
2. Review [Configuration](Configuration) for setup options
3. Check [Troubleshooting](Troubleshooting) for common issues
4. Configure your preferred exit nodes
5. Test the connection with tor_network_test.py

---

## Additional Resources

- [Home](Home) - Wiki home page
- [User Guide](User-Guide) - Comprehensive user guide
- [Configuration](Configuration) - Configuration options
- [Troubleshooting](Troubleshooting) - Common issues
- [Developer Guide](Developer-Guide) - Development setup

---

**Last Updated**: 2024-04-23
