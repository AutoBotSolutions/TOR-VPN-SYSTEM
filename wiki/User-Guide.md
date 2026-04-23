# User Guide

This comprehensive guide covers how to use the Tor VPN System for managing Tor connections.

## Table of Contents

- [Getting Started](#getting-started)
- [Using the GUI Application](#using-the-gui-application)
- [Using Command-Line Tools](#using-command-line-tools)
- [Using Shell Scripts](#using-shell-scripts)
- [Country Selection](#country-selection)
- [Network Testing](#network-testing)
- [Diagnostics](#diagnostics)
- [Advanced Usage](#advanced-usage)

---

## Getting Started

### Prerequisites

Before using the system, ensure you have:
- Installed Tor (see [Installation Guide](Installation))
- Installed Python dependencies
- Tor service running
- Appropriate permissions (sudo/root for some operations)

### Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the GUI application
python tor_vpn_beta.py
```

---

## Using the GUI Application

### Launching the GUI

```bash
python tor_vpn_beta.py
```

The GUI requires:
- Python with tkinter installed
- Tor service running
- Appropriate permissions

### GUI Overview

The GUI consists of two main tabs:

#### Status Tab

**Connection Status Display**
- Shows current connection state (Connected/Not Connected)
- Color-coded indicators (green for connected, red for disconnected)

**Control Buttons**
- **Connect Button**: Initiates Tor connection with selected country
- **Disconnect Button**: Terminates Tor connection

#### Servers Tab

**Server List**
- Displays all available exit node countries
- Shows country name, code, and ID
- Scrollable list with 200+ countries

### Connecting to Tor

1. Click the "Connect" button
2. Enter a valid two-letter country code (e.g., "us", "de", "gb")
3. Click OK
4. Wait for connection confirmation
5. Status will change to "Connected" (green)

**Example Country Codes:**
- `us` - United States
- `de` - Germany
- `gb` - United Kingdom
- `jp` - Japan
- `fr` - France

### Disconnecting from Tor

1. Click the "Disconnect" button
2. Wait for disconnection confirmation
3. Status will change to "Not Connected" (red)

### GUI Features

- **Country Code Validation**: Only valid two-letter codes accepted
- **Error Messages**: Clear feedback for invalid inputs
- **Status Updates**: Real-time connection status
- **Server Browser**: Easy country selection from list

---

## Using Command-Line Tools

### tor_vpn_beta.py (GUI Mode)

```bash
python tor_vpn_beta.py
```

**Purpose**: Launch the graphical interface

**Requirements**: GUI environment (X11, Wayland, etc.)

### tor_custom_config.py

```bash
python tor_custom_config.py
```

**Purpose**: Generate custom Tor configuration with user-specified password

**Process**:
1. Prompts for password (hidden input)
2. Generates hashed password
3. Creates torrc file
4. Sets proper permissions (600)
5. Configures ownership

**Output**:
- Creates `~/.tor_config/torrc`
- Logs to `create_torrc.log`

### tor_auto_torrc_config.py

```bash
# Use defaults
python tor_auto_torrc_config.py

# Custom directories
python tor_auto_torrc_config.py /custom/data/dir /custom/log/dir /custom/torrc/path
```

**Purpose**: Automated Tor setup and configuration

**Features**:
- Checks Tor installation
- Installs Tor if missing
- Sets up directories
- Generates torrc
- Restarts Tor service

### tor_diagnostic_repair.py

```bash
# Basic usage
python tor_diagnostic_repair.py

# With custom paths
python tor_diagnostic_repair.py --tor-binary /usr/bin/tor --tor-config /etc/tor/torrc
```

**Purpose**: Diagnose and repair Tor configuration issues

**Features**:
- Init system detection
- Tor process management
- Configuration validation
- Diagnostic collection
- Automated repair

**Command-line Options**:
- `--tor-binary`: Path to Tor binary
- `--tor-config`: Path to torrc file
- `--custom-start-command`: Custom start command
- `--custom-stop-command`: Custom stop command

### tor_network_test.py

```bash
python tor_network_test.py
```

**Purpose**: Test Tor network connectivity and performance

**Output**:
- Connection status
- Latency measurement
- Exit IP address
- Circuit information
- Error list

**Test Results Structure**:
```python
{
    "connection": bool,
    "latency": float or None,
    "exit_ip": str or None,
    "errors": list
}
```

### tor_route_traffic_setup.py

```bash
sudo python tor_route_traffic_setup.py
```

**Purpose**: Configure transparent proxy for system-wide Tor routing

**Features**:
- iptables configuration
- DNS redirection through Tor
- System-wide traffic routing
- Service management

⚠️ **Warning**: This routes ALL system traffic through Tor. Use with caution.

### tor_vpn_inclued.py

```bash
python tor_vpn_inclued.py
```

**Purpose**: Validate Tor configuration and start Tor manually

**Features**:
- Configuration validation
- Automatic config generation
- Manual Tor startup
- Platform-specific paths

---

## Using Shell Scripts

### setup_tor_custom.sh

```bash
sudo bash setup_tor_custom.sh
```

**Purpose**: Bash script for custom Tor configuration setup

**Features**:
- Permission configuration
- Init script modification
- Boot enablement
- Service verification

**Process**:
1. Prompts for admin password
2. Stops existing Tor processes
3. Sets proper permissions
4. Modifies init script
5. Enables Tor at boot
6. Restarts Tor service
7. Verifies configuration

### tor_auto_proxy.sh

```bash
bash tor_auto_proxy.sh
```

**Purpose**: Zenity-based GUI for proxy management

**Requirements**:
- Zenity installed
- Tor service running

**Features**:
- System-wide proxy toggle
- Browser integration (Chrome, Firefox)
- Temporary Firefox profiles
- Logging

**Menu Options**:
- `enable_proxy` - Enable system-wide Tor proxy
- `disable_proxy` - Disable proxy
- `open_chrome` - Open Chrome with Tor
- `open_firefox` - Open Firefox with Tor
- `exit` - Exit script

---

## Country Selection

### Available Countries

The system supports exit nodes in 200+ countries. Some popular options:

| Country | Code | Country | Code |
|---------|------|---------|------|
| United States | us | Germany | de |
| United Kingdom | gb | France | fr |
| Japan | jp | Canada | ca |
| Australia | au | Netherlands | nl |
| Switzerland | ch | Sweden | se |
| Brazil | br | India | in |
| Singapore | sg | South Korea | kr |

### Complete Country List

See the `SERVERS` dictionary in `tor_vpn_beta.py` for the complete list of 200+ countries.

### Selecting Exit Nodes

#### Via GUI
1. Click "Connect" button
2. Enter country code
3. Confirm connection

#### Via Command Line
```python
from tor_vpn_beta import connect_to_tor
connect_to_tor("us")  # Connect to US exit node
```

#### Via Stem API
```python
from stem.control import Controller
from stem import Signal

with Controller.from_port(port=9051) as controller:
    controller.authenticate(password="your_password")
    controller.set_conf("ExitNodes", "{us}")
    controller.signal(Signal.NEWNYM)
```

### Changing Exit Nodes

To change exit nodes, simply disconnect and reconnect with a different country code, or send a NEWNYM signal:

```python
controller.signal(Signal.NEWNYM)
```

---

## Network Testing

### Running Network Tests

```bash
python tor_network_test.py
```

### Test Components

1. **Tor Service Check**
   - Verifies Tor is running
   - Checks process status

2. **Control Port Detection**
   - Detects control port from torrc
   - Validates port accessibility

3. **Authentication Test**
   - Tries password authentication
   - Falls back to cookie authentication
   - Tests default authentication

4. **Connection Test**
   - Sends NEWNYM signal
   - Measures latency
   - Detects exit IP
   - Gets circuit information

### Interpreting Results

**Successful Test:**
```
INFO - Tor service is running.
INFO - Control Port 9051 is accessible.
INFO - Tor is successfully routing traffic.
INFO - Exit IP detected: 185.xxx.xxx.xxx
```

**Failed Test:**
```
ERROR - Tor service is not running.
ERROR - Control Port 9051 is not accessible.
```

### Manual Testing

```bash
# Test with curl
curl --socks5 127.0.0.1:9050 https://check.torproject.org

# Test with telnet
telnet 127.0.0.1 9051
```

---

## Diagnostics

### Running Diagnostics

```bash
python tor_diagnostic_repair.py
```

### Diagnostic Process

1. **Configuration Validation**
   - Checks Tor binary exists
   - Validates torrc file
   - Verifies configuration syntax

2. **Password Collection**
   - Prompts for sudo password
   - Validates password (3 attempts)
   - Secure password handling

3. **Init System Detection**
   - Detects systemd
   - Detects init.d
   - Falls back to manual

4. **Service Restart**
   - Uses detected init system
   - Restarts Tor service
   - Validates restart success

5. **Diagnostic Collection**
   - Copies torrc file
   - Collects logs
   - Saves system info

### Diagnostic Output

Diagnostics are saved to `diagnostics/` directory:
- `torrc` - Tor configuration snapshot
- `logfile.log` - Collected logs
- `system_info.txt` - System information

### Manual Diagnostics

```bash
# Check Tor version
tor --version

# Check Tor configuration
tor --verify-config

# Check Tor process
ps aux | grep tor

# Check Tor ports
netstat -tulnp | grep tor

# Check Tor logs
tail -f /var/log/tor/log
```

---

## Advanced Usage

### Custom Configuration

#### Custom torrc Location

```python
import os
custom_torrc = "/path/to/custom/torrc"
os.environ["TOR_CONFIG"] = custom_torrc
```

#### Custom Exit Node Selection

```python
# Multiple countries
controller.set_conf("ExitNodes", "{us},{de},{gb}")

# Exclude countries
controller.set_conf("ExcludeNodes", "{cn},{ru}")

# Strict node selection
controller.set_conf("StrictNodes", "1")
```

### Circuit Management

#### Get Current Circuits

```python
circuits = controller.get_circuits()
for circuit in circuits:
    print(f"Circuit {circuit.id}: {circuit.purpose}")
    print(f"Build flags: {circuit.build_flags}")
```

#### Build New Circuit

```python
controller.signal(Signal.NEWNYM)
```

#### Close Circuit

```python
controller.close_circuit(circuit_id)
```

### Stream Management

#### Attach Stream to Circuit

```python
controller.set_conf("__LeaveStreamsUnattached", "1")
# Then attach stream manually
controller.attach_stream(stream_id, circuit_id)
```

### Event Monitoring

```python
def circuit_event(event):
    print(f"Circuit event: {event}")

controller.add_event_listener('CIRC', circuit_event)
```

### Browser Integration

#### Firefox Configuration

1. Open Firefox Settings > Network Settings
2. Manual proxy configuration
3. SOCKS Host: 127.0.0.1
4. Port: 9050
5. SOCKS v5
6. Proxy DNS when using SOCKS v5

#### Chrome Configuration

```bash
google-chrome --proxy-server="socks5://127.0.0.1:9050"
```

#### Configuration with Extension

Install proxy switcher extension:
- Proxy type: SOCKS5
- Host: 127.0.0.1
- Port: 9050
- DNS: Proxy DNS

### Transparent Proxy

#### Enable Transparent Proxy (Linux)

```bash
sudo python tor_route_traffic_setup.py
```

This configures iptables to route all traffic through Tor.

#### Verify Transparent Proxy

```bash
curl https://check.torproject.org
```

Should show Tor is being used.

#### Disable Transparent Proxy

```bash
# Flush iptables rules
sudo iptables -F
sudo iptables -t nat -F

# Restore default rules
sudo iptables-restore < /etc/iptables/rules.v4.backup
```

### Multiple Tor Instances

#### Run Multiple Instances

```bash
# First instance
tor -f ~/.tor/torrc1

# Second instance (different ports)
tor -f ~/.tor/torrc2
```

#### Configure Different Ports

In torrc:
```
ControlPort 9051
SocksPort 9050
```

### Automation

#### Scripted Connection

```python
#!/usr/bin/env python3
from tor_vpn_beta import connect_to_tor, disconnect_tor

# Connect to US
connect_to_tor("us")

# Do work...

# Disconnect
disconnect_tor()
```

#### Scheduled Connection Changes

```bash
# Cron job to change exit node hourly
0 * * * * /path/to/change_exit_node.sh
```

### Performance Optimization

#### Select Fast Exit Nodes

```python
# Use countries with typically faster connections
connect_to_tor("nl")  # Netherlands
connect_to_tor("de")  # Germany
connect_to_tor("se")  # Sweden
```

#### Reduce Circuit Build Time

```python
# Use stable guard nodes
controller.set_conf("EntryNodes", "{us}")
controller.set_conf("GuardLifetime", "30 days")
```

---

## Tips and Best Practices

### General Tips

1. **Use Stable Exit Nodes**: Countries with good infrastructure provide better performance
2. **Monitor Connection**: Regularly test connection with `tor_network_test.py`
3. **Check Logs**: Review logs for issues
4. **Keep Updated**: Regularly update Tor and dependencies
5. **Use Strong Passwords**: Generate secure passwords for Tor control

### Security Best Practices

1. **Change Default Passwords**: Don't use hardcoded passwords
2. **Restrict Permissions**: Ensure torrc has 600 permissions
3. **Monitor Logs**: Check for suspicious activity
4. **Use HTTPS**: Always use HTTPS when possible
5. **Don't Log Sensitive Data**: Avoid logging passwords or personal data

### Performance Tips

1. **Select Nearby Exit Nodes**: Reduces latency
2. **Avoid Congested Nodes**: Some exit nodes may be overloaded
3. **Use Circuit Persistence**: Don't change circuits too frequently
4. **Monitor Resource Usage**: Check memory and CPU usage

---

## Common Use Cases

### Web Browsing

1. Start Tor service
2. Run `tor_vpn_beta.py`
3. Connect to desired country
4. Configure browser to use SOCKS5 proxy (127.0.0.1:9050)
5. Browse anonymously

### Command Line Tools

```bash
# Use with curl
curl --socks5 127.0.0.1:9050 https://example.com

# Use with wget
wget --proxy=on --proxy-type=socks5 --proxy=127.0.0.1:9050 https://example.com

# Use with git
git config --global http.proxy socks5://127.0.0.1:9050
```

### Programming

```python
import requests

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

response = requests.get('https://example.com', proxies=proxies)
```

---

## Troubleshooting

For common issues and solutions, see the [Troubleshooting](Troubleshooting) page.

---

## Additional Resources

- [Home](Home) - Wiki home page
- [Installation](Installation) - Installation guide
- [Configuration](Configuration) - Configuration options
- [Troubleshooting](Troubleshooting) - Common issues
- [API Reference](API-Reference) - Python API documentation

---

**Last Updated**: 2024-04-23
