# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Tor VPN System.

## Table of Contents

- [Common Issues](#common-issues)
- [Tor Service Issues](#tor-service-issues)
- [Connection Issues](#connection-issues)
- [Authentication Issues](#authentication-issues)
- [Configuration Issues](#configuration-issues)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Getting Help](#getting-help)

---

## Common Issues

### Tor Won't Start

**Symptoms:**
- Tor service fails to start
- Error messages about port conflicts
- Tor process not found

**Solutions:**

1. Check if Tor is installed:
```bash
tor --version
```

2. Check Tor service status:
```bash
sudo systemctl status tor  # Linux
ps aux | grep tor          # macOS
tasklist | findstr tor    # Windows
```

3. Check for port conflicts:
```bash
netstat -tulnp | grep 9050
netstat -tulnp | grep 9051
```

4. Check Tor logs:
```bash
sudo journalctl -xe | grep -i tor  # Linux
tail -f /usr/local/var/log/tor/log  # macOS
# Check Tor log directory on Windows
```

5. Restart Tor:
```bash
sudo systemctl restart tor  # Linux
sudo /etc/init.d/tor restart # init.d systems
```

### Control Port Not Accessible

**Symptoms:**
- Cannot connect to control port
- Authentication failures
- "Connection refused" errors

**Solutions:**

1. Check if control port is listening:
```bash
netstat -tulnp | grep 9051
```

2. Verify torrc has ControlPort:
```bash
cat ~/.tor_config/torrc | grep ControlPort
```

3. Check firewall:
```bash
sudo ufw status  # Linux
# Check Windows Firewall settings
```

4. Test with telnet:
```bash
telnet 127.0.0.1 9051
```

5. Check Tor is running with correct config:
```bash
ps aux | grep "tor -f"
```

### Permission Errors

**Symptoms:**
- "Permission denied" errors
- Cannot write to config files
- Cannot modify system settings

**Solutions:**

1. Run with sudo:
```bash
sudo python tor_vpn_beta.py
sudo python tor_auto_torrc_config.py
```

2. Check file permissions:
```bash
ls -la ~/.tor_config/torrc
```

3. Fix permissions:
```bash
chmod 600 ~/.tor_config/torrc
chmod 700 ~/.tor_config
```

4. Fix ownership:
```bash
sudo chown -R $USER:$USER ~/.tor_config
```

### GUI Won't Open

**Symptoms:**
- GUI application doesn't launch
- tkinter import errors
- Display errors

**Solutions:**

1. Install tkinter:
```bash
sudo apt install python3-tk  # Ubuntu/Debian
```

2. Check display environment:
```bash
echo $DISPLAY
```

3. Try running with explicit display:
```bash
export DISPLAY=:0
python tor_vpn_beta.py
```

4. Check for X11/Wayland issues:
```bash
# For Wayland, try X11 backend
export GDK_BACKEND=x11
python tor_vpn_beta.py
```

---

## Tor Service Issues

### Tor Service Not Starting

**Diagnosis:**

```bash
# Check service status
sudo systemctl status tor

# Check for errors
sudo journalctl -xe | grep -i tor

# Try manual start
tor -f /path/to/torrc
```

**Common Causes and Solutions:**

1. **Invalid torrc syntax**
```bash
# Validate configuration
tor --verify-config -f /path/to/torrc
```

2. **Missing directories**
```bash
# Create data directory
sudo mkdir -p /var/lib/tor
sudo chown debian-tor:debian-tor /var/lib/tor
```

3. **Port conflicts**
```bash
# Kill conflicting process
sudo kill -9 <PID>
# Or change port in torrc
```

4. **Permission issues**
```bash
# Fix ownership
sudo chown -R debian-tor:debian-tor /var/lib/tor
```

### Tor Service Keeps Crashing

**Diagnosis:**

```bash
# Check crash logs
sudo journalctl -u tor -n 100

# Check memory usage
ps aux | grep tor
```

**Solutions:**

1. **Memory issues**
```bash
# Reduce circuit count in torrc
MaxCircuitDirtiness 300
```

2. **Disk space issues**
```bash
# Check available space
df -h
# Clean old data
rm -rf /var/lib/tor/cached-certs
```

3. **Configuration errors**
```bash
# Use default configuration
sudo mv /etc/tor/torrc /etc/tor/torrc.backup
sudo systemctl restart tor
```

---

## Connection Issues

### Cannot Connect to Tor

**Symptoms:**
- Connection timeouts
- "Network unreachable" errors
- Cannot establish circuits

**Solutions:**

1. Run diagnostic tool:
```bash
python tor_diagnostic_repair.py
```

2. Test Tor connection:
```bash
python tor_network_test.py
```

3. Check network connectivity:
```bash
ping -c 4 8.8.8.8
```

4. Check firewall:
```bash
sudo iptables -L -n
sudo ufw status
```

5. Verify Tor is working:
```bash
curl --socks5 127.0.0.1:9050 https://check.torproject.org
```

### Slow Connection Speed

**Symptoms:**
- High latency
- Slow page loads
- Poor performance

**Solutions:**

1. Test with different exit nodes:
```bash
# Try different countries
connect_to_tor("nl")  # Netherlands
connect_to_tor("de")  # Germany
```

2. Check exit node performance:
```bash
# Run network test
python tor_network_test.py
# Check latency in output
```

3. Reduce circuit rebuilds:
```bash
# Add to torrc
NewCircuitPeriod 60
```

4. Use nearby exit nodes:
```bash
# Select geographically close countries
```

### Connection Drops Frequently

**Symptoms:**
- Connection lost intermittently
- Frequent reconnections needed

**Solutions:**

1. Check internet stability:
```bash
ping -c 100 8.8.8.8
```

2. Increase circuit lifetime:
```bash
# Add to torrc
MaxCircuitDirtiness 600
```

3. Use stable guard nodes:
```bash
# Add to torrc
EntryNodes {us}
GuardLifetime "30 days"
```

---

## Authentication Issues

### Password Authentication Fails

**Symptoms:**
- "Authentication failed" errors
- Cannot connect to control port

**Solutions:**

1. Verify password hash:
```bash
tor --hash-password "your_password"
```

2. Check torrc authentication:
```bash
cat ~/.tor_config/torrc | grep HashedControlPassword
```

3. Test authentication:
```python
from stem.control import Controller

try:
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password")
        print("Authentication successful")
except Exception as e:
    print(f"Authentication failed: {e}")
```

4. Regenerate password:
```bash
python tor_custom_config.py
```

### Cookie Authentication Fails

**Symptoms:**
- Cookie authentication errors
- Cannot find auth cookie

**Solutions:**

1. Check cookie file exists:
```bash
ls -la /run/tor/control.authcookie
# or
ls -la /var/lib/tor/control_auth_cookie
```

2. Check cookie permissions:
```bash
ls -la /run/tor/control.authcookie
# Should be readable by Tor user
```

3. Enable cookie authentication:
```bash
# Add to torrc
CookieAuthentication 1
```

4. Restart Tor:
```bash
sudo systemctl restart tor
```

---

## Configuration Issues

### Invalid torrc Syntax

**Symptoms:**
- Tor won't start
- Syntax errors in logs

**Solutions:**

1. Validate configuration:
```bash
tor --verify-config -f /path/to/torrc
```

2. Check for common errors:
- Missing quotes
- Invalid parameter names
- Typos in country codes
- Incorrect port numbers

3. Use configuration template:
```bash
# Start with known-good configuration
cp /etc/tor/torrc ~/.tor_config/torrc.backup
```

### Configuration Not Applied

**Symptoms:**
- Changes not taking effect
- Old settings still active

**Solutions:**

1. Restart Tor:
```bash
sudo systemctl restart tor
```

2. Check which config is being used:
```bash
ps aux | grep tor
# Look for -f flag
```

3. Verify config file location:
```bash
cat ~/.tor_config/torrc
```

4. Check for multiple config files:
```bash
# Tor might be using system config instead
sudo systemctl cat tor
```

---

## Performance Issues

### High CPU Usage

**Symptoms:**
- Tor using excessive CPU
- System slowdown

**Solutions:**

1. Monitor Tor CPU usage:
```bash
top -p $(pgrep tor)
```

2. Reduce circuit count:
```bash
# Add to torrc
MaxCircuitDirtiness 300
```

3. Disable unused features:
```bash
# Comment out unused parameters in torrc
```

4. Check for infinite loops in custom scripts

### High Memory Usage

**Symptoms:**
- Tor using excessive memory
- Out of memory errors

**Solutions:**

1. Monitor memory usage:
```bash
ps aux | grep tor
```

2. Reduce circuit count:
```bash
# Add to torrc
MaxCircuitDirtiness 300
```

3. Clear Tor cache:
```bash
rm -rf /var/lib/tor/cached-certs
```

4. Restart Tor:
```bash
sudo systemctl restart tor
```

### High Disk Usage

**Symptoms:**
- Tor using excessive disk space
- Logs growing too large

**Solutions:**

1. Check disk usage:
```bash
du -sh /var/lib/tor
du -sh /var/log/tor
```

2. Configure log rotation:
```bash
# Add to torrc
Log notice file /var/log/tor/notices.log
Log warn file /var/log/tor/warnings.log
```

3. Clean old logs:
```bash
sudo rm /var/log/tor/notices.log.*
sudo rm /var/log/tor/warnings.log.*
```

4. Limit data directory size:
```bash
# Add to torrc
MaxMemInQueues 2 GB
```

---

## Platform-Specific Issues

### Linux Issues

#### systemd Issues

**Symptoms:**
- systemd service fails
- Cannot manage Tor with systemctl

**Solutions:**

1. Check systemd status:
```bash
systemctl is-system-running
```

2. Use init.d fallback:
```bash
sudo /etc/init.d/tor restart
```

3. Check service file:
```bash
systemctl cat tor
```

#### iptables Issues

**Symptoms:**
- iptables rules not applying
- Transparent proxy not working

**Solutions:**

1. Check iptables rules:
```bash
sudo iptables -L -n
sudo iptables -t nat -L -n
```

2. Flush and reapply:
```bash
sudo iptables -F
sudo iptables -t nat -F
# Re-run setup script
sudo python tor_route_traffic_setup.py
```

3. Check for other firewall rules:
```bash
sudo ufw status
```

### macOS Issues

#### Homebrew Installation Issues

**Symptoms:**
- Cannot install Tor via Homebrew
- Brew commands fail

**Solutions:**

1. Update Homebrew:
```bash
brew update
brew doctor
```

2. Clean and reinstall:
```bash
brew uninstall tor
brew install tor
```

#### Permission Issues

**Symptoms:**
- Cannot write to config directories
- Permission denied errors

**Solutions:**

1. Fix ownership:
```bash
sudo chown -R $USER:staff ~/Library/Application\ Support/Tor
```

2. Check permissions:
```bash
ls -la ~/Library/Application\ Support/Tor
```

### Windows Issues

#### Path Issues

**Symptoms:**
- Cannot find Tor executable
- PATH not set correctly

**Solutions:**

1. Add Tor to PATH:
- System Properties > Environment Variables
- Add `C:\Tor` to PATH

2. Use full path:
```cmd
C:\Tor\tor.exe -f C:\Tor\torrc
```

#### Service Issues

**Symptoms:**
- Tor service won't start
- Service management issues

**Solutions:**

1. Run Tor manually:
```cmd
tor -f %APPDATA%\tor\torrc
```

2. Check Windows Event Viewer for errors

3. Use Task Scheduler instead of service

---

## Diagnostic Tools

### Built-in Diagnostic Tool

Run the comprehensive diagnostic tool:

```bash
python tor_diagnostic_repair.py
```

This tool:
- Detects init system
- Validates configuration
- Checks Tor process
- Attempts repair
- Collects diagnostics

### Network Test Tool

Test Tor connectivity:

```bash
python tor_network_test.py
```

This tool:
- Checks Tor service
- Tests control port
- Measures latency
- Detects exit IP
- Shows circuit info

### Manual Diagnostics

#### Check Tor Version
```bash
tor --version
```

#### Check Tor Configuration
```bash
tor --verify-config
```

#### Check Tor Process
```bash
ps aux | grep tor
```

#### Check Tor Ports
```bash
netstat -tulnp | grep tor
```

#### Check Tor Logs
```bash
sudo journalctl -u tor -f
tail -f /var/log/tor/notices.log
```

---

## Getting Help

### Before Asking for Help

1. **Check documentation**
   - Review [Home](Home)
   - Check [User Guide](User-Guide)
   - Review [Configuration](Configuration)

2. **Run diagnostics**
   ```bash
   python tor_diagnostic_repair.py
   python tor_network_test.py
   ```

3. **Check logs**
   - Tor logs
   - Application logs
   - System logs

4. **Search existing issues**
   - GitHub Issues
   - Project discussions

### When Creating an Issue

Include:

1. **System Information**
   - OS and version
   - Python version
   - Tor version

2. **Error Messages**
   - Full error output
   - Stack traces
   - Log excerpts

3. **Steps to Reproduce**
   - What you were doing
   - What happened
   - Expected vs actual behavior

4. **Configuration**
   - torrc file (sanitized)
   - Environment variables
   - Command used

5. **Diagnostic Output**
   - Output from diagnostic tools
   - Network test results

### Community Resources

- **GitHub Issues**: [Report issues](https://github.com/your-username/tor_vpn/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/your-username/tor_vpn/discussions)
- **Documentation**: [docs/INDEX.md](../docs/INDEX.md)

---

## Common Error Messages

### "Control port not accessible"

**Cause**: Tor not running or control port blocked

**Solution**:
```bash
sudo systemctl start tor
sudo ufw allow 9051/tcp
```

### "Authentication failed"

**Cause**: Incorrect password or authentication method

**Solution**:
```bash
# Regenerate password
python tor_custom_config.py
# Or use cookie authentication
```

### "Port already in use"

**Cause**: Another process using the port

**Solution**:
```bash
# Find and kill process
sudo lsof -i :9051
sudo kill -9 <PID>
```

### "Permission denied"

**Cause**: Insufficient permissions

**Solution**:
```bash
# Run with sudo
sudo python <script>
# Or fix permissions
chmod 600 ~/.tor_config/torrc
```

### "Tor not found"

**Cause**: Tor not installed or not in PATH

**Solution**:
```bash
# Install Tor
sudo apt install tor
# Or add to PATH
export PATH=$PATH:/path/to/tor
```

---

## Additional Resources

- [Home](Home) - Wiki home page
- [Installation](Installation) - Installation guide
- [User Guide](User-Guide) - User guide
- [Configuration](Configuration) - Configuration options
- [Security](Security) - Security considerations

---

**Last Updated**: 2024-04-23
