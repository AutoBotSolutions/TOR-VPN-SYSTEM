# Python Scripts Documentation

This document provides detailed documentation for all Python scripts in the Tor VPN system.

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
The main GUI application for Tor VPN management with country-specific exit node selection.

### Purpose
Provides a Tkinter-based graphical interface for connecting to Tor with the ability to select specific exit nodes by country code.

### Dependencies
- `tkinter` - GUI framework
- `stem` - Tor control library
- Standard library modules: os, sys, signal, subprocess, socket, logging

### Key Features
- Country-specific exit node selection (200+ countries)
- Real-time connection status display
- Connect/disconnect functionality
- Server list browser
- Precomputed password authentication

### Global Constants
```python
TOR_PASSWORD_ENV = "TOR_PASSWORD"
TOR_DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".tor_config")
TOR_CONFIG_FILE = os.path.join(TOR_DEFAULT_DIR, "torrc")
DEFAULT_PASSWORD = "467rSeG7%tGd757575EwPLsaQ$BplwEQJ7676RLsa$3@4161"
PRECOMPUTED_HASHED_PASSWORD = "16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD"
LOG_FILE = "vpn_app_advanced.log"
```

### Main Functions

#### `setup_logging(log_file=LOG_FILE)`
Sets up rotating file handlers for logging with both file and console output.

**Parameters:**
- `log_file` (str): Path to log file (default: "vpn_app_advanced.log")

**Returns:**
- `logger`: Configured logger instance

#### `setup_signal_handlers()`
Configures signal handlers for clean termination (SIGTERM, SIGINT).

#### `ensure_admin_privileges()`
Verifies the script is running with administrator/root privileges. Exits if not.

#### `update_tor_config_file(hashed_password)`
Updates the Tor configuration file (torrc) with hashed password and control port.

**Parameters:**
- `hashed_password` (str): Precomputed hashed password for Tor authentication

#### `restart_tor_service()`
Restarts the Tor service to ensure updated configuration is loaded.

#### `validate_tor_control_port()`
Checks if the Tor control port (9051) is accessible via socket connection.

**Returns:**
- `bool`: True if accessible, False otherwise

#### `initialize_tor_config()`
Initializes Tor configuration by:
- Using precomputed hashed password
- Updating the configuration file
- Verifying the Tor service
- Restarting if necessary

#### `connect_to_tor(country_code)`
Connects to Tor using the specified country code for the exit node.

**Parameters:**
- `country_code` (str): Two-letter country code (e.g., "us", "de")

**Raises:**
- `ValueError`: If invalid country code provided
- `Exception`: For connection failures

#### `disconnect_tor()`
Disconnects from Tor by resetting exit node configurations.

### GUI Classes

#### `VPNInterface`
Main GUI class for the Tor VPN client.

**Methods:**
- `__init__(master)`: Initialize the GUI window
- `create_widgets()`: Build all GUI components
- `create_status_tab()`: Create connection status tab
- `create_servers_tab()`: Create server list tab
- `connect()`: Connect to Tor with user-specified country
- `disconnect()`: Disconnect from Tor

**GUI Components:**
- Status tab with connection status label
- Connect/Disconnect buttons
- Servers tab with country list treeview
- Color-coded status indicators

### Usage
```bash
sudo python tor_vpn_beta.py
```

### Security Notes
⚠️ Contains hardcoded password - should be changed for production use

---

## tor_custom_config.py

### Overview
Custom Tor configuration generator with user-specified password and ownership management.

### Purpose
Creates a custom torrc configuration file with user-provided password, sets proper permissions, and manages file ownership.

### Dependencies
- Standard library: os, logging, stat, pwd, grp, subprocess, getpass

### Key Features
- Interactive password input (using getpass)
- Automatic password hashing
- Directory creation with secure permissions
- File ownership management
- Permission verification

### Global Constants
```python
torrc_directory = os.path.join(os.path.expanduser("~"), ".tor_config")
torrc_path = os.path.join(torrc_directory, "torrc")
control_port = 9051
```

### Main Functions

#### `generate_hashed_password(password)`
Generates the hashed control password for Tor using the `tor --hash-password` command.

**Parameters:**
- `password` (str): Plain-text password

**Returns:**
- `str`: Hashed password string

**Raises:**
- `subprocess.CalledProcessError`: If hashing fails

#### `change_ownership(file_path, user_name, group_name)`
Changes the ownership of a file to the specified user and group.

**Parameters:**
- `file_path` (str): Path to the file
- `user_name` (str): Username for ownership
- `group_name` (str): Group name for ownership

**Raises:**
- `KeyError`: If user or group doesn't exist
- `PermissionError`: If insufficient permissions

#### `create_directory(directory)`
Creates the specified directory with proper permissions (700).

**Parameters:**
- `directory` (str): Directory path to create

#### `create_torrc_file()`
Creates the torrc file with:
- User-provided password
- Hashed password generation
- Proper file permissions (600)
- Ownership assignment

#### `verify_file_access(file_path)`
Verifies file permissions and accessibility.

**Parameters:**
- `file_path` (str): Path to file to verify

### Usage
```bash
sudo python tor_custom_config.py
```

### Output
- Creates `~/.tor_config/torrc`
- Logs to `create_torrc.log`

---

## tor_auto_torrc_config.py

### Overview
Automated Tor setup and configuration script with cross-platform support.

### Purpose
Automates the entire Tor installation and configuration process including directory setup, torrc generation, and service restart.

### Dependencies
- Standard library: os, platform, subprocess, shutil, sys, getpass

### Key Features
- Cross-platform support (Linux, macOS, Windows)
- Automatic Tor installation
- Directory setup with proper permissions
- Custom torrc generation
- Service restart with password prompt

### Global Constants
```python
DEFAULT_DATA_DIR = "/var/lib/tor"  # Linux
DEFAULT_LOG_DIR = "/var/log/tor"    # Linux
DEFAULT_USER_TORRC_PATH = "~/.tor/torrc"
DEFAULT_CONTROL_PASSWORD = "TorSecurePassword123!"
```

### Main Functions

#### `check_if_tor_installed()`
Checks if Tor is already installed by checking for the tor binary in PATH.

**Returns:**
- `bool`: True if installed, False otherwise

#### `install_tor()`
Installs Tor depending on the operating system:
- Linux: `sudo apt install tor`
- macOS: `brew install tor`
- Windows: Manual installation required

#### `generate_hashed_password(password)`
Generates hashed control password for Tor.

**Parameters:**
- `password` (str): Plain-text password

**Returns:**
- `str`: Hashed password

#### `setup_directories(data_dir, log_dir)`
Creates necessary directories for Tor data and logs.

**Parameters:**
- `data_dir` (str): Data directory path
- `log_dir` (str): Log directory path

#### `apply_torrc(data_dir, log_dir, custom_torrc_path=None)`
Generates and applies the custom torrc configuration file.

**Parameters:**
- `data_dir` (str): Data directory path
- `log_dir` (str): Log directory path
- `custom_torrc_path` (str, optional): Custom torrc path

#### `restart_tor()`
Handles Tor service restart securely with password prompt.

**Security:**
- Uses `getpass` for secure password input
- Passes password via stdin to avoid command-line exposure

### Usage
```bash
# Use defaults
python tor_auto_torrc_config.py

# Custom directories
python tor_auto_torrc_config.py /custom/data/dir /custom/log/dir /custom/torrc/path
```

### Command-line Arguments
1. Data directory (optional)
2. Log directory (optional)
3. Torrc path (optional)

---

## tor_diagnostic_repair.py

### Overview
Comprehensive Tor diagnostic and repair tool with init system detection.

### Purpose
Diagnoses Tor configuration issues, detects init systems, validates passwords, and repairs Tor service problems.

### Dependencies
- `stem` - Tor control library
- `psutil` - Process utilities
- Standard library: platform, subprocess, os, logging, getpass, shutil, argparse

### Key Features
- Init system detection (systemd, sysvinit, manual)
- Sudo password validation with retry
- Tor process detection and management
- Configuration validation
- Custom command support
- Diagnostic collection

### Command-line Arguments
```bash
--tor-binary          Path to Tor binary (default: 'tor')
--tor-config          Path to Tor config (default: '/etc/tor/torrc')
--custom-start-command Custom command to start Tor
--custom-stop-command  Custom command to stop Tor
```

### Main Functions

#### `parse_arguments()`
Parses command-line arguments for custom paths and commands.

**Returns:**
- `argparse.Namespace`: Parsed arguments

#### `setup_logging()`
Configures logging to work in both console and file outputs with graceful fallback.

#### `check_tor_version()`
Checks and logs the installed Tor version.

#### `detect_init_system()`
Detects the initialization system used by the host system.

**Returns:**
- `str`: 'systemd', 'sysvinit', or 'manual'

#### `prompt_for_password()`
Prompts the user for sudo password with fallback methods.

**Returns:**
- `str`: Password string

#### `validate_sudo_password(sudo_password)`
Validates the provided sudo password by running 'sudo -v'.

**Parameters:**
- `sudo_password` (str): Password to validate

**Returns:**
- `bool`: True if valid, False otherwise

#### `run_command(command, sudo_password=None)`
Executes a shell command with optional sudo password.

**Parameters:**
- `command` (list): Command to execute
- `sudo_password` (str, optional): Sudo password

**Returns:**
- `tuple`: (success: bool, output: str)

#### `find_tor_process()`
Locates the Tor process by checking active processes.

**Returns:**
- `int` or `None`: PID of Tor process if found

#### `stop_tor_directly(sudo_password=None)`
Stops the Tor process manually by sending a kill signal.

**Parameters:**
- `sudo_password` (str, optional): Sudo password

**Returns:**
- `bool`: True if successful

#### `start_tor_directly()`
Starts the Tor process manually using the specified Tor binary.

**Returns:**
- `bool`: True if successful

#### `validate_tor_configuration()`
Validates the provided Tor binary and checks the configuration file.

**Returns:**
- `bool`: True if valid, False otherwise

#### `restart_tor_with_systemd(sudo_password)`
Restarts the Tor service using systemd.

**Parameters:**
- `sudo_password` (str): Sudo password

**Returns:**
- `bool`: Success status

#### `restart_tor_with_sysvinit(sudo_password)`
Restarts the Tor service using SysVinit.

**Parameters:**
- `sudo_password` (str): Sudo password

**Returns:**
- `bool`: Success status

#### `validate_running_tor()`
Validates whether the Tor process is running after a restart attempt.

**Returns:**
- `bool`: True if running, False otherwise

#### `restart_tor_service(init_system, sudo_password)`
Restarts the Tor service using the detected init system.

**Parameters:**
- `init_system` (str): Detected init system
- `sudo_password` (str): Sudo password

**Returns:**
- `bool`: Success status

#### `collect_diagnostics(output_dir="diagnostics")`
Collects diagnostic logs and custom configuration files.

**Parameters:**
- `output_dir` (str): Directory for diagnostic output

### Usage
```bash
# Basic usage
sudo python tor_diagnostic_repair.py

# With custom paths
sudo python tor_diagnostic_repair.py --tor-binary /usr/bin/tor --tor-config /etc/tor/torrc
```

### Output
- Creates `diagnostics/` directory with:
  - `torrc` - Tor configuration snapshot
  - `logfile.log` - Collected logs
  - `system_info.txt` - System information

---

## tor_network_test.py

### Overview
Tor network connectivity and performance testing tool.

### Purpose
Tests Tor network connectivity, measures latency, detects exit IP, and validates circuit information.

### Dependencies
- `stem` - Tor control library
- `requests` - HTTP library
- Standard library: logging, os, time, subprocess, socket

### Key Features
- Tor service status checking
- Control port detection
- Authentication method auto-detection (password or cookie)
- Latency measurement
- Exit IP detection
- Circuit information display

### Configuration Paths
```python
TORRC_PATHS = [
    "/etc/tor/torrc",
    "/usr/local/etc/tor/torrc",
    "~/.torrc"
]
AUTH_COOKIE_PATHS = [
    "/run/tor/control.authcookie",
    "/var/lib/tor/control_auth_cookie"
]
```

### Main Functions

#### `is_tor_running()`
Checks if the Tor service is running using pgrep.

**Returns:**
- `bool`: True if running, False otherwise

#### `get_process_using_port(port)`
Detects the process using the specified port using lsof.

**Parameters:**
- `port` (int): Port number to check

**Returns:**
- `str` or `None`: Process details if found

#### `check_port_status(host, port)`
Checks if the specified port is open and listening.

**Parameters:**
- `host` (str): Host address
- `port` (int): Port number

**Returns:**
- `bool`: True if open, False otherwise

#### `detect_tor_control_port()`
Detects the Tor control port from the torrc file.

**Returns:**
- `int`: Control port number (default: 9051)

#### `detect_tor_password()`
Tries to auto-detect the Tor Control Port password from torrc files.

**Returns:**
- `str` or `None`: Detected password (or None if hashed)

#### `detect_auth_cookie()`
Tries to auto-detect the Tor Control Port authentication cookie.

**Returns:**
- `str` or `None`: Path to auth cookie if found

#### `is_control_port_accessible(port)`
Checks if the Tor control port is accessible via Stem controller.

**Parameters:**
- `port` (int): Control port number

**Returns:**
- `bool`: True if accessible, False otherwise

#### `test_tor_connection()`
Main function to test Tor network connectivity.

**Returns:**
- `dict`: Test results containing:
  - `connection` (bool): Connection status
  - `latency` (float): Latency in seconds
  - `exit_ip` (str): Exit IP address
  - `errors` (list): List of error messages

### Test Results Structure
```python
{
    "connection": bool,
    "latency": float or None,
    "exit_ip": str or None,
    "errors": list
}
```

### Usage
```bash
python tor_network_test.py
```

### Output
- Logs detailed test information
- Returns structured results
- Displays circuit information

---

## tor_route_traffic_setup.py

### Overview
Transparent proxy setup script for routing all system traffic through Tor.

### Purpose
Configures iptables rules to redirect all system traffic through Tor's transparent proxy port.

### Dependencies
- Standard library: os, subprocess, sys, logging, stat

### Key Features
- Root privilege verification
- Tor process management
- iptables rule configuration
- Transparent proxy setup
- DNS redirection through Tor
- Service management (systemd/init.d)

### Global Constants
```python
torrc_directory = os.path.join(os.path.expanduser("~"), ".tor_config")
torrc_path = os.path.join(torrc_directory, "torrc")
control_port = 9051
hashed_control_password = "16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD"
```

### Transparent Proxy Configuration
```python
transparent_proxy_config = """
ControlPort {control_port}
HashedControlPassword {hashed_password}
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort 9040     # Transparent proxy port
DNSPort 5353       # DNS resolver port
"""
```

### Main Functions

#### `is_root()`
Checks if the script is being run as root.

**Returns:**
- `bool`: True if root, False otherwise

#### `stop_tor_if_running()`
Checks if Tor is running and stops it if necessary.

#### `create_directory(directory)`
Creates the specified directory with proper permissions (700).

**Parameters:**
- `directory` (str): Directory path

#### `create_torrc_file()`
Creates the torrc file with transparent proxy configuration.

#### `install_packages()`
Installs necessary packages (tor, iptables-persistent).

#### `get_tor_uid()`
Gets the UID of the 'debian-tor' user.

**Returns:**
- `str`: UID as string

#### `setup_iptables(tor_uid)`
Sets up iptables rules to redirect all traffic through Tor.

**Parameters:**
- `tor_uid` (str): Tor user ID for owner matching

**iptables Rules Applied:**
1. Allow loopback traffic
2. Allow local network traffic
3. Redirect DNS to Tor DNS port (5353)
4. Redirect TCP traffic to Tor transparent port (9040)
5. Allow Tor's own traffic
6. Allow established connections
7. Reject all other traffic

#### `verify_tor_connection()`
Verifies that traffic is routed through Tor by checking torproject.org.

### Usage
```bash
sudo python tor_route_traffic_setup.py
```

### Requirements
- Must be run as root
- Tor must be installed
- iptables must be available

### Security Notes
⚠️ This script modifies system firewall rules. Use with caution.

---

## tor_vpn_inclued.py

### Overview
Tor startup validation and configuration management script.

### Purpose
Validates Tor configuration, generates missing config files, and starts Tor manually without relying on system services.

### Dependencies
- Standard library: os, platform, subprocess, logging, shutil, getpass, time

### Key Features
- Cross-platform Tor status checking
- Manual Tor startup
- Configuration validation
- Automatic config generation
- Platform-specific paths

### Global Constants
```python
TORRC_DEFAULT_CONTENT = """SocksPort 9050
ControlPort 9051
HashedControlPassword {hashed_password}
DataDirectory {data_directory}
"""
OPERATING_SYSTEM = platform.system()
```

### Main Functions

#### `is_tor_running()`
Checks if Tor is running on the current platform.

**Returns:**
- `bool`: True if running, False otherwise

**Platform-specific methods:**
- Windows: Uses `tasklist` to check for tor.exe
- Linux/macOS: Uses `pidof` to check for tor process

#### `generate_hashed_password(password)`
Generates the hashed control password for Tor.

**Parameters:**
- `password` (str): Plain-text password

**Returns:**
- `str`: Hashed password

#### `start_tor_manual(torrc_path)`
Starts Tor manually without relying on system services.

**Parameters:**
- `torrc_path` (str): Path to torrc configuration file

**Returns:**
- `bool`: True if successful, False otherwise

#### `validate_and_generate_config()`
Validates and generates the Tor configuration file if missing.

**Returns:**
- `tuple`: (torrc_path, data_directory) or (None, None) on failure

**Platform-specific paths:**
- Windows: `%APPDATA%\tor`
- macOS: `~/Library/Application Support/Tor`
- Linux: `~/.tor`

### Usage
```bash
python tor_vpn_inclued.py
```

### Workflow
1. Check if Tor is already running
2. If not running, validate/generate configuration
3. Prompt for password if needed
4. Start Tor manually with configuration

---

## Common Patterns Across Scripts

### Authentication Methods
1. **Password-based**: Uses `HashedControlPassword` in torrc
2. **Cookie-based**: Uses `CookieAuthentication 1` and auth cookie file
3. **Default**: No authentication (not recommended)

### Configuration Management
- Most scripts use `~/.tor_config/torrc` as default
- Platform-specific fallbacks are implemented
- Permissions are set to 600 for files, 700 for directories

### Logging
- All scripts use Python's logging module
- Common log format: timestamp - level - message
- Both file and console logging are typical

### Error Handling
- Try-except blocks for subprocess operations
- Graceful fallbacks for missing dependencies
- Detailed error messages for troubleshooting

### Security Best Practices (Not Always Followed)
⚠️ **Security Issues to Address:**
- Hardcoded passwords in some scripts
- Passwords passed via command-line in some cases
- Root privilege requirements without proper validation
- Missing input sanitization in some functions
