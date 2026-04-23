# Shell Scripts Documentation

This document provides detailed documentation for all shell scripts in the Tor VPN system.

## Table of Contents

- [setup_tor_custom.sh](#setup_tor_custom.sh)
- [tor_auto_proxy.sh](#tor_auto_proxy.sh)

---

## setup_tor_custom.sh

### Overview
Bash script for setting up custom Tor configuration with proper permissions and service integration.

### Purpose
Automates the setup of a custom Tor configuration file, sets appropriate permissions, modifies the init script, and enables the Tor service to start on boot.

### Dependencies
- Bash shell
- sudo privileges
- Tor service (init.d based)
- Standard Unix utilities: chown, chmod, sed, killall, netstat

### Key Features
- Admin password prompt at script start
- Automatic Tor service user detection
- Permission configuration for custom torrc
- Init script modification
- Boot enablement
- Service restart and verification
- Port listening verification

### Configuration Variables
```bash
CUSTOM_TORRC_PATH="~/.tor_config/torrc"
CUSTOM_TORRC_DIR="~/.tor_config"
INIT_SCRIPT_PATH="/etc/init.d/tor"
```

### Functions

#### `set_permissions()`
Sets proper permissions for the custom torrc path and directories.

**Actions:**
1. Detects Tor service user (default: debian-tor)
2. Changes ownership of custom torrc directory to service user
3. Sets execute permission on current user (750)
4. Sets recursive permissions on torrc directory (750)
5. Sets file permissions on torrc (640)
6. Debug output of permission settings

**Parameters:**
- Uses global `$ADMIN_PASS` for sudo operations
- Uses global `$CUSTOM_TORRC_PATH` and `$CUSTOM_TORRC_DIR`

### Script Execution Flow

#### Step 1: Admin Password Prompt
```bash
echo "Please enter your admin password:"
read -s ADMIN_PASS
```
Prompts for admin password silently and stores in `$ADMIN_PASS` variable.

#### Step 2: Stop Existing Tor Processes
```bash
echo "$ADMIN_PASS" | sudo -S killall tor 2>/dev/null
```
Stops any running Tor processes to prevent conflicts during setup.

#### Step 3: Set Permissions
Calls `set_permissions()` function to configure proper file and directory permissions.

#### Step 4: Modify Init Script
```bash
echo "$ADMIN_PASS" | sudo -S sed -i "s|/usr/bin/tor .*|/usr/bin/tor -f $CUSTOM_TORRC_PATH|" "$INIT_SCRIPT_PATH"
```
Modifies `/etc/init.d/tor` to use the custom torrc configuration file.

**Check:**
- Verifies if already configured before modification
- Exits on failure with error message

#### Step 5: Enable Boot Startup
```bash
echo "$ADMIN_PASS" | sudo -S update-rc.d tor defaults
```
Enables Tor service to start automatically on system boot using SysVinit.

#### Step 6: Restart Tor Service
```bash
echo "$ADMIN_PASS" | sudo -S /etc/init.d/tor restart
```
Restarts the Tor service with the new custom configuration.

#### Step 7: Verify Tor Process
```bash
ps aux | grep "[t]or -f $CUSTOM_TORRC_PATH"
```
Verifies that Tor is running with the custom configuration file.

#### Step 8: Check Listening Ports
```bash
echo "$ADMIN_PASS" | sudo -S netstat -tulnp | grep tor
```
Verifies that Tor is listening on the expected ports.

### Usage
```bash
sudo bash setup_tor_custom.sh
```

### Requirements
- Must be run with sudo privileges
- Tor must be installed
- init.d service management must be available
- User must exist on the system

### Output
- Console output showing each step
- Success/failure messages
- Debug permission information

### Error Handling
- Exits on failure to update init script
- Exits on failure to enable boot startup
- Exits on failure to restart Tor
- Exits if Tor not listening on expected ports

### Security Considerations
⚠️ **Security Issues:**
- Password stored in variable during script execution
- Password passed via stdin to sudo
- No password validation
- Hardcoded user paths

### Troubleshooting
- If Tor doesn't start: Check `journalctl -xe | grep -i tor`
- If permissions fail: Verify user exists
- If init script fails: Check `/etc/init.d/tor` exists

---

## tor_auto_proxy.sh

### Overview
Interactive bash script for managing Tor proxy settings with a Zenity-based GUI.

### Purpose
Provides a user-friendly graphical interface for enabling/disabling system-wide Tor proxy settings and opening browsers with Tor routing.

### Dependencies
- Bash shell
- Zenity (GTK+ dialog utility)
- Tor service running on localhost
- Standard Unix utilities

### Key Features
- Cross-platform compatibility (Linux/macOS detection)
- System-wide proxy environment variable management
- Browser integration (Chrome, Firefox)
- Temporary Firefox profile creation
- Logging to file
- Interactive menu system

### Configuration Variables
```bash
TOR_LOG_FILE="$HOME/tor_management_gui.log"
TOR_PORT=9050
CONTROL_PORT=9051
UI_WIDTH=500
UI_HEIGHT=500
```

### Platform Detection
```bash
is_macos=false
if [[ "$OSTYPE" == "darwin"* ]]; then
   is_macos=true
fi
```
Detects macOS vs Linux for platform-specific operations.

### Functions

#### `enable_tor_proxy()`
Enables system-wide Tor proxy by setting environment variables.

**Actions:**
```bash
export http_proxy="socks5h://127.0.0.1:$TOR_PORT"
export https_proxy="socks5h://127.0.0.1:$TOR_PORT"
export all_proxy="socks5h://127.0.0.1:$TOR_PORT"
```

**Note:** These exports only affect the current shell session and child processes.

#### `disable_tor_proxy()`
Disables system-wide Tor proxy by unsetting environment variables.

**Actions:**
```bash
unset http_proxy https_proxy all_proxy
```

#### `log_message(message_type, message)`
Logs messages with timestamp to the log file.

**Parameters:**
- `message_type`: INFO, ERROR, etc.
- `message`: The message to log

**Format:**
```
[YYYY-MM-DD HH:MM:SS] [message_type] message
```

#### `stream_command_output(title, command)`
Executes a command and streams its output to a Zenity text info dialog.

**Parameters:**
- `title`: Window title for the dialog
- `command`: Command to execute

**Actions:**
1. Creates temporary file for output
2. Executes command in background
3. Streams output to Zenity dialog
4. Cleans up temporary file

#### `open_browser_with_tor(browser)`
Opens a web browser with Tor proxy configuration.

**Parameters:**
- `browser`: "chrome" or "firefox"

**Chrome:**
```bash
google-chrome --proxy-server="socks5://127.0.0.1:$TOR_PORT"
```

**Firefox:**
- Creates temporary profile directory
- Generates user.js with proxy settings
- Opens Firefox with temporary profile in private mode

#### `setup_firefox_temp_profile()`
Creates a temporary Firefox profile with Tor proxy settings.

**Actions:**
1. Creates temporary directory for profile
2. Writes user.js with proxy configuration:
   - `network.proxy.type = 1` (manual proxy)
   - `network.proxy.socks = 127.0.0.1`
   - `network.proxy.socks_port = 9050`
   - `network.proxy.socks_remote_dns = true`

**Returns:**
- Path to temporary profile directory

### Main Menu Loop

The script presents an interactive Zenity menu with the following options:

| Command | Description |
|---------|-------------|
| enable_proxy | Enable proxy system-wide for Tor |
| disable_proxy | Disable proxy system-wide |
| open_chrome | Open Google Chrome with traffic routed through Tor |
| open_firefox | Open Firefox with traffic routed through Tor |
| exit | Exit the Script |

### Usage
```bash
bash tor_auto_proxy.sh
```

### Requirements
- Zenity must be installed:
  - Linux: `sudo apt install zenity`
  - macOS: `brew install zenity`
- Tor service must be running on port 9050
- Chrome or Firefox must be installed for browser options

### Platform-Specific Behavior

#### Linux
- Uses standard package manager for Zenity installation
- Standard browser paths

#### macOS
- Detects macOS via `$OSTYPE`
- Recommends Homebrew for Zenity installation
- May require different browser paths

### Logging
All actions are logged to `$HOME/tor_management_gui.log` with timestamps and message types.

### Error Handling
- Exits if Zenity is not installed with platform-specific instructions
- Shows error dialog for invalid browser selection
- Shows error dialog for invalid menu options
- Logs all errors to log file

### Limitations
- Proxy environment variables only affect current shell session
- Does not modify system-wide proxy settings permanently
- Temporary Firefox profile is deleted on browser close
- Requires manual Tor service management

### Security Considerations
- No password handling (relies on Tor being already configured)
- Proxy settings are temporary
- Temporary profiles are cleaned up automatically
- Logs may contain sensitive information (commands executed)

### Troubleshooting
- If Zenity not found: Install using package manager
- If browsers don't open: Check browser installation paths
- If proxy not working: Verify Tor is running on port 9050
- Check log file for detailed error information

---

## Common Patterns Across Shell Scripts

### Password Handling
- `setup_tor_custom.sh`: Prompts for password at start, stores in variable
- `tor_auto_proxy.sh`: No password handling (assumes Tor already configured)

### Sudo Usage
- Both scripts use `echo "$PASSWORD" | sudo -S` pattern
- Password passed via stdin to avoid command-line exposure
- No password validation in either script

### Error Handling
- Exit on critical failures
- Error messages to console
- Some scripts have logging, others don't
- Limited retry logic

### Platform Detection
- `tor_auto_proxy.sh`: Has explicit macOS/Linux detection
- `setup_tor_custom.sh`: Linux-specific (init.d)

### Service Management
- `setup_tor_custom.sh`: Uses init.d for service management
- `tor_auto_proxy.sh`: No service management (assumes running)

### Logging
- `setup_tor_custom.sh`: Console output only
- `tor_auto_proxy.sh`: File logging to `$HOME/tor_management_gui.log`

### GUI Integration
- `setup_tor_custom.sh`: No GUI (command-line only)
- `tor_auto_proxy.sh`: Zenity-based GUI

### Security Best Practices (Not Always Followed)
⚠️ **Security Issues to Address:**
- Passwords stored in shell variables
- No password encryption
- Limited input validation
- Hardcoded paths and user names
- No audit logging for sensitive operations
