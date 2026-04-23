# Configuration Files and Logs Documentation

This document provides detailed documentation for all configuration files, log files, and diagnostic outputs in the Tor VPN system.

## Table of Contents

- [Configuration Files](#configuration-files)
- [Log Files](#log-files)
- [Diagnostic Files](#diagnostic-files)
- [Dependency Files](#dependency-files)

---

## Configuration Files

### Tor Configuration (torrc)

#### Location
- **Primary**: `~/.tor_config/torrc` (user home directory)
- **System**: `/etc/tor/torrc`
- **User**: `~/.tor/torrc`
- **Diagnostics**: `diagnostics/torrc` (snapshot)

#### Standard Configuration Template

```bash
# Basic Tor Configuration
ControlPort 9051
HashedControlPassword {hashed_password}
CookieAuthentication 1
SocksPort 9050
DataDirectory {data_directory}
Log notice file {log_directory}/notices.log
Log warn file {log_directory}/warnings.log
Log debug file {log_directory}/debug.log
```

#### Transparent Proxy Configuration

```bash
# Transparent Proxy Configuration
ControlPort 9051
HashedControlPassword {hashed_password}
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort 9040     # Transparent proxy port
DNSPort 5353       # DNS resolver port
```

#### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| ControlPort | 9051 | Tor control interface port for Stem API |
| SocksPort | 9050 | SOCKS5 proxy port for applications |
| TransPort | 9040 | Transparent proxy port for system-wide routing |
| DNSPort | 5353 | DNS resolver port for DNS through Tor |
| HashedControlPassword | - | Hashed password for control port authentication |
| CookieAuthentication | 1 | Enable cookie-based authentication |
| DataDirectory | /var/lib/tor | Tor data storage directory |
| VirtualAddrNetworkIPv4 | 10.192.0.0/10 | Virtual address network for transparent proxy |
| AutomapHostsOnResolve | 1 | Automap .onion addresses to virtual addresses |

#### Security Settings

#### Ownership and Permissions

- **Owner**: Current user (or debian-tor for system Tor)
- **Group**: Current user's group (or debian-tor for system Tor)
- **torrc**: `600` (owner read/write only)
- **Config directory**: `700` (owner read/write/execute only)

#### Password Hashing

Tor uses SHA1-based password hashing for control port authentication:

```bash
# Generate hashed password
tor --hash-password "your_password"
# Output: 16:HASHED_PASSWORD_STRING
```

**Example from system:**
```
16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD
```

#### Authentication Methods

1. **Password-based**: Uses `HashedControlPassword` in torrc
2. **Cookie-based**: Uses `CookieAuthentication 1` and auth cookie file
3. **None**: Not recommended for production use

#### Platform-Specific Paths

| Platform | Default Data Directory | Default Config Path |
|----------|----------------------|-------------------|
| Linux | /var/lib/tor | /etc/tor/torrc |
| macOS | ~/Library/Application Support/Tor | /usr/local/etc/tor/torrc |
| Windows | %APPDATA%\tor | %APPDATA%\tor\torrc |

---

## Log Files

### vpn_app_advanced.log

#### Location
- `/home/robbie/Desktop/tor_vpn/vpn_app_advanced.log`

#### Purpose
Main application log for the Tor VPN GUI application (`tor_vpn_beta.py`).

#### Format
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

#### Log Levels
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages for potential issues
- ERROR: Error messages for failures
- CRITICAL: Critical errors requiring immediate attention

#### Rotation
- Max file size: 1,000,000 bytes (1 MB)
- Backup count: 5 files
- Handler: RotatingFileHandler

#### Typical Entries
```
2024-01-15 10:30:45,123 - root - INFO - Initializing Tor configuration...
2024-01-15 10:30:45,456 - root - DEBUG - Using precomputed hashed password: 16:B76A...
2024-01-15 10:30:46,789 - root - INFO - Tor configuration initialized successfully.
```

### logfile.log

#### Location
- `/home/robbie/Desktop/tor_vpn/logfile.log`
- `/home/robbie/Desktop/tor_vpn/diagnostics/logfile.log`

#### Purpose
Diagnostic log file used by `tor_diagnostic_repair.py`.

#### Format
```
[%(asctime)s.%(msecs)03d] %(levelname)s :: %(message)s
```
Example:
```
[2024-01-15 10:30:45.123] INFO :: Starting Tor diagnostic and repair tool...
```

#### Content
- System information
- Tor version checks
- Init system detection
- Sudo password validation
- Service restart attempts
- Process detection results
- Error messages and stack traces

### create_torrc.log

#### Location
- `/home/robbie/Desktop/tor_vpn/create_torrc.log`

#### Purpose
Log file for `tor_custom_config.py` torrc creation process.

#### Format
```
%(asctime)s - %(levelname)s - %(message)s
```

#### Content
- Directory creation status
- Password generation results
- File permission changes
- Ownership modifications
- File access verification

### setup_tor.log

#### Location
- `/home/robbie/Desktop/tor_vpn/setup_tor.log`

#### Purpose
Log file for `tor_route_traffic_setup.py` transparent proxy setup.

#### Format
```
%(asctime)s - %(levelname)s - %(message)s
```

#### Content
- Root privilege checks
- Tor process status
- Directory creation
- Package installation
- iptables rule application
- Connection verification

### tor_management_gui.log

#### Location
- `$HOME/tor_management_gui.log`

#### Purpose
Log file for `tor_auto_proxy.sh` bash GUI script.

#### Format
```
[YYYY-MM-DD HH:MM:SS] [message_type] message
```

#### Content
- Proxy enable/disable actions
- Browser launch attempts
- Error messages
- User actions

---

## Diagnostic Files

### diagnostics/torrc

#### Location
- `/home/robbie/Desktop/tor_vpn/diagnostics/torrc`

#### Purpose
Snapshot of the Tor configuration file collected during diagnostics.

#### Content
```bash
ControlPort 9051
HashedControlPassword Mar 21 23:38:11.970 [warn] You are running Tor as root. You don't need to, and you probably shouldn't.
16:B0CEBA820EDC964160DF8AAE1AEA9B66919D22D3948C9A6E2B35488BBE

# Transparent proxy settings for Tor
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort 9040     # Transparent proxy port
DNSPort 5353       # DNS resolver port
```

#### Notes
- Contains warning about running Tor as root
- Includes both control port and transparent proxy settings
- Hashed password is included (security risk if directory not protected)

### diagnostics/system_info.txt

#### Location
- `/home/robbie/Desktop/tor_vpn/diagnostics/system_info.txt`

#### Purpose
System information collected during diagnostics.

#### Content
```
System Info: Linux-6.1.0-32-amd64-x86_64-with-glibc2.36
Python Version: 3.10.16
```

#### Information Included
- Operating system and kernel version
- Architecture (x86_64)
- glibc version
- Python version

### diagnostics/logfile.log

#### Location
- `/home/robbie/Desktop/tor_vpn/diagnostics/logfile.log`

#### Purpose
Copy of the main logfile.log for diagnostic purposes.

#### Content
Same as main logfile.log, copied to diagnostics directory for analysis.

---

## Dependency Files

### requirements.txt

#### Location
- `/home/robbie/Desktop/tor_vpn/requirements.txt`

#### Content
```
stem~=1.8.2
psutil~=7.0.0
```

#### Dependencies

##### stem~=1.8.2
- **Purpose**: Python library for communicating with Tor's control port
- **Features**: 
  - Controller connection and authentication
  - Circuit management
  - Stream handling
  - Event listening
  - Signal sending (NEWNYM, etc.)
- **Used in**: 
  - tor_vpn_beta.py
  - tor_network_test.py
  - tor_diagnostic_repair.py

##### psutil~=7.0.0
- **Purpose**: Cross-platform library for process and system monitoring
- **Features**:
  - Process information retrieval
  - System resource monitoring
  - Network connection tracking
- **Used in**:
  - tor_diagnostic_repair.py (process detection)

#### Installation
```bash
pip install -r requirements.txt
```

#### Version Constraints
- `~=` indicates compatible release (matches major.minor.patch)
- Ensures compatibility while allowing bug fixes and minor updates

---

## Empty/Placeholder Files

### tor_bash_gui.sh.py

#### Location
- `/home/robbie/Desktop/tor_vpn/tor_bash_gui.sh.py`

#### Status
- Empty file (0 bytes)
- Appears to be a placeholder or abandoned file
- No functionality implemented

#### Purpose
Unknown - possibly intended for a bash GUI wrapper in Python.

---

## Log File Management

### Log Rotation Strategy

#### Python Scripts (RotatingFileHandler)
- Max size: 1 MB per file
- Backup count: 5 files
- Total storage: ~5 MB per logger
- Naming: `logfile.log`, `logfile.log.1`, `logfile.log.2`, etc.

#### Shell Scripts
- No automatic rotation
- Manual cleanup required
- May grow indefinitely

### Log Analysis

#### Common Log Patterns

**Successful Connection:**
```
INFO - Connected to Tor with exit node: US.
INFO - Tor configuration initialized successfully.
```

**Authentication Failure:**
```
ERROR - Failed to connect to Tor: Authentication failed
ERROR - Tor Control Port 9051 is not accessible.
```

**Permission Errors:**
```
ERROR - Permission denied while changing ownership
ERROR - This script must be run with sudo/root privileges.
```

**Service Issues:**
```
ERROR - Tor service restart failed
ERROR - No running Tor process found.
```

### Log Monitoring

#### Real-time Monitoring
```bash
# Watch main application log
tail -f vpn_app_advanced.log

# Watch diagnostic log
tail -f logfile.log

# Watch all logs
tail -f *.log
```

#### Log Filtering
```bash
# Show only errors
grep ERROR vpn_app_advanced.log

# Show authentication attempts
grep "Authenticating" logfile.log

# Show Tor service operations
grep "Tor service" *.log
```

### Log Cleanup

#### Manual Cleanup
```bash
# Remove old log files
rm logfile.log.*
rm vpn_app_advanced.log.*

# Clear log files
> logfile.log
> vpn_app_advanced.log
```

#### Automated Cleanup
```bash
# Remove logs older than 30 days
find . -name "*.log" -mtime +30 -delete

# Remove rotated logs
find . -name "*.log.*" -delete
```

---

## Configuration Best Practices

### Security Recommendations

1. **File Permissions**
   - torrc: `600` (owner read/write only)
   - Directory: `700` (owner read/write/execute only)
   - Logs: `640` (owner read/write, group read)

2. **Password Management**
   - Use strong, unique passwords
   - Avoid hardcoded passwords in scripts
   - Rotate passwords regularly
   - Use environment variables for sensitive data

3. **Ownership**
   - Tor config: owned by `debian-tor` or dedicated user
   - User config: owned by the user
   - Avoid root ownership of user files

4. **Log Security**
   - Restrict log file access
   - Avoid logging sensitive information
   - Regular log rotation and cleanup
   - Encrypt logs if containing sensitive data

### Configuration Validation

#### Validate torrc Syntax
```bash
tor --verify-config -f /path/to/torrc
```

#### Check Configuration
```bash
tor --defaults-torrc /path/to/torrc --verify-config
```

#### Test Control Port
```bash
telnet 127.0.0.1 9051
```

#### Check Tor Status
```bash
sudo systemctl status tor
# or
sudo /etc/init.d/tor status
```

### Backup Strategies

#### Configuration Backup
```bash
# Backup torrc
cp ~/.tor_config/torrc ~/.tor_config/torrc.backup

# Backup entire config directory
tar -czf tor_config_backup.tar.gz ~/.tor_config/
```

#### Log Backup
```bash
# Archive old logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz *.log
```

---

## Troubleshooting Configuration Issues

### Common Problems

#### Tor Won't Start
1. Check torrc syntax: `tor --verify-config`
2. Check file permissions: `ls -la ~/.tor_config/torrc`
3. Check ownership: `stat ~/.tor_config/torrc`
4. Review logs: `tail -f /var/log/tor/log`

#### Control Port Not Accessible
1. Verify Tor is running: `ps aux | grep tor`
2. Check firewall: `sudo iptables -L -n | grep 9051`
3. Verify port is listening: `netstat -tulnp | grep 9051`
4. Check torrc: Ensure ControlPort is set

#### Authentication Failures
1. Verify password hash in torrc
2. Check if CookieAuthentication is enabled
3. Verify auth cookie file exists and permissions
4. Test with Stem: Use `tor_network_test.py`

#### Permission Errors
1. Run with sudo if required
2. Check file ownership: `ls -la ~/.tor_config/`
3. Verify user exists: `id $USER`
4. Check group membership: `groups $USER`

### Diagnostic Commands

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

# Check system Tor status
sudo systemctl status tor

# Test Tor connection
curl --socks5 127.0.0.1:9050 https://check.torproject.org
```

---

## Configuration File Templates

### Minimal torrc
```bash
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD_HERE
SocksPort 9050
DataDirectory /var/lib/tor
```

### torrc with Logging
```bash
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD_HERE
SocksPort 9050
DataDirectory /var/lib/tor
Log notice file /var/log/tor/notices.log
Log warn file /var/log/tor/warnings.log
```

### torrc with Transparent Proxy
```bash
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD_HERE
SocksPort 9050
TransPort 9040
DNSPort 5353
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
DataDirectory /var/lib/tor
```

### torrc with Exit Node Selection
```bash
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD_HERE
SocksPort 9050
DataDirectory /var/lib/tor
ExitNodes {us}
StrictNodes 1
```
