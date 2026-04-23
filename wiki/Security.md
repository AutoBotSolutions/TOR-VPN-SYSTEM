# Security Guide

This guide covers security considerations, best practices, and recommendations for the Tor VPN System.

## Table of Contents

- [Security Overview](#security-overview)
- [Current Security Issues](#current-security-issues)
- [Security Best Practices](#security-best-practices)
- [Authentication Security](#authentication-security)
- [File and Permission Security](#file-and-permission-security)
- [Network Security](#network-security)
- [Logging Security](#logging-security)
- [Development Security](#development-security)
- [Security Auditing](#security-auditing)

---

## Security Overview

The Tor VPN System provides tools for managing Tor connections, but like any software that handles network traffic and system configuration, it requires careful security considerations.

### Threat Model

The system is designed for:
- **Privacy**: Protecting user identity and location
- **Anonymity**: Hiding traffic patterns and destinations
- **Security**: Preventing unauthorized access to Tor controls

### Security Goals

1. Protect Tor control port access
2. Secure configuration files
3. Prevent unauthorized system modifications
4. Protect sensitive data (passwords, logs)
5. Ensure secure communication with Tor

---

## Current Security Issues

⚠️ **Known Security Concerns in Current Version:**

### Hardcoded Passwords

Several scripts contain hardcoded passwords:
- `tor_vpn_beta.py`: `DEFAULT_PASSWORD` constant
- `tor_auto_torrc_config.py`: `DEFAULT_CONTROL_PASSWORD` constant
- Precomputed hashed passwords in configuration files

**Risk:** If source code is exposed, passwords are compromised.

**Mitigation:**
- Remove hardcoded passwords
- Use environment variables
- Implement proper key management
- Use password managers or keyring libraries

### Password Handling

Some scripts pass passwords via command-line or store in variables:
- Shell scripts store passwords in shell variables
- Some Python scripts pass passwords via stdin
- No encryption at rest

**Risk:** Passwords may be exposed in process lists or memory dumps.

**Mitigation:**
- Use secure password input methods
- Implement proper memory handling
- Use keyring libraries for storage
- Avoid password in command-line arguments

### Privilege Management

Many scripts require root/sudo privileges:
- Limited privilege validation
- No privilege dropping after operations
- Some operations run with unnecessary privileges

**Risk:** Privilege escalation if code is compromised.

**Mitigation:**
- Implement principle of least privilege
- Drop privileges after operations
- Validate sudo access properly
- Use capability-based security where possible

### Input Validation

Limited input validation in some functions:
- Country codes not always validated
- File paths not sanitized
- User input not properly escaped

**Risk:** Command injection or path traversal attacks.

**Mitigation:**
- Implement comprehensive input validation
- Sanitize all user inputs
- Use parameterized queries
- Validate file paths

### Logging Security

Logs may contain sensitive information:
- Passwords may be logged in debug mode
- IP addresses and connection details
- System information

**Risk:** Sensitive data exposure in log files.

**Mitigation:**
- Redact sensitive data from logs
- Implement log rotation and secure storage
- Restrict log file permissions
- Use structured logging with controlled verbosity

---

## Security Best Practices

### Immediate Actions

#### 1. Change Default Passwords

Before using the system in production:

```python
# Use environment variables
import os
password = os.environ.get("TOR_PASSWORD")
if not password:
    raise ValueError("TOR_PASSWORD environment variable not set")
```

#### 2. Secure Configuration Files

```bash
# Set proper permissions
chmod 600 ~/.tor_config/torrc
chmod 700 ~/.tor_config

# Verify permissions
ls -la ~/.tor_config/torrc
```

#### 3. Restrict Log Access

```bash
# Set log file permissions
chmod 640 /var/log/tor/*.log

# Restrict log directory
chmod 750 /var/log/tor
```

### Operational Security

#### 1. Use Strong Passwords

Generate strong, unique passwords for Tor control:

```bash
# Generate secure password
openssl rand -base64 32

# Hash the password
tor --hash-password "your_secure_password"
```

#### 2. Regular Updates

Keep Tor and dependencies updated:

```bash
# Update Tor
sudo apt update && sudo apt install tor

# Update Python dependencies
pip install --upgrade -r requirements.txt
```

#### 3. Monitor Logs

Regularly review logs for suspicious activity:

```bash
# Monitor Tor logs
tail -f /var/log/tor/notices.log

# Monitor application logs
tail -f vpn_app_advanced.log
```

#### 4. Network Security

Configure firewall rules:

```bash
# Allow only necessary ports
sudo ufw allow 9050/tcp  # SOCKS proxy
sudo ufw allow 9051/tcp  # Control port
sudo ufw deny incoming
sudo ufw enable
```

---

## Authentication Security

### Password-Based Authentication

#### Current Implementation

The system uses hashed passwords in torrc:

```
HashedControlPassword 16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD
```

#### Best Practices

1. **Generate Strong Hashes**
```bash
# Use strong password
tor --hash-password "your_very_strong_password_here"
```

2. **Rotate Passwords Regularly**
```bash
# Every 30-90 days
# Generate new password
# Update torrc
# Restart Tor
```

3. **Use Environment Variables**
```python
import os
from stem.control import Controller

password = os.environ.get("TOR_PASSWORD")
with Controller.from_port(port=9051) as controller:
    controller.authenticate(password=password)
```

### Cookie-Based Authentication

#### Current Implementation

Cookie authentication uses a shared secret file:

```
CookieAuthentication 1
```

#### Best Practices

1. **Secure Cookie File**
```bash
# Set restrictive permissions
chmod 600 /run/tor/control.authcookie
```

2. **Use in Trusted Environments Only**
Cookie authentication is suitable for:
- Local development
- Trusted servers
- Automated scripts

3. **Regular Cookie Rotation**
```bash
# Delete old cookie
rm /run/tor/control.authcookie
# Restart Tor to generate new cookie
sudo systemctl restart tor
```

### Multi-Factor Authentication

Currently not implemented. Future enhancement:

```python
# Example: Add MFA support
import pyotp

def authenticate_with_mfa(controller, password, totp_code):
    """Authenticate with password and TOTP code."""
    # Verify TOTP
    totp = pyotp.TOTP("your_secret_key")
    if not totp.verify(totp_code):
        raise AuthenticationError("Invalid TOTP code")
    
    # Authenticate with password
    controller.authenticate(password=password)
```

---

## File and Permission Security

### Configuration Files

#### Secure torrc

```bash
# Create secure torrc
umask 077
cat > ~/.tor_config/torrc << EOF
ControlPort 9051
HashedControlPassword 16:YOUR_HASHED_PASSWORD
EOF

# Set permissions
chmod 600 ~/.tor_config/torrc
```

#### Directory Permissions

```bash
# Configuration directory
chmod 700 ~/.tor_config

# Data directory
chmod 700 /var/lib/tor

# Log directory
chmod 750 /var/log/tor
```

#### Ownership

```bash
# Set appropriate ownership
sudo chown -R debian-tor:debian-tor /var/lib/tor
sudo chown -R $USER:$USER ~/.tor_config
```

### Log Files

#### Secure Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Secure log handler
handler = RotatingFileHandler(
    "secure.log",
    maxBytes=1_000_000,
    backupCount=5
)
handler.setLevel(logging.INFO)

# Set permissions
import os
os.chmod("secure.log", 0o640)
```

#### Log Redaction

```python
def redact_sensitive_data(message):
    """Redact sensitive data from log messages."""
    import re
    # Redact passwords
    message = re.sub(r'password["\s:]+["\s]+[\w]+', 'password="***"', message)
    # Redact IPs (optional)
    message = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '***.***.***.***', message)
    return message
```

---

## Network Security

### Control Port Security

#### Restrict Access

```bash
# Only allow localhost
sudo iptables -A INPUT -p tcp -s 127.0.0.1 --dport 9051 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9051 -j DROP
```

#### Use Unix Domain Sockets (Future Enhancement)

```python
# More secure than TCP
# Configure in torrc
ControlSocket /run/tor/control.sock
CookieAuthentication 1
```

### SOCKS Proxy Security

#### Restrict SOCKS Port

```bash
# Only allow localhost
sudo iptables -A INPUT -p tcp -s 127.0.0.1 --dport 9050 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9050 -j DROP
```

#### Application-Level Restrictions

Only allow trusted applications to use the proxy:

```python
# In application code
import os
os.environ["HTTP_PROXY"] = "socks5h://127.0.0.1:9050"
os.environ["HTTPS_PROXY"] = "socks5h://127.0.0.1:9050"
```

### Transparent Proxy Security

⚠️ **Critical Warning:** Transparent proxy routes ALL traffic through Tor.

#### Audit iptables Rules

```bash
# Review current rules
sudo iptables -L -n
sudo iptables -t nat -L -n

# Save rules for audit
sudo iptables-save > /tmp/iptables-backup
```

#### Disable When Not Needed

```bash
# Flush rules when not using transparent proxy
sudo iptables -F
sudo iptables -t nat -F
```

---

## Logging Security

### Log File Protection

#### Set Appropriate Permissions

```bash
# Application logs
chmod 640 vpn_app_advanced.log

# Tor logs
chmod 640 /var/log/tor/*.log

# Diagnostic logs
chmod 600 diagnostics/*
```

#### Log Rotation

```python
from logging.handlers import RotatingFileHandler

# Rotate logs to prevent unlimited growth
handler = RotatingFileHandler(
    "app.log",
    maxBytes=10_000_000,  # 10 MB
    backupCount=5
)
```

### Log Content Security

#### Sensitive Data in Logs

Avoid logging:
- Passwords (even hashed)
- Personal information
- Full IP addresses
- User credentials

#### Structured Logging

```python
import logging
import json

class SecureFormatter(logging.Formatter):
    def format(self, record):
        # Remove sensitive fields
        if hasattr(record, 'password'):
            record.password = "***REDACTED***"
        return super().format(record)
```

---

## Development Security

### Secure Coding Practices

#### Input Validation

```python
def validate_country_code(code):
    """Validate and sanitize country code."""
    if not isinstance(code, str):
        raise TypeError("Country code must be a string")
    
    if len(code) != 2:
        raise ValueError("Country code must be 2 characters")
    
    if not code.isalpha():
        raise ValueError("Country code must contain only letters")
    
    return code.lower()
```

#### Output Encoding

```python
import html

def safe_output(text):
    """Safely encode output."""
    return html.escape(text)
```

#### SQL Injection Prevention (if using database)

```python
# Use parameterized queries
cursor.execute(
    "SELECT * FROM users WHERE username = %s",
    (username,)
)
```

### Dependency Security

#### Scan Dependencies

```bash
# Check for known vulnerabilities
pip install safety
safety check

# Check for outdated packages
pip install pip-audit
pip-audit
```

#### Keep Dependencies Updated

```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Check for security updates
pip list --outdated
```

### Code Review Checklist

- [ ] No hardcoded passwords or secrets
- [ ] Input validation on all user inputs
- [ ] Output encoding on all outputs
- [ ] Proper error handling
- [ ] Secure file permissions
- [ ] No sensitive data in logs
- [ ] Dependencies are up-to-date
- [ ] No known vulnerabilities in dependencies

---

## Security Auditing

### Automated Security Scanning

#### Bandit (Python Security)

```bash
pip install bandit
bandit -r .
```

#### Safety (Dependency Scanning)

```bash
pip install safety
safety check -r requirements.txt
```

#### TruffleHog (Secret Scanning)

```bash
pip install trufflehog
trufflehog --regex --entropy=False /path/to/repo
```

### Manual Security Review

#### Review Areas

1. **Authentication**
   - Password storage
   - Authentication methods
   - Session management

2. **Authorization**
   - Privilege checks
   - Access controls
   - Resource limits

3. **Data Protection**
   - Encryption at rest
   - Encryption in transit
   - Data retention

4. **Logging**
   - Log content
   - Log access
   - Log retention

### Penetration Testing

#### Test Areas

1. **Control Port**
   - Try unauthorized access
   - Test authentication bypass
   - Attempt privilege escalation

2. **Configuration**
   - Test file permission bypass
   - Attempt configuration injection
   - Test path traversal

3. **Network**
   - Test port scanning
   - Attempt man-in-the-middle
   - Test DNS poisoning

---

## Security Incident Response

### Detecting Security Incidents

#### Signs of Compromise

- Unexpected Tor behavior
- Configuration changes without authorization
- Failed authentication attempts in logs
- Unknown processes or connections
- Log file tampering

#### Monitoring Commands

```bash
# Check for unauthorized Tor processes
ps aux | grep tor

# Check for suspicious network connections
netstat -tulnp | grep 9051

# Check for file modifications
find ~/.tor_config -mtime -1

# Check authentication attempts
grep "Authentication" /var/log/tor/notices.log
```

### Response Steps

1. **Isolate System**
   ```bash
   # Stop Tor service
   sudo systemctl stop tor
   
   # Disconnect from network if needed
   ```

2. **Preserve Evidence**
   ```bash
   # Copy logs
   cp /var/log/tor/notices.log ~/incident-evidence/
   
   # Copy configuration
   cp ~/.tor_config/torrc ~/incident-evidence/
   ```

3. **Investigate**
   ```bash
   # Review logs for suspicious activity
   grep -i "error\|fail\|unauthorized" /var/log/tor/notices.log
   
   # Check for configuration changes
   git diff ~/.tor_config/torrc
   ```

4. **Remediate**
   ```bash
   # Change all passwords
   # Update configuration
   # Apply security patches
   # Restart services
   ```

5. **Document**
   - Document incident timeline
   - Record actions taken
   - Identify lessons learned

---

## Additional Resources

- [Home](Home) - Wiki home page
- [Configuration](Configuration) - Configuration options
- [Troubleshooting](Troubleshooting) - Common issues
- [Tor Project Security](https://torproject.org/docs/security) - Tor security documentation
- [Stem Security](https://stem.torproject.org) - Stem library security

---

## Security Checklist

### Before Deployment

- [ ] Remove all hardcoded passwords
- [ ] Implement environment variable usage
- [ ] Set appropriate file permissions
- [ ] Configure firewall rules
- [ ] Enable log rotation
- [ ] Review and redact sensitive logs
- [ ] Update all dependencies
- [ ] Run security scans
- [ ] Test authentication methods
- [ ] Document security procedures

### Ongoing Maintenance

- [ ] Regularly update Tor and dependencies
- [ ] Rotate passwords regularly
- [ ] Monitor logs for suspicious activity
- [ ] Review access logs
- [ ] Perform security audits
- [ ] Update security documentation
- [ ] Train users on security best practices

---

**Last Updated**: 2024-04-23
