# API Reference

This document provides API reference documentation for the Tor VPN System Python modules.

## Table of Contents

- [tor_vpn_beta.py](#tor_vpn_beta.py)
- [tor_custom_config.py](#tor_custom_config.py)
- [tor_auto_torrc_config.py](#tor_auto_torrc_config.py)
- [tor_diagnostic_repair.py](#tor_diagnostic_repair.py)
- [tor_network_test.py](#tor_network_test.py)
- [tor_route_traffic_setup.py](#tor_route_traffic_setup.py)
- [tor_vpn_inclued.py](#tor_vpn_inclued.py)

---

## tor_vpn_beta.py

### Overview

Main GUI application with country-specific exit node selection using Tkinter.

### Functions

#### `setup_logging(log_file=LOG_FILE)`

Setup logging with rotating file handlers.

**Parameters:**
- `log_file` (str): Path to log file (default: "vpn_app_advanced.log")

**Returns:**
- `logger`: Configured logger instance

**Example:**
```python
logger = setup_logging("custom.log")
```

#### `setup_signal_handlers()`

Setup signal handlers for clean termination (SIGTERM, SIGINT).

**Example:**
```python
setup_signal_handlers()
```

#### `ensure_admin_privileges()`

Ensure the script is running with administrator privileges.

**Raises:**
- `SystemExit`: If not running with appropriate privileges

**Example:**
```python
ensure_admin_privileges()
```

#### `connect_to_tor(country_code)`

Connect to Tor using the specified country code for the exit node.

**Parameters:**
- `country_code` (str): Two-letter country code (e.g., "us", "de")

**Raises:**
- `ValueError`: If invalid country code provided
- `Exception`: For connection failures

**Example:**
```python
from tor_vpn_beta import connect_to_tor
connect_to_tor("us")
```

#### `disconnect_tor()`

Disconnect from Tor by resetting exit node configurations.

**Raises:**
- `Exception`: For disconnection failures

**Example:**
```python
from tor_vpn_beta import disconnect_tor
disconnect_tor()
```

### Classes

#### `VPNInterface`

Main GUI class for the Tor VPN client.

**Methods:**

- `__init__(master)`: Initialize the GUI window
- `create_widgets()`: Build all GUI components
- `create_status_tab()`: Create connection status tab
- `create_servers_tab()`: Create server list tab
- `connect()`: Connect to Tor with user-specified country
- `disconnect()`: Disconnect from Tor

**Example:**
```python
import tkinter as tk
from tor_vpn_beta import VPNInterface

root = tk.Tk()
app = VPNInterface(root)
root.mainloop()
```

### Constants

```python
TOR_PASSWORD_ENV = "TOR_PASSWORD"
TOR_DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".tor_config")
TOR_CONFIG_FILE = os.path.join(TOR_DEFAULT_DIR, "torrc")
DEFAULT_PASSWORD = "467rSeG7%tGd757575EwPLsaQ$BplwEQJ7676RLsa$3@4161"
PRECOMPUTED_HASHED_PASSWORD = "16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD"
LOG_FILE = "vpn_app_advanced.log"
```

---

## tor_custom_config.py

### Overview

Custom Tor configuration generator with user-specified password and ownership management.

### Functions

#### `generate_hashed_password(password)`

Generate the hashed control password for Tor.

**Parameters:**
- `password` (str): Plain-text password

**Returns:**
- `str`: Hashed password string

**Raises:**
- `subprocess.CalledProcessError`: If hashing fails

**Example:**
```python
from tor_custom_config import generate_hashed_password
hashed = generate_hashed_password("my_password")
```

#### `change_ownership(file_path, user_name, group_name)`

Changes the ownership of a file to the specified user and group.

**Parameters:**
- `file_path` (str): Path to the file
- `user_name` (str): Username for ownership
- `group_name` (str): Group name for ownership

**Raises:**
- `KeyError`: If user or group doesn't exist
- `PermissionError`: If insufficient permissions

**Example:**
```python
from tor_custom_config import change_ownership
change_ownership("/path/to/file", "user", "group")
```

#### `create_directory(directory)`

Creates the specified directory with proper permissions (700).

**Parameters:**
- `directory` (str): Directory path to create

**Example:**
```python
from tor_custom_config import create_directory
create_directory("/home/user/.tor_config")
```

#### `create_torrc_file()`

Creates the torrc file with:
- User-provided password
- Hashed password generation
- Proper file permissions (600)
- Ownership assignment

**Example:**
```python
from tor_custom_config import create_torrc_file
create_torrc_file()
```

#### `verify_file_access(file_path)`

Verifies file permissions and accessibility.

**Parameters:**
- `file_path` (str): Path to file to verify

**Example:**
```python
from tor_custom_config import verify_file_access
verify_file_access("/home/user/.tor_config/torrc")
```

### Constants

```python
torrc_directory = os.path.join(os.path.expanduser("~"), ".tor_config")
torrc_path = os.path.join(torrc_directory, "torrc")
control_port = 9051
```

---

## tor_auto_torrc_config.py

### Overview

Automated Tor setup and configuration script with cross-platform support.

### Functions

#### `check_if_tor_installed()`

Checks if Tor is already installed.

**Returns:**
- `bool`: True if installed, False otherwise

**Example:**
```python
from tor_auto_torrc_config import check_if_tor_installed
if not check_if_tor_installed():
    install_tor()
```

#### `install_tor()`

Installs Tor depending on the operating system.

**Example:**
```python
from tor_auto_torrc_config import install_tor
install_tor()
```

#### `generate_hashed_password(password)`

Generates hashed control password for Tor.

**Parameters:**
- `password` (str): Plain-text password

**Returns:**
- `str`: Hashed password

**Example:**
```python
from tor_auto_torrc_config import generate_hashed_password
hashed = generate_hashed_password("password")
```

#### `setup_directories(data_dir, log_dir)`

Creates necessary directories for Tor data and logs.

**Parameters:**
- `data_dir` (str): Data directory path
- `log_dir` (str): Log directory path

**Example:**
```python
from tor_auto_torrc_config import setup_directories
setup_directories("/var/lib/tor", "/var/log/tor")
```

#### `apply_torrc(data_dir, log_dir, custom_torrc_path=None)`

Generates and applies the custom torrc configuration file.

**Parameters:**
- `data_dir` (str): Data directory path
- `log_dir` (str): Log directory path
- `custom_torrc_path` (str, optional): Custom torrc path

**Example:**
```python
from tor_auto_torrc_config import apply_torrc
apply_torrc("/var/lib/tor", "/var/log/tor")
```

#### `restart_tor()`

Handles Tor service restart securely with password prompt.

**Example:**
```python
from tor_auto_torrc_config import restart_tor
restart_tor()
```

### Constants

```python
DEFAULT_DATA_DIR = "/var/lib/tor"
DEFAULT_LOG_DIR = "/var/log/tor"
DEFAULT_USER_TORRC_PATH = os.path.expanduser("~/.tor/torrc")
DEFAULT_CONTROL_PASSWORD = "TorSecurePassword123!"
```

---

## tor_diagnostic_repair.py

### Overview

Comprehensive Tor diagnostic and repair tool with init system detection.

### Functions

#### `parse_arguments()`

Parses command-line arguments for custom paths and commands.

**Returns:**
- `argparse.Namespace`: Parsed arguments

**Command-line Arguments:**
- `--tor-binary`: Path to Tor binary (default: 'tor')
- `--tor-config`: Path to Tor config (default: '/etc/tor/torrc')
- `--custom-start-command`: Custom command to start Tor
- `--custom-stop-command`: Custom command to stop Tor

**Example:**
```bash
python tor_diagnostic_repair.py --tor-binary /usr/bin/tor --tor-config /etc/tor/torrc
```

#### `detect_init_system()`

Detects the initialization system used by the host system.

**Returns:**
- `str`: 'systemd', 'sysvinit', or 'manual'

**Example:**
```python
from tor_diagnostic_repair import detect_init_system
init_system = detect_init_system()
```

#### `validate_tor_configuration()`

Validates the provided Tor binary and checks the configuration file.

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
from tor_diagnostic_repair import validate_tor_configuration
if validate_tor_configuration():
    print("Configuration is valid")
```

#### `find_tor_process()`

Locates the Tor process by checking active processes.

**Returns:**
- `int` or `None`: PID of Tor process if found

**Example:**
```python
from tor_diagnostic_repair import find_tor_process
pid = find_tor_process()
if pid:
    print(f"Tor running with PID: {pid}")
```

#### `restart_tor_service(init_system, sudo_password)`

Restarts the Tor service using the detected init system.

**Parameters:**
- `init_system` (str): Detected init system
- `sudo_password` (str): Sudo password

**Returns:**
- `bool`: Success status

**Example:**
```python
from tor_diagnostic_repair import restart_tor_service
restart_tor_service("systemd", "password")
```

#### `collect_diagnostics(output_dir="diagnostics")`

Collects diagnostic logs and custom configuration files.

**Parameters:**
- `output_dir` (str): Directory for diagnostic output

**Example:**
```python
from tor_diagnostic_repair import collect_diagnostics
collect_diagnostics("my_diagnostics")
```

---

## tor_network_test.py

### Overview

Tor network connectivity and performance testing tool.

### Functions

#### `is_tor_running()`

Checks if the Tor service is running.

**Returns:**
- `bool`: True if running, False otherwise

**Example:**
```python
from tor_network_test import is_tor_running
if is_tor_running():
    print("Tor is running")
```

#### `check_port_status(host, port)`

Checks if the specified port is open and listening.

**Parameters:**
- `host` (str): Host address
- `port` (int): Port number

**Returns:**
- `bool`: True if open, False otherwise

**Example:**
```python
from tor_network_test import check_port_status
if check_port_status("127.0.0.1", 9051):
    print("Control port is accessible")
```

#### `detect_tor_control_port()`

Detects the Tor control port from the torrc file.

**Returns:**
- `int`: Control port number (default: 9051)

**Example:**
```python
from tor_network_test import detect_tor_control_port
port = detect_tor_control_port()
```

#### `detect_tor_password()`

Tries to auto-detect the Tor Control Port password from torrc files.

**Returns:**
- `str` or `None`: Detected password (or None if hashed)

**Example:**
```python
from tor_network_test import detect_tor_password
password = detect_tor_password()
```

#### `detect_auth_cookie()`

Tries to auto-detect the Tor Control Port authentication cookie.

**Returns:**
- `str` or `None`: Path to auth cookie if found

**Example:**
```python
from tor_network_test import detect_auth_cookie
cookie_path = detect_auth_cookie()
```

#### `test_tor_connection()`

Main function to test Tor network connectivity.

**Returns:**
- `dict`: Test results containing:
  - `connection` (bool): Connection status
  - `latency` (float): Latency in seconds
  - `exit_ip` (str): Exit IP address
  - `errors` (list): List of error messages

**Example:**
```python
from tor_network_test import test_tor_connection
results = test_tor_connection()
print(f"Connection: {results['connection']}")
print(f"Latency: {results['latency']}s")
print(f"Exit IP: {results['exit_ip']}")
```

### Constants

```python
TORRC_PATHS = [
    "/etc/tor/torrc",
    "/usr/local/etc/tor/torrc",
    os.path.expanduser("~/.torrc")
]
AUTH_COOKIE_PATHS = [
    "/run/tor/control.authcookie",
    "/var/lib/tor/control_auth_cookie"
]
```

---

## tor_route_traffic_setup.py

### Overview

Transparent proxy setup script for routing all system traffic through Tor.

### Functions

#### `is_root()`

Checks if the script is being run as root.

**Returns:**
- `bool`: True if root, False otherwise

**Example:**
```python
from tor_route_traffic_setup import is_root
if not is_root():
    print("This script requires root privileges")
```

#### `stop_tor_if_running()`

Checks if Tor is running and stops it if necessary.

**Example:**
```python
from tor_route_traffic_setup import stop_tor_if_running
stop_tor_if_running()
```

#### `create_directory(directory)`

Creates the specified directory with proper permissions (700).

**Parameters:**
- `directory` (str): Directory path

**Example:**
```python
from tor_route_traffic_setup import create_directory
create_directory("/home/user/.tor_config")
```

#### `create_torrc_file()`

Creates the torrc file with transparent proxy configuration.

**Example:**
```python
from tor_route_traffic_setup import create_torrc_file
create_torrc_file()
```

#### `install_packages()`

Installs necessary packages (tor, iptables-persistent).

**Example:**
```python
from tor_route_traffic_setup import install_packages
install_packages()
```

#### `get_tor_uid()`

Gets the UID of the 'debian-tor' user.

**Returns:**
- `str`: UID as string

**Example:**
```python
from tor_route_traffic_setup import get_tor_uid
uid = get_tor_uid()
```

#### `setup_iptables(tor_uid)`

Sets up iptables rules to redirect all traffic through Tor.

**Parameters:**
- `tor_uid` (str): Tor user ID for owner matching

**Example:**
```python
from tor_route_traffic_setup import setup_iptables
setup_iptables("100")
```

#### `verify_tor_connection()`

Verifies that traffic is routed through Tor.

**Example:**
```python
from tor_route_traffic_setup import verify_tor_connection
verify_tor_connection()
```

### Constants

```python
torrc_directory = os.path.join(os.path.expanduser("~"), ".tor_config")
torrc_path = os.path.join(torrc_directory, "torrc")
control_port = 9051
hashed_control_password = "16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD"
```

---

## tor_vpn_inclued.py

### Overview

Tor startup validation and configuration management script.

### Functions

#### `is_tor_running()`

Checks if Tor is running on the current platform.

**Returns:**
- `bool`: True if running, False otherwise

**Example:**
```python
from tor_vpn_inclued import is_tor_running
if is_tor_running():
    print("Tor is already running")
```

#### `generate_hashed_password(password)`

Generates the hashed control password for Tor.

**Parameters:**
- `password` (str): Plain-text password

**Returns:**
- `str`: Hashed password

**Example:**
```python
from tor_vpn_inclued import generate_hashed_password
hashed = generate_hashed_password("password")
```

#### `start_tor_manual(torrc_path)`

Starts Tor manually without relying on system services.

**Parameters:**
- `torrc_path` (str): Path to torrc configuration file

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
from tor_vpn_inclued import start_tor_manual
if start_tor_manual("/path/to/torrc"):
    print("Tor started successfully")
```

#### `validate_and_generate_config()`

Validates and generates the Tor configuration file if missing.

**Returns:**
- `tuple`: (torrc_path, data_directory) or (None, None) on failure

**Example:**
```python
from tor_vpn_inclued import validate_and_generate_config
torrc_path, data_dir = validate_and_generate_config()
```

### Constants

```python
TORRC_DEFAULT_CONTENT = """SocksPort 9050
ControlPort 9051
HashedControlPassword {hashed_password}
DataDirectory {data_directory}
"""
OPERATING_SYSTEM = platform.system()
```

---

## Stem API Usage

The system uses the Stem library for Tor control port communication.

### Basic Controller Connection

```python
from stem.control import Controller

with Controller.from_port(port=9051) as controller:
    controller.authenticate(password="your_password")
    # Perform operations
```

### Authentication Methods

#### Password Authentication

```python
controller.authenticate(password="plain_password")
```

#### Cookie Authentication

```python
controller.authenticate(cookie_path="/run/tor/control.authcookie")
```

#### Default Authentication

```python
controller.authenticate()
```

### Common Operations

#### Set Exit Node

```python
controller.set_conf("ExitNodes", "{us}")
controller.signal(Signal.NEWNYM)
```

#### Get Circuits

```python
circuits = controller.get_circuits()
for circuit in circuits:
    print(f"Circuit {circuit.id}: {circuit.purpose}")
```

#### Get Version

```python
version = controller.get_version()
print(f"Tor version: {version}")
```

#### New Identity

```python
from stem import Signal
controller.signal(Signal.NEWNYM)
```

---

## Error Handling

### Common Exceptions

#### TorConnectionError

Raised when Tor connection fails.

```python
try:
    connect_to_tor("us")
except TorConnectionError as e:
    print(f"Connection failed: {e}")
```

#### AuthenticationError

Raised when authentication fails.

```python
try:
    controller.authenticate(password="password")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

#### ConfigurationError

Raised when configuration is invalid.

```python
try:
    validate_tor_configuration()
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

---

## Additional Resources

- [Home](Home) - Wiki home page
- [User Guide](User-Guide) - User guide
- [Developer Guide](Developer-Guide) - Developer guide
- [Stem Documentation](https://stem.torproject.org) - Stem library documentation

---

**Last Updated**: 2024-04-23
