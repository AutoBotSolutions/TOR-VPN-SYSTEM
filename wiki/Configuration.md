# Configuration Guide

This guide covers all configuration options for the Tor VPN System.

## Table of Contents

- [Tor Configuration Files](#tor-configuration-files)
- [Configuration Parameters](#configuration-parameters)
- [Authentication Methods](#authentication-methods)
- [Platform-Specific Paths](#platform-specific-paths)
- [Environment Variables](#environment-variables)
- [Advanced Configuration](#advanced-configuration)
- [Configuration Templates](#configuration-templates)

---

## Tor Configuration Files

### Default Configuration Location

The system uses custom Tor configuration files located at:

- **Linux**: `~/.tor_config/torrc` or `~/.tor/torrc`
- **macOS**: `~/Library/Application Support/Tor/torrc`
- **Windows**: `%APPDATA%\tor\torrc`

### System Configuration

- **Linux**: `/etc/tor/torrc`
- **macOS**: `/usr/local/etc/tor/torrc`
- **Windows**: `C:\Tor\torrc`

### File Permissions

Configuration files should have restricted permissions:

```bash
# torrc file
chmod 600 ~/.tor_config/torrc

# Configuration directory
chmod 700 ~/.tor_config
```

**Permissions breakdown:**
- `600` - Owner read/write only
- `700` - Owner read/write/execute only

---

## Configuration Parameters

### Basic Parameters

#### ControlPort

**Default**: `9051`

Tor control interface port for Stem API communication.

```
ControlPort 9051
```

#### SocksPort

**Default**: `9050`

SOCKS5 proxy port for applications.

```
SocksPort 9050
```

#### TransPort

**Default**: `9040`

Transparent proxy port for system-wide traffic routing.

```
TransPort 9040
```

#### DNSPort

**Default**: `5353`

DNS resolver port for DNS through Tor.

```
DNSPort 5353
```

### Authentication Parameters

#### HashedControlPassword

Hashed password for control port authentication.

```
HashedControlPassword 16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD
```

**Generate hashed password:**
```bash
tor --hash-password "your_password"
```

#### CookieAuthentication

Enable cookie-based authentication.

```
CookieAuthentication 1
```

Cookie file location: `/run/tor/control.authcookie` or `/var/lib/tor/control_auth_cookie`

### Network Parameters

#### DataDirectory

Tor data storage directory.

```
DataDirectory /var/lib/tor
```

#### VirtualAddrNetworkIPv4

Virtual address network for transparent proxy.

```
VirtualAddrNetworkIPv4 10.192.0.0/10
```

#### AutomapHostsOnResolve

Automap .onion addresses to virtual addresses.

```
AutomapHostsOnResolve 1
```

### Exit Node Parameters

#### ExitNodes

Specify exit nodes by country code.

```
ExitNodes {us}
ExitNodes {us},{de},{gb}
```

#### ExcludeNodes

Exclude specific countries from exit nodes.

```
ExcludeNodes {cn},{ru}
```

#### StrictNodes

Strictly use specified exit nodes (no fallback).

```
StrictNodes 1
```

### Logging Parameters

#### Log Levels

```
Log notice file /var/log/tor/notices.log
Log warn file /var/log/tor/warnings.log
Log debug file /var/log/tor/debug.log
```

**Log levels:**
- `debug` - Detailed debugging information
- `info` - General informational messages
- `notice` - Normal but significant conditions
- `warn` - Warning messages
- `err` - Error conditions

---

## Authentication Methods

### Password-Based Authentication

#### Setup

1. Generate hashed password:
```bash
tor --hash-password "your_secure_password"
```

2. Add to torrc:
```
HashedControlPassword 16:YOUR_HASHED_PASSWORD
```

3. Use in Python:
```python
from stem.control import Controller

with Controller.from_port(port=9051) as controller:
    controller.authenticate(password="your_plain_password")
```

### Cookie-Based Authentication

#### Setup

1. Enable in torrc:
```
CookieAuthentication 1
```

2. Ensure cookie file exists:
```bash
ls -la /run/tor/control.authcookie
```

3. Use in Python:
```python
from stem.control import Controller

with Controller.from_port(port=9051) as controller:
    controller.authenticate(cookie_path="/run/tor/control.authcookie")
```

### No Authentication (Not Recommended)

```
# Remove authentication parameters from torrc
# Only use in trusted environments
```

---

## Platform-Specific Paths

### Linux

| File | Default Location |
|------|-----------------|
| torrc | `/etc/tor/torrc` or `~/.tor_config/torrc` |
| Data directory | `/var/lib/tor` |
| Log directory | `/var/log/tor` |
| Auth cookie | `/run/tor/control.authcookie` |

### macOS

| File | Default Location |
|------|-----------------|
| torrc | `/usr/local/etc/tor/torrc` or `~/Library/Application Support/Tor/torrc` |
| Data directory | `~/Library/Application Support/Tor` |
| Log directory | `~/Library/Logs/Tor` |
| Auth cookie | `/var/run/tor/control.authcookie` |

### Windows

| File | Default Location |
|------|-----------------|
| torrc | `C:\Tor\torrc` or `%APPDATA%\tor\torrc` |
| Data directory | `%APPDATA%\tor` |
| Log directory | `%APPDATA%\tor\logs` |
| Auth cookie | `%APPDATA%\tor\data\control_auth_cookie` |

---

## Environment Variables

### TOR_PASSWORD

Set Tor control password via environment variable.

```bash
export TOR_PASSWORD="your_secure_password"
```

### TOR_CONFIG_DIR

Set custom configuration directory.

```bash
export TOR_CONFIG_DIR="/custom/config/dir"
```

### HTTP_PROXY / HTTPS_PROXY

Set system proxy environment variables.

```bash
export http_proxy="socks5h://127.0.0.1:9050"
export https_proxy="socks5h://127.0.0.1:9050"
export all_proxy="socks5h://127.0.0.1:9050"
```

---

## Advanced Configuration

### Custom Exit Node Selection

#### Single Country
```
ExitNodes {us}
```

#### Multiple Countries
```
ExitNodes {us},{de},{gb},{nl}
```

#### Exclude Countries
```
ExcludeNodes {cn},{ru},{kp}
```

#### Strict Selection
```
ExitNodes {us}
StrictNodes 1
```

### Circuit Configuration

#### Guard Node Selection
```
EntryNodes {us}
GuardLifetime "30 days"
```

#### Middle Node Configuration
```
MiddleNodes {de},{nl}
```

#### Exit Node Configuration
```
ExitNodes {gb}
ExitPolicy reject *:*
```

### Performance Tuning

#### Circuit Build Timeout
```
CircuitBuildTimeout 60
```

#### New Circuit Timeout
```
NewCircuitPeriod 30
```

#### Max Circuit Build Attempts
```
MaxCircuitDirtiness 300
```

### Bandwidth Configuration

#### Bandwidth Rate
```
BandwidthRate 1 MB
```

#### Bandwidth Burst
```
BandwidthBurst 2 MB
```

#### Relay Bandwidth
```
RelayBandwidthRate 100 KB
RelayBandwidthBurst 200 KB
```

### Bridge Configuration

#### Using Bridges
```
UseBridges 1
Bridge obfs4 192.0.2.1:443 1234567890ABCDEF cert=... iat-date=...
```

#### Bridge Directory
```
BridgeRelay 1
ServerTransportPlugin obfs4 exec /usr/bin/obfs4proxy managed
```

### Hidden Service Configuration

#### Create Hidden Service
```
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:8080
```

#### Multiple Hidden Services
```
HiddenServiceDir /var/lib/tor/hidden_service1/
HiddenServicePort 80 127.0.0.1:8080

HiddenServiceDir /var/lib/tor/hidden_service2/
HiddenServicePort 443 127.0.0.1:8443
```

---

## Configuration Templates

### Minimal torrc

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
```

### torrc with Logging

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
Log notice file /var/log/tor/notices.log
Log warn file /var/log/tor/warnings.log
```

### torrc with Transparent Proxy

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
TransPort 9040
DNSPort 5353
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
DataDirectory /var/lib/tor
```

### torrc with Exit Node Selection

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
ExitNodes {us}
StrictNodes 1
```

### torrc with Bridges

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
UseBridges 1
Bridge obfs4 192.0.2.1:443 1234567890ABCDEF cert=... iat-date=...
```

### torrc with Hidden Service

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:8080
```

---

## Configuration Management

### Using tor_custom_config.py

```bash
python tor_custom_config.py
```

This script:
1. Prompts for password
2. Generates hashed password
3. Creates torrc file
4. Sets permissions (600)
5. Sets ownership

### Using tor_auto_torrc_config.py

```bash
python tor_auto_torrc_config.py
```

This script:
1. Checks Tor installation
2. Installs Tor if missing
3. Sets up directories
4. Generates torrc
5. Restarts Tor service

### Manual Configuration

1. Create torrc file:
```bash
nano ~/.tor_config/torrc
```

2. Add configuration parameters

3. Set permissions:
```bash
chmod 600 ~/.tor_config/torrc
chmod 700 ~/.tor_config
```

4. Restart Tor:
```bash
sudo systemctl restart tor
```

---

## Configuration Validation

### Validate torrc Syntax

```bash
tor --verify-config -f /path/to/torrc
```

### Check Configuration

```bash
tor --defaults-torrc /path/to/torrc --verify-config
```

### Test Configuration

```bash
# Start Tor with custom config
tor -f /path/to/torrc

# Check if Tor is running
ps aux | grep tor
```

---

## Common Configuration Scenarios

### High Anonymity Configuration

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
ExitNodes {us},{de},{nl},{se},{ch}
StrictNodes 1
NewCircuitPeriod 60
MaxCircuitDirtiness 600
```

### High Performance Configuration

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
CircuitBuildTimeout 30
NewCircuitPeriod 15
MaxCircuitDirtiness 180
NumEntryGuards 8
```

### Low Latency Configuration

```
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
SocksPort 9050
DataDirectory /var/lib/tor
ExitNodes {nl},{de},{gb},{fr}
CircuitBuildTimeout 45
```

---

## Backup and Restore

### Backup Configuration

```bash
# Backup torrc
cp ~/.tor_config/torrc ~/.tor_config/torrc.backup

# Backup entire config directory
tar -czf tor_config_backup.tar.gz ~/.tor_config/
```

### Restore Configuration

```bash
# Restore torrc
cp ~/.tor_config/torrc.backup ~/.tor_config/torrc

# Restore entire directory
tar -xzf tor_config_backup.tar.gz -C ~/
```

---

## Troubleshooting Configuration

### Configuration Not Loading

1. Check file permissions:
```bash
ls -la ~/.tor_config/torrc
```

2. Validate syntax:
```bash
tor --verify-config -f ~/.tor_config/torrc
```

3. Check Tor logs:
```bash
tail -f /var/log/tor/notices.log
```

### Authentication Failing

1. Verify password hash:
```bash
tor --hash-password "your_password"
```

2. Check torrc authentication settings:
```bash
cat ~/.tor_config/torrc | grep HashedControlPassword
```

3. Try cookie authentication:
```bash
ls -la /run/tor/control.authcookie
```

### Port Already in Use

1. Check what's using the port:
```bash
netstat -tulnp | grep 9051
```

2. Kill conflicting process:
```bash
kill -9 <PID>
```

3. Change port in torrc:
```
ControlPort 9052
```

---

## Additional Resources

- [Home](Home) - Wiki home page
- [User Guide](User-Guide) - User guide
- [Installation](Installation) - Installation guide
- [Security](Security) - Security considerations
- [Tor Project Documentation](https://torproject.org/docs)

---

**Last Updated**: 2024-04-23
