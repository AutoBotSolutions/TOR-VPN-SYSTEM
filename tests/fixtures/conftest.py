"""
Pytest configuration and fixtures for Tor VPN System tests.
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import pytest
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture(scope="session")
def test_config_dir(tmp_path_factory):
    """Create a temporary directory for test configurations."""
    config_dir = tmp_path_factory.mktemp("tor_config")
    yield config_dir
    # Cleanup is automatic with tmp_path_factory


@pytest.fixture(scope="session")
def test_log_file(tmp_path_factory):
    """Create a temporary log file for testing."""
    log_file = tmp_path_factory.mktemp("logs") / "test.log"
    yield log_file


@pytest.fixture
def mock_tor_controller():
    """Create a mock Tor controller."""
    controller = MagicMock()
    controller.is_alive.return_value = True
    controller.get_version.return_value = "0.4.7.10"
    controller.get_info.return_value = {"version": "0.4.7.10"}
    controller.authenticate.return_value = True
    return controller


@pytest.fixture
def mock_subprocess():
    """Mock subprocess module."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "16:ABCD1234"
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_psutil():
    """Mock psutil module."""
    with patch('psutil.process_iter') as mock_iter:
        mock_process = MagicMock()
        mock_process.info = {"pid": 12345, "name": "tor"}
        mock_iter.return_value = [mock_process]
        yield mock_iter


@pytest.fixture
def sample_torrc_content():
    """Sample torrc configuration content."""
    return """ControlPort 9051
HashedControlPassword 16:ABCD1234EFGH5678
SocksPort 9050
DataDirectory /var/lib/tor
Log notice file /var/log/tor/notices.log
"""


@pytest.fixture
def sample_servers_dict():
    """Sample servers dictionary."""
    return {
        "us": {"name": "United States", "id": 1},
        "de": {"name": "Germany", "id": 2},
        "gb": {"name": "United Kingdom", "id": 3},
        "fr": {"name": "France", "id": 4},
        "jp": {"name": "Japan", "id": 5},
    }


@pytest.fixture
def mock_torrc_file(tmp_path):
    """Create a mock torrc file."""
    torrc_file = tmp_path / "torrc"
    torrc_content = """ControlPort 9051
HashedControlPassword 16:ABCD1234EFGH5678
SocksPort 9050
DataDirectory /var/lib/tor
"""
    torrc_file.write_text(torrc_content)
    return torrc_file


@pytest.fixture
def mock_auth_cookie(tmp_path):
    """Create a mock authentication cookie."""
    cookie_file = tmp_path / "control_auth_cookie"
    cookie_file.write_bytes(b"\x00" * 32)
    return cookie_file


@pytest.fixture
def mock_logger(tmp_path):
    """Create a mock logger with file handler."""
    log_file = tmp_path / "test.log"
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    yield logger
    
    logger.removeHandler(handler)
    handler.close()


@pytest.fixture
def temp_working_dir(tmp_path):
    """Create a temporary working directory."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)


@pytest.fixture
def mock_platform():
    """Mock platform module."""
    with patch('platform.system') as mock_system:
        with patch('platform.platform') as mock_platform_func:
            mock_system.return_value = "Linux"
            mock_platform_func.return_value = "Linux-6.1.0-32-amd64-x86_64-with-glibc2.36"
            yield {"system": "Linux", "platform": "Linux-6.1.0-32-amd64-x86_64-with-glibc2.36"}


@pytest.fixture
def mock_getpass():
    """Mock getpass module."""
    with patch('getpass.getpass') as mock_getpass_func:
        mock_getpass_func.return_value = "test_password"
        yield mock_getpass_func


@pytest.fixture
def mock_os_environ():
    """Mock os.environ with test values."""
    original_env = os.environ.copy()
    os.environ["TOR_PASSWORD"] = "test_password"
    os.environ["TOR_CONFIG_DIR"] = "/tmp/test_config"
    yield os.environ
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_file_permissions(tmp_path):
    """Create a file with specific permissions for testing."""
    test_file = tmp_path / "test_file"
    test_file.write_text("test content")
    test_file.chmod(0o600)
    return test_file


@pytest.fixture
def mock_tor_process():
    """Mock a Tor process."""
    process = MagicMock()
    process.pid = 12345
    process.name = "tor"
    process.status = "running"
    process.cpu_percent.return_value = 0.5
    process.memory_info.return_value = MagicMock(rss=50*1024*1024)  # 50 MB
    process.num_threads.return_value = 3
    return process


@pytest.fixture
def mock_systemd():
    """Mock systemd service."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "active"
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_init_d():
    """Mock init.d service."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_network_socket():
    """Mock network socket."""
    with patch('socket.create_connection') as mock_socket:
        mock_sock = MagicMock()
        mock_socket.close.return_value = None
        mock_socket.__enter__ = MagicMock(return_value=mock_sock)
        mock_socket.__exit__ = MagicMock(return_value=False)
        mock_socket.return_value = mock_sock
        yield mock_socket


@pytest.fixture
def mock_stem_controller():
    """Mock Stem Controller."""
    with patch('stem.control.Controller') as mock_controller_class:
        mock_controller = MagicMock()
        mock_controller.is_alive.return_value = True
        mock_controller.get_version.return_value = "0.4.7.10"
        mock_controller.authenticate.return_value = True
        mock_controller.get_circuits.return_value = []
        mock_controller.get_info.return_value = {}
        mock_controller.signal.return_value = None
        mock_controller.set_conf.return_value = None
        
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_controller)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_controller_class.from_port.return_value = mock_context
        
        yield mock_controller


@pytest.fixture
def mock_iptables():
    """Mock iptables commands."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def sample_password():
    """Sample password for testing."""
    return "TestPassword123!"


@pytest.fixture
def sample_hashed_password():
    """Sample hashed password for testing."""
    return "16:ABCD1234EFGH5678IJKL9012MNOP3456QRST7890"


@pytest.fixture
def sample_country_code():
    """Sample country code for testing."""
    return "us"


@pytest.fixture
def invalid_country_code():
    """Invalid country code for testing."""
    return "xyz"


@pytest.fixture
def sample_exit_node():
    """Sample exit node information."""
    return {
        "country": "us",
        "name": "United States",
        "ip": "192.0.2.1",
        "fingerprint": "ABCD1234EFGH5678",
    }


@pytest.fixture
def mock_circuit():
    """Mock Tor circuit."""
    circuit = MagicMock()
    circuit.id = 1
    circuit.purpose = "GENERAL"
    circuit.build_flags = []
    circuit.path = []
    circuit.state = "BUILT"
    return circuit


@pytest.fixture
def mock_stream():
    """Mock Tor stream."""
    stream = MagicMock()
    stream.id = 1
    stream.purpose = "DIR_FETCH"
    stream.target = "127.0.0.1:9050"
    stream.state = "NEW"
    return stream


@pytest.fixture
def mock_event():
    """Mock Tor event."""
    event = MagicMock()
    event.type = "CIRC"
    event.circuit_id = 1
    event.event_name = "CIRC"
    return event


@pytest.fixture
def test_environment():
    """Set up test environment variables."""
    original_env = os.environ.copy()
    
    os.environ["TOR_PASSWORD"] = "test_password"
    os.environ["TOR_CONFIG_DIR"] = "/tmp/test_tor_config"
    os.environ["HOME"] = "/tmp/test_home"
    
    yield os.environ
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def skip_if_no_tor():
    """Skip test if Tor is not available."""
    try:
        import subprocess
        result = subprocess.run(["tor", "--version"], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode != 0:
            pytest.skip("Tor is not installed")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pytest.skip("Tor is not available")


@pytest.fixture
def skip_if_no_root():
    """Skip test if not running as root."""
    if os.geteuid() != 0:
        pytest.skip("Test requires root privileges")


@pytest.fixture
def skip_if_no_gui():
    """Skip test if GUI environment is not available."""
    if os.environ.get("DISPLAY") is None:
        pytest.skip("GUI environment not available")


@pytest.fixture
def sample_config_dict():
    """Sample configuration dictionary."""
    return {
        "ControlPort": 9051,
        "SocksPort": 9050,
        "TransPort": 9040,
        "DNSPort": 5353,
        "HashedControlPassword": "16:ABCD1234EFGH5678",
        "DataDirectory": "/var/lib/tor",
        "Log": ["notice file /var/log/tor/notices.log"],
    }


@pytest.fixture
def sample_log_entries():
    """Sample log entries for testing."""
    return [
        "2024-01-15 10:30:45,123 - root - INFO - Initializing Tor configuration...",
        "2024-01-15 10:30:45,456 - root - DEBUG - Using precomputed hashed password",
        "2024-01-15 10:30:46,789 - root - INFO - Tor configuration initialized successfully.",
        "2024-01-15 10:30:47,012 - root - ERROR - Failed to connect to Tor",
    ]


@pytest.fixture
def mock_time():
    """Mock time module."""
    with patch('time.time') as mock_time_func:
        with patch('time.sleep') as mock_sleep:
            mock_time_func.return_value = 1234567890.123
            yield {"time": mock_time_func, "sleep": mock_sleep}


@pytest.fixture
def mock_signal():
    """Mock signal module."""
    with patch('signal.signal') as mock_signal_func:
        with patch('signal.SIGTERM') as mock_sigterm:
            with patch('signal.SIGINT') as mock_sigint:
                yield {
                    "signal": mock_signal_func,
                    "SIGTERM": mock_sigterm,
                    "SIGINT": mock_sigint,
                }


@pytest.fixture
def mock_shutil():
    """Mock shutil module."""
    with patch('shutil.chown') as mock_chown:
        with patch('shutil.copy') as mock_copy:
            yield {
                "chown": mock_chown,
                "copy": mock_copy,
            }


@pytest.fixture
def mock_os():
    """Mock os module."""
    with patch('os.chmod') as mock_chmod:
        with patch('os.chown') as mock_chown_os:
            with patch('os.path.exists') as mock_exists:
                mock_exists.return_value = True
                yield {
                    "chmod": mock_chmod,
                    "chown": mock_chown_os,
                    "exists": mock_exists,
                }


@pytest.fixture
def mock_pathlib():
    """Mock pathlib.Path."""
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        with patch('pathlib.Path.write_text') as mock_write:
            with patch('pathlib.Path.read_text') as mock_read:
                mock_read.return_value = "sample content"
                yield {
                    "mkdir": mock_mkdir,
                    "write_text": mock_write,
                    "read_text": mock_read,
                }


@pytest.fixture
def mock_requests():
    """Mock requests library."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Congratulations"
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_telnetlib():
    """Mock telnetlib library."""
    with patch('telnetlib.Telnet') as mock_telnet:
        mock_conn = MagicMock()
        mock_telnet.return_value = mock_conn
        yield mock_telnet


@pytest.fixture
def mock_zenity():
    """Mock zenity subprocess calls."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "us"
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_tor_binary():
    """Mock Tor binary path."""
    return "/usr/bin/tor"


@pytest.fixture
def mock_tor_data_dir(tmp_path):
    """Create a mock Tor data directory."""
    data_dir = tmp_path / "tor_data"
    data_dir.mkdir()
    (data_dir / "cached-certs").mkdir()
    return data_dir


@pytest.fixture
def mock_tor_log_dir(tmp_path):
    """Create a mock Tor log directory."""
    log_dir = tmp_path / "tor_logs"
    log_dir.mkdir()
    return log_dir


@pytest.fixture
def mock_hidden_service_dir(tmp_path):
    """Create a mock hidden service directory."""
    hs_dir = tmp_path / "hidden_service"
    hs_dir.mkdir()
    (hs_dir / "hostname").write_text("example.onion")
    (hs_dir / "private_key").write_text("private_key_content")
    return hs_dir


@pytest.fixture
def sample_bridge_config():
    """Sample bridge configuration."""
    return {
        "type": "obfs4",
        "address": "192.0.2.1",
        "port": 443,
        "fingerprint": "1234567890ABCDEF",
        "cert": "cert_data",
        "iat_date": "2024-01-15",
    }


@pytest.fixture
def sample_hidden_service_config():
    """Sample hidden service configuration."""
    return {
        "directory": "/var/lib/tor/hidden_service/",
        "port": 80,
        "target": "127.0.0.1:8080",
    }


@pytest.fixture
def sample_bandwidth_config():
    """Sample bandwidth configuration."""
    return {
        "rate": "1 MB",
        "burst": "2 MB",
        "relay_rate": "100 KB",
        "relay_burst": "200 KB",
    }


@pytest.fixture
def sample_circuit_config():
    """Sample circuit configuration."""
    return {
        "build_timeout": 60,
        "new_circuit_period": 30,
        "max_circuit_dirtiness": 300,
        "num_entry_guards": 8,
    }


@pytest.fixture
def sample_exit_node_config():
    """Sample exit node configuration."""
    return {
        "countries": ["us", "de", "gb"],
        "exclude": ["cn", "ru"],
        "strict": True,
    }


@pytest.fixture
def sample_guard_node_config():
    """Sample guard node configuration."""
    return {
        "countries": ["us"],
        "lifetime": "30 days",
    }


@pytest.fixture
def mock_tor_control_port():
    """Mock Tor control port."""
    return 9051


@pytest.fixture
def mock_tor_socks_port():
    """Mock Tor SOCKS port."""
    return 9050


@pytest.fixture
def mock_tor_transport_port():
    """Mock Tor transparent proxy port."""
    return 9040


@pytest.fixture
def mock_tor_dns_port():
    """Mock Tor DNS port."""
    return 5353


@pytest.fixture
def sample_tor_ports():
    """Sample Tor port configuration."""
    return {
        "control": 9051,
        "socks": 9050,
        "transport": 9040,
        "dns": 5353,
    }


@pytest.fixture
def mock_netstat():
    """Mock netstat output."""
    return """Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 127.0.0.1:9050          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9051          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9040          0.0.0.0:*               LISTEN
udp        0      0 127.0.0.1:5353          0.0.0.0:*               
"""


@pytest.fixture
def sample_iptables_rules():
    """Sample iptables rules."""
    return [
        "iptables -t nat -A OUTPUT -p tcp -d 10.192.0.0/10 -j REDIRECT --to-ports 9040",
        "iptables -t nat -A OUTPUT -p udp -d 10.192.0.0/10 -j REDIRECT --to-ports 9040",
        "iptables -t nat -A OUTPUT -p tcp -d 10.192.0.0/10 --dport 53 -j REDIRECT --to-ports 5353",
        "iptables -t filter -A OUTPUT -m owner --uid-owner debian-tor -j ACCEPT",
    ]


@pytest.fixture
def mock_system_info():
    """Sample system information."""
    return {
        "system": "Linux",
        "platform": "Linux-6.1.0-32-amd64-x86_64-with-glibc2.36",
        "python_version": "3.10.16",
        "tor_version": "0.4.7.10",
        "stem_version": "1.8.2",
    }


@pytest.fixture
def sample_diagnostic_report():
    """Sample diagnostic report."""
    return {
        "timestamp": "2024-01-15 10:30:45",
        "system_info": {
            "os": "Linux",
            "python": "3.10.16",
        },
        "tor_status": "running",
        "configuration": {
            "control_port": 9051,
            "socks_port": 9050,
        },
        "errors": [],
        "warnings": [],
    }


@pytest.fixture
def mock_uptime():
    """Mock system uptime."""
    return "123456.78"


@pytest.fixture
def mock_memory_info():
    """Mock memory information."""
    return {
        "total": 8589934592,  # 8 GB
        "available": 4294967296,  # 4 GB
        "used": 4294967296,  # 4 GB
        "percent": 50.0,
    }


@pytest.fixture
def mock_cpu_info():
    """Mock CPU information."""
    return {
        "percent": 25.5,
        "count": 4,
        "freq": 2400.0,
    }


@pytest.fixture
def mock_disk_info():
    """Mock disk information."""
    return {
        "total": 500000000000,  # 500 GB
        "used": 250000000000,  # 250 GB
        "free": 250000000000,  # 250 GB
        "percent": 50.0,
    }


@pytest.fixture
def sample_network_test_result():
    """Sample network test result."""
    return {
        "connection": True,
        "latency": 0.5,
        "exit_ip": "192.0.2.1",
        "country": "us",
        "errors": [],
    }


@pytest.fixture
def sample_latency_measurement():
    """Sample latency measurements."""
    return [0.45, 0.52, 0.48, 0.50, 0.47]


@pytest.fixture
def sample_circuit_info():
    """Sample circuit information."""
    return {
        "circuit_id": 1,
        "purpose": "GENERAL",
        "state": "BUILT",
        "path": [
            {"nickname": "Guard1", "fingerprint": "ABCD1234"},
            {"nickname": "Middle1", "fingerprint": "EFGH5678"},
            {"nickname": "Exit1", "fingerprint": "IJKL9012"},
        ],
        "build_flags": [],
    }


@pytest.fixture
def sample_stream_info():
    """Sample stream information."""
    return {
        "stream_id": 1,
        "purpose": "DIR_FETCH",
        "target": "127.0.0.1:9050",
        "state": "SUCCEEDED",
        "circuit_id": 1,
    }


@pytest.fixture
def sample_tor_metrics():
    """Sample Tor metrics."""
    return {
        "uptime": 1234567,
        "circuits_built": 100,
        "streams_succeeded": 500,
        "streams_failed": 5,
        "bytes_read": 10000000,
        "bytes_written": 5000000,
    }


@pytest.fixture
def mock_tor_status():
    """Mock Tor status."""
    return {
        "running": True,
        "pid": 12345,
        "uptime": 3600,
        "version": "0.4.7.10",
    }


@pytest.fixture
def sample_error_message():
    """Sample error message."""
    return "Failed to connect to Tor control port: Connection refused"


@pytest.fixture
def sample_warning_message():
    """Sample warning message."""
    return "Tor is running as root, which is not recommended"


@pytest.fixture
def sample_info_message():
    """Sample info message."""
    "Tor configuration initialized successfully"


@pytest.fixture
def sample_debug_message():
    """Sample debug message."""
    "Using precomputed hashed password: 16:ABCD1234"


@pytest.fixture
def mock_log_levels():
    """Mock log levels."""
    return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


@pytest.fixture
def sample_log_format():
    """Sample log format."""
    return "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@pytest.fixture
def sample_log_rotation_config():
    """Sample log rotation configuration."""
    return {
        "max_bytes": 1_000_000,
        "backup_count": 5,
        "encoding": "utf-8",
    }


@pytest.fixture
def mock_file_handler(tmp_path):
    """Mock file handler for logging."""
    log_file = tmp_path / "test.log"
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return handler


@pytest.fixture
def mock_stream_handler():
    """Mock stream handler for logging."""
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return handler


@pytest.fixture
def sample_environment_variables():
    """Sample environment variables for testing."""
    return {
        "TOR_PASSWORD": "test_password",
        "TOR_CONFIG_DIR": "/tmp/test_config",
        "TOR_DATA_DIR": "/tmp/test_data",
        "TOR_LOG_DIR": "/tmp/test_logs",
    }


@pytest.fixture
def mock_apt():
    """Mock apt-get commands."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_dnf():
    """Mock dnf commands."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_pacman():
    """Mock pacman commands."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_brew():
    """Mock brew commands."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_systemctl():
    """Mock systemctl commands."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "active"
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_service():
    """Mock service commands."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def sample_package_info():
    """Sample package information."""
    return {
        "name": "tor",
        "version": "0.4.7.10",
        "installed": True,
        "dependencies": ["libssl", "zlib"],
    }


@pytest.fixture
def sample_dependency_info():
    """Sample dependency information."""
    return {
        "stem": {
            "version": "1.8.2",
            "installed": True,
            "required": True,
        },
        "psutil": {
            "version": "7.0.0",
            "installed": True,
            "required": True,
        },
    }


@pytest.fixture
def mock_version_info():
    """Mock version information."""
    return {
        "tor": "0.4.7.10",
        "stem": "1.8.2",
        "psutil": "7.0.0",
        "python": "3.10.16",
    }


@pytest.fixture
def sample_changelog_entry():
    """Sample changelog entry."""
    return {
        "version": "1.0.0",
        "date": "2024-01-15",
        "changes": [
            "Initial release",
            "Added GUI application",
            "Added configuration management",
        ],
    }


@pytest.fixture
def sample_release_notes():
    """Sample release notes."""
    return """
## Version 1.0.0 - 2024-01-15

### Added
- Initial release of Tor VPN System
- GUI application with country selection
- Configuration management tools
- Diagnostic and repair utilities
- Network testing tools

### Changed
- N/A

### Fixed
- N/A

### Security
- Documented known security issues
"""
