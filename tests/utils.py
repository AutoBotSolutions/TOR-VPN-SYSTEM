"""
Test utilities for Tor VPN System tests.
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import subprocess
import time


class TestHelper:
    """Helper class for common test operations."""
    
    @staticmethod
    def create_temp_directory():
        """Create a temporary directory for testing."""
        return tempfile.mkdtemp()
    
    @staticmethod
    def cleanup_temp_directory(directory):
        """Clean up a temporary directory."""
        if os.path.exists(directory):
            shutil.rmtree(directory)
    
    @staticmethod
    def create_temp_file(content, suffix=".txt"):
        """Create a temporary file with content."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    @staticmethod
    def cleanup_temp_file(path):
        """Clean up a temporary file."""
        if os.path.exists(path):
            os.remove(path)
    
    @staticmethod
    def mock_subprocess_run(return_value=0, stdout="", stderr=""):
        """Create a mock subprocess.run."""
        mock_result = Mock()
        mock_result.returncode = return_value
        mock_result.stdout = stdout
        mock_result.stderr = stderr
        return mock_result
    
    @staticmethod
    def mock_file_exists(exists=True):
        """Create a mock os.path.exists."""
        return lambda path: exists
    
    @staticmethod
    def mock_file_read(content):
        """Create a mock file read."""
        return lambda: content
    
    @staticmethod
    def mock_file_write():
        """Create a mock file write."""
        return lambda content: None
    
    @staticmethod
    def wait_for_condition(condition, timeout=10, interval=0.1):
        """Wait for a condition to become true."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition():
                return True
            time.sleep(interval)
        return False
    
    @staticmethod
    def run_command(command, timeout=30):
        """Run a command and return the result."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=isinstance(command, str)
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out",
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
            }
    
    @staticmethod
    def check_port_open(host, port, timeout=5):
        """Check if a port is open."""
        import socket
        try:
            sock = socket.create_connection((host, port), timeout=timeout)
            sock.close()
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
    
    @staticmethod
    def check_process_running(process_name):
        """Check if a process is running."""
        try:
            result = subprocess.run(
                ["pgrep", "-x", process_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def get_process_pid(process_name):
        """Get the PID of a running process."""
        try:
            result = subprocess.run(
                ["pgrep", "-x", process_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
            return None
        except Exception:
            return None
    
    @staticmethod
    def kill_process(pid):
        """Kill a process by PID."""
        try:
            subprocess.run(["kill", str(pid)], check=True)
            return True
        except Exception:
            return False


class MockConfig:
    """Mock configuration for testing."""
    
    @staticmethod
    def get_torrc_content(password_hash="16:ABCD1234"):
        """Get sample torrc content."""
        return f"""ControlPort 9051
HashedControlPassword {password_hash}
SocksPort 9050
DataDirectory /var/lib/tor
Log notice file /var/log/tor/notices.log
"""
    
    @staticmethod
    def get_servers_dict():
        """Get sample servers dictionary."""
        return {
            "us": {"name": "United States", "id": 1},
            "de": {"name": "Germany", "id": 2},
            "gb": {"name": "United Kingdom", "id": 3},
            "fr": {"name": "France", "id": 4},
            "jp": {"name": "Japan", "id": 5},
        }
    
    @staticmethod
    def get_config_dict():
        """Get sample configuration dictionary."""
        return {
            "ControlPort": 9051,
            "SocksPort": 9050,
            "TransPort": 9040,
            "DNSPort": 5353,
            "HashedControlPassword": "16:ABCD1234EFGH5678",
            "DataDirectory": "/var/lib/tor",
        }


class MockTor:
    """Mock Tor controller for testing."""
    
    @staticmethod
    def create_mock_controller():
        """Create a mock Tor controller."""
        controller = MagicMock()
        controller.is_alive.return_value = True
        controller.get_version.return_value = "0.4.7.10"
        controller.authenticate.return_value = True
        controller.get_circuits.return_value = []
        controller.get_info.return_value = {}
        controller.signal.return_value = None
        controller.set_conf.return_value = None
        return controller
    
    @staticmethod
    def create_mock_circuit():
        """Create a mock Tor circuit."""
        circuit = MagicMock()
        circuit.id = 1
        circuit.purpose = "GENERAL"
        circuit.state = "BUILT"
        circuit.path = []
        return circuit
    
    @staticmethod
    def create_mock_stream():
        """Create a mock Tor stream."""
        stream = MagicMock()
        stream.id = 1
        stream.purpose = "DIR_FETCH"
        stream.state = "SUCCEEDED"
        return stream


class MockLogger:
    """Mock logger for testing."""
    
    def __init__(self):
        self.messages = []
    
    def info(self, message):
        """Log info message."""
        self.messages.append(("INFO", message))
    
    def debug(self, message):
        """Log debug message."""
        self.messages.append(("DEBUG", message))
    
    def warning(self, message):
        """Log warning message."""
        self.messages.append(("WARNING", message))
    
    def error(self, message):
        """Log error message."""
        self.messages.append(("ERROR", message))
    
    def critical(self, message):
        """Log critical message."""
        self.messages.append(("CRITICAL", message))
    
    def get_messages(self, level=None):
        """Get logged messages, optionally filtered by level."""
        if level:
            return [msg for lvl, msg in self.messages if lvl == level]
        return [msg for lvl, msg in self.messages]
    
    def clear(self):
        """Clear all messages."""
        self.messages.clear()


class TestAssertions:
    """Custom assertion helpers for testing."""
    
    @staticmethod
    def assert_dict_subset(subset, dictionary):
        """Assert that dictionary contains all key-value pairs from subset."""
        for key, value in subset.items():
            assert key in dictionary, f"Key '{key}' not found in dictionary"
            assert dictionary[key] == value, f"Value mismatch for key '{key}': expected {value}, got {dictionary[key]}"
    
    @staticmethod
    def assert_file_exists(path):
        """Assert that a file exists."""
        assert os.path.exists(path), f"File does not exist: {path}"
    
    @staticmethod
    def assert_file_not_exists(path):
        """Assert that a file does not exist."""
        assert not os.path.exists(path), f"File exists: {path}"
    
    @staticmethod
    def assert_file_content(path, expected_content):
        """Assert that a file contains expected content."""
        with open(path, 'r') as f:
            content = f.read()
        assert content == expected_content, f"File content mismatch"
    
    @staticmethod
    def assert_file_contains(path, expected_substring):
        """Assert that a file contains a substring."""
        with open(path, 'r') as f:
            content = f.read()
        assert expected_substring in content, f"File does not contain: {expected_substring}"
    
    @staticmethod
    def assert_file_permissions(path, expected_permissions):
        """Assert that a file has expected permissions."""
        actual_permissions = oct(os.stat(path).st_mode)[-3:]
        assert actual_permissions == expected_permissions, f"Permissions mismatch: expected {expected_permissions}, got {actual_permissions}"
    
    @staticmethod
    def assert_directory_exists(path):
        """Assert that a directory exists."""
        assert os.path.isdir(path), f"Directory does not exist: {path}"
    
    @staticmethod
    def assert_directory_not_exists(path):
        """Assert that a directory does not exist."""
        assert not os.path.isdir(path), f"Directory exists: {path}"
    
    @staticmethod
    def assert_process_running(process_name):
        """Assert that a process is running."""
        pid = TestHelper.get_process_pid(process_name)
        assert pid is not None, f"Process not running: {process_name}"
    
    @staticmethod
    def assert_process_not_running(process_name):
        """Assert that a process is not running."""
        pid = TestHelper.get_process_pid(process_name)
        assert pid is None, f"Process is running: {process_name}"
    
    @staticmethod
    def assert_port_open(host, port):
        """Assert that a port is open."""
        assert TestHelper.check_port_open(host, port), f"Port not open: {host}:{port}"
    
    @staticmethod
    def assert_port_closed(host, port):
        """Assert that a port is closed."""
        assert not TestHelper.check_port_open(host, port), f"Port is open: {host}:{port}"


class TestEnvironment:
    """Test environment setup and teardown."""
    
    def __init__(self):
        self.temp_dirs = []
        self.temp_files = []
        self.original_env = os.environ.copy()
    
    def setup(self):
        """Set up the test environment."""
        pass
    
    def teardown(self):
        """Tear down the test environment."""
        # Clean up temporary directories
        for directory in self.temp_dirs:
            TestHelper.cleanup_temp_directory(directory)
        
        # Clean up temporary files
        for file in self.temp_files:
            TestHelper.cleanup_temp_file(file)
        
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def create_temp_dir(self):
        """Create a temporary directory and track it for cleanup."""
        directory = TestHelper.create_temp_directory()
        self.temp_dirs.append(directory)
        return directory
    
    def create_temp_file(self, content, suffix=".txt"):
        """Create a temporary file and track it for cleanup."""
        file = TestHelper.create_temp_file(content, suffix)
        self.temp_files.append(file)
        return file


class TestDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.data = {}
    
    def set(self, key, value):
        """Set a value in the database."""
        self.data[key] = value
    
    def get(self, key, default=None):
        """Get a value from the database."""
        return self.data.get(key, default)
    
    def delete(self, key):
        """Delete a value from the database."""
        if key in self.data:
            del self.data[key]
    
    def exists(self, key):
        """Check if a key exists in the database."""
        return key in self.data
    
    def clear(self):
        """Clear all data from the database."""
        self.data.clear()


class TestCache:
    """Mock cache for testing."""
    
    def __init__(self):
        self.cache = {}
    
    def set(self, key, value, ttl=None):
        """Set a value in the cache."""
        self.cache[key] = {"value": value, "ttl": ttl}
    
    def get(self, key):
        """Get a value from the cache."""
        if key in self.cache:
            return self.cache[key]["value"]
        return None
    
    def delete(self, key):
        """Delete a value from the cache."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all data from the cache."""
        self.cache.clear()


class TestNetwork:
    """Mock network utilities for testing."""
    
    @staticmethod
    def mock_http_request(url, status_code=200, content=""):
        """Create a mock HTTP request."""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.text = content
        return mock_response
    
    @staticmethod
    def mock_dns_query(hostname, ip="192.0.2.1"):
        """Create a mock DNS query."""
        return ip
    
    @staticmethod
    def mock_socket_connection(host, port, success=True):
        """Create a mock socket connection."""
        mock_sock = Mock()
        mock_sock.connect.return_value = None if success else Exception("Connection refused")
        mock_sock.close.return_value = None
        return mock_sock


class TestTime:
    """Mock time utilities for testing."""
    
    def __init__(self):
        self.current_time = 1234567890.0
    
    def time(self):
        """Get the current time."""
        return self.current_time
    
    def sleep(self, seconds):
        """Sleep for a specified duration (mocked)."""
        self.current_time += seconds
    
    def advance(self, seconds):
        """Advance the time by a specified duration."""
        self.current_time += seconds


class TestRandom:
    """Mock random utilities for testing."""
    
    def __init__(self, seed=42):
        self.seed = seed
        self.counter = 0
    
    def choice(self, sequence):
        """Choose a random element from a sequence."""
        self.counter += 1
        return sequence[self.counter % len(sequence)]
    
    def randint(self, a, b):
        """Generate a random integer."""
        self.counter += 1
        return (self.counter % (b - a + 1)) + a
    
    def random(self):
        """Generate a random float."""
        self.counter += 1
        return (self.counter % 1000) / 1000.0


class TestFileSystem:
    """Mock file system operations for testing."""
    
    def __init__(self):
        self.files = {}
        self.directories = set()
    
    def write_file(self, path, content):
        """Write a file."""
        self.files[path] = content
    
    def read_file(self, path):
        """Read a file."""
        return self.files.get(path, "")
    
    def file_exists(self, path):
        """Check if a file exists."""
        return path in self.files
    
    def create_directory(self, path):
        """Create a directory."""
        self.directories.add(path)
    
    def directory_exists(self, path):
        """Check if a directory exists."""
        return path in self.directories
    
    def delete_file(self, path):
        """Delete a file."""
        if path in self.files:
            del self.files[path]
    
    def delete_directory(self, path):
        """Delete a directory."""
        if path in self.directories:
            self.directories.remove(path)
    
    def list_directory(self, path):
        """List directory contents."""
        contents = []
        for file_path in self.files:
            if file_path.startswith(path):
                contents.append(file_path[len(path):].lstrip("/"))
        return contents


def skip_if_no_network():
    """Decorator to skip tests if network is unavailable."""
    import pytest
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return lambda func: func
    except Exception:
        return pytest.mark.skip("Network unavailable")


def skip_if_no_tor():
    """Decorator to skip tests if Tor is unavailable."""
    import pytest
    try:
        result = subprocess.run(["tor", "--version"], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode != 0:
            return pytest.mark.skip("Tor is not installed")
        return lambda func: func
    except Exception:
        return pytest.mark.skip("Tor is not available")


def skip_if_no_root():
    """Decorator to skip tests if not running as root."""
    import pytest
    if os.geteuid() != 0:
        return pytest.mark.skip("Test requires root privileges")
    return lambda func: func


def skip_if_no_gui():
    """Decorator to skip tests if GUI environment is unavailable."""
    import pytest
    if os.environ.get("DISPLAY") is None:
        return pytest.mark.skip("GUI environment not available")
    return lambda func: func
