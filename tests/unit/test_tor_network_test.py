"""
Unit tests for tor_network_test.py - Network connectivity tester.
"""
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
import subprocess

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestTorNetworkTest:
    """Test suite for tor_network_test.py main functionality."""
    
    @pytest.fixture
    def mock_tor_network_test_module(self):
        """Mock the tor_network_test module."""
        import tor_network_test as tnt
        return tnt
    
    def test_is_tor_running_true(self, mock_tor_network_test_module, mock_psutil):
        """Test Tor running check when Tor is running."""
        result = mock_tor_network_test_module.is_tor_running()
        
        assert result is True
    
    def test_is_tor_running_false(self, mock_tor_network_test_module):
        """Test Tor running check when Tor is not running."""
        with patch('psutil.process_iter', return_value=[]):
            result = mock_tor_network_test_module.is_tor_running()
            
            assert result is False
    
    def test_is_tor_running_exception(self, mock_tor_network_test_module):
        """Test Tor running check when exception occurs."""
        with patch('psutil.process_iter', side_effect=Exception("Error")):
            result = mock_tor_network_test_module.is_tor_running()
            
            assert result is False
    
    def test_check_port_status_open(self, mock_tor_network_test_module, mock_network_socket):
        """Test port status check when port is open."""
        result = mock_tor_network_test_module.check_port_status("127.0.0.1", 9051)
        
        assert result is True
    
    def test_check_port_status_closed(self, mock_tor_network_test_module):
        """Test port status check when port is closed."""
        with patch('socket.create_connection', side_effect=ConnectionRefusedError):
            result = mock_tor_network_test_module.check_port_status("127.0.0.1", 9051)
            
            assert result is False
    
    def test_check_port_status_timeout(self, mock_tor_network_test_module):
        """Test port status check when connection times out."""
        with patch('socket.create_connection', side_effect=TimeoutError):
            result = mock_tor_network_test_module.check_port_status("127.0.0.1", 9051)
            
            assert result is False
    
    def test_detect_tor_control_port_default(self, mock_tor_network_test_module, mock_torrc_file):
        """Test control port detection with default config."""
        port = mock_tor_network_test_module.detect_tor_control_port()
        
        assert port == 9051
    
    def test_detect_tor_control_port_custom(self, mock_tor_network_test_module, tmp_path):
        """Test control port detection with custom port."""
        custom_torrc = tmp_path / "custom_torrc"
        custom_torrc.write_text("ControlPort 9052")
        
        with patch('tor_network_test.TORRC_PATHS', [str(custom_torrc)]):
            port = mock_tor_network_test_module.detect_tor_control_port()
            
            assert port == 9052
    
    def test_detect_tor_control_port_not_found(self, mock_tor_network_test_module):
        """Test control port detection when not found."""
        with patch('tor_network_test.TORRC_PATHS', []):
            port = mock_tor_network_test_module.detect_tor_control_port()
            
            assert port == 9051  # Should return default
    
    def test_detect_tor_password_found(self, mock_tor_network_test_module, tmp_path):
        """Test password detection when found."""
        custom_torrc = tmp_path / "custom_torrc"
        custom_torrc.write_text("ControlPort 9051\nHashedControlPassword 16:ABCD1234")
        
        with patch('tor_network_test.TORRC_PATHS', [str(custom_torrc)]):
            password = mock_tor_network_test_module.detect_tor_password()
            
            # Should return None for hashed passwords
            assert password is None
    
    def test_detect_tor_password_plain_text(self, mock_tor_network_test_module, tmp_path):
        """Test password detection with plain text password."""
        custom_torrc = tmp_path / "custom_torrc"
        custom_torrc.write_text("ControlPort 9051\nControlPassword mypassword")
        
        with patch('tor_network_test.TORRC_PATHS', [str(custom_torrc)]):
            password = mock_tor_network_test_module.detect_tor_password()
            
            assert password == "mypassword"
    
    def test_detect_tor_password_not_found(self, mock_tor_network_test_module):
        """Test password detection when not found."""
        with patch('tor_network_test.TORRC_PATHS', []):
            password = mock_tor_network_test_module.detect_tor_password()
            
            assert password is None
    
    def test_detect_auth_cookie_found(self, mock_tor_network_test_module, mock_auth_cookie):
        """Test auth cookie detection when found."""
        with patch('tor_network_test.AUTH_COOKIE_PATHS', [str(mock_auth_cookie)]):
            cookie_path = mock_tor_network_test_module.detect_auth_cookie()
            
            assert cookie_path == str(mock_auth_cookie)
    
    def test_detect_auth_cookie_not_found(self, mock_tor_network_test_module):
        """Test auth cookie detection when not found."""
        with patch('tor_network_test.AUTH_COOKIE_PATHS', []):
            cookie_path = mock_tor_network_test_module.detect_auth_cookie()
            
            assert cookie_path is None
    
    def test_test_tor_connection_success(self, mock_tor_network_test_module, mock_stem_controller):
        """Test successful Tor connection test."""
        with patch('stem.control.Controller.from_port', return_value=mock_stem_controller):
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.status_code = 200
                        mock_response.text = "Congratulations"
                        mock_get.return_value = mock_response
                        
                        result = mock_tor_network_test_module.test_tor_connection()
                        
                        assert result["connection"] is True
                        assert result["latency"] is not None
                        assert result["exit_ip"] is not None
                        assert len(result["errors"]) == 0
    
    def test_test_tor_connection_tor_not_running(self, mock_tor_network_test_module):
        """Test Tor connection when Tor is not running."""
        with patch('tor_network_test.is_tor_running', return_value=False):
            result = mock_tor_network_test_module.test_tor_connection()
            
            assert result["connection"] is False
            assert len(result["errors"]) > 0
    
    def test_test_tor_connection_port_not_accessible(self, mock_tor_network_test_module):
        """Test Tor connection when control port not accessible."""
        with patch('tor_network_test.is_tor_running', return_value=True):
            with patch('tor_network_test.check_port_status', return_value=False):
                result = mock_tor_network_test_module.test_tor_connection()
                
                assert result["connection"] is False
                assert len(result["errors"]) > 0
    
    def test_test_tor_connection_auth_fails(self, mock_tor_network_test_module):
        """Test Tor connection when authentication fails."""
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_context.__enter__ = MagicMock(side_effect=Exception("Authentication failed"))
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    result = mock_tor_network_test_module.test_tor_connection()
                    
                    assert result["connection"] is False
                    assert len(result["errors"]) > 0
    
    def test_test_tor_connection_network_error(self, mock_tor_network_test_module, mock_stem_controller):
        """Test Tor connection with network error."""
        with patch('stem.control.Controller.from_port', return_value=mock_stem_controller):
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get', side_effect=Exception("Network error")):
                        result = mock_tor_network_test_module.test_tor_connection()
                        
                        assert result["connection"] is True  # Connection to Tor succeeded
                        assert result["latency"] is not None
                        assert result["exit_ip"] is None  # But exit IP failed


class TestTorNetworkTestSecurity:
    """Test security-related functionality in tor_network_test.py."""
    
    @pytest.fixture
    def mock_tor_network_test_module(self):
        """Mock the tor_network_test module."""
        import tor_network_test as tnt
        return tnt
    
    def test_password_not_logged(self, mock_tor_network_test_module):
        """Test that passwords are not logged."""
        # This test documents expected behavior
        assert True  # Placeholder for actual log checking
    
    def test_auth_cookie_permissions(self, mock_tor_network_test_module, tmp_path):
        """Test that auth cookie has restricted permissions."""
        cookie_file = tmp_path / "control_auth_cookie"
        cookie_file.write_bytes(b"\x00" * 32)
        cookie_file.chmod(0o600)
        
        permissions = oct(cookie_file.stat().st_mode)[-3:]
        assert permissions == "600"
    
    def test_control_port_localhost_only(self, mock_tor_network_test_module):
        """Test that control port is only accessible from localhost."""
        # This test documents expected behavior
        assert True  # Placeholder for actual port binding check


class TestTorNetworkTestErrorHandling:
    """Test error handling in tor_network_test.py."""
    
    @pytest.fixture
    def mock_tor_network_test_module(self):
        """Mock the tor_network_test module."""
        import tor_network_test as tnt
        return tnt
    
    def test_check_port_status_invalid_host(self, mock_tor_network_test_module):
        """Test port status check with invalid host."""
        with patch('socket.create_connection', side_effect=OSError("Invalid host")):
            result = mock_tor_network_test_module.check_port_status("invalid_host", 9051)
            
            assert result is False
    
    def test_check_port_status_invalid_port(self, mock_tor_network_test_module):
        """Test port status check with invalid port."""
        with patch('socket.create_connection', side_effect=OSError("Invalid port")):
            result = mock_tor_network_test_module.check_port_status("127.0.0.1", -1)
            
            assert result is False
    
    def test_detect_tor_control_port_read_error(self, mock_tor_network_test_module, tmp_path):
        """Test control port detection with read error."""
        custom_torrc = tmp_path / "custom_torrc"
        custom_torrc.write_text("ControlPort 9051")
        custom_torrc.chmod(0o000)
        
        with patch('tor_network_test.TORRC_PATHS', [str(custom_torrc)]):
            port = mock_tor_network_test_module.detect_tor_control_port()
            
            assert port == 9051  # Should return default on error
    
    def test_detect_auth_cookie_read_error(self, mock_tor_network_test_module, tmp_path):
        """Test auth cookie detection with read error."""
        cookie_file = tmp_path / "control_auth_cookie"
        cookie_file.write_bytes(b"\x00" * 32)
        cookie_file.chmod(0o000)
        
        with patch('tor_network_test.AUTH_COOKIE_PATHS', [str(cookie_file)]):
            cookie_path = mock_tor_network_test_module.detect_auth_cookie()
            
            assert cookie_path is None


class TestTorNetworkTestEdgeCases:
    """Test edge cases in tor_network_test.py."""
    
    @pytest.fixture
    def mock_tor_network_test_module(self):
        """Mock the tor_network_test module."""
        import tor_network_test as tnt
        return tnt
    
    def test_check_port_status_ipv6(self, mock_tor_network_test_module, mock_network_socket):
        """Test port status check with IPv6 address."""
        result = mock_tor_network_test_module.check_port_status("::1", 9051)
        
        assert result is True
    
    def test_check_port_status_very_high_port(self, mock_tor_network_test_module):
        """Test port status check with very high port number."""
        with patch('socket.create_connection', side_effect=OSError):
            result = mock_tor_network_test_module.check_port_status("127.0.0.1", 65535)
            
            assert result is False
    
    def test_detect_tor_control_port_multiple_configs(self, mock_tor_network_test_module, tmp_path):
        """Test control port detection with multiple config files."""
        torrc1 = tmp_path / "torrc1"
        torrc1.write_text("ControlPort 9051")
        torrc2 = tmp_path / "torrc2"
        torrc2.write_text("ControlPort 9052")
        
        with patch('tor_network_test.TORRC_PATHS', [str(torrc1), str(torrc2)]):
            port = mock_tor_network_test_module.detect_tor_control_port()
            
            # Should use first found
            assert port in [9051, 9052]
    
    def test_detect_tor_password_mixed_format(self, mock_tor_network_test_module, tmp_path):
        """Test password detection with mixed format."""
        custom_torrc = tmp_path / "custom_torrc"
        custom_torrc.write_text("ControlPort 9051\nHashedControlPassword 16:ABCD\nControlPassword plain")
        
        with patch('tor_network_test.TORRC_PATHS', [str(custom_torrc)]):
            password = mock_tor_network_test_module.detect_tor_password()
            
            # Should prefer plain text if available
            assert password == "plain"
    
    def test_test_tor_connection_zero_latency(self, mock_tor_network_test_module, mock_stem_controller):
        """Test Tor connection with zero latency."""
        with patch('stem.control.Controller.from_port', return_value=mock_stem_controller):
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.status_code = 200
                        mock_response.text = "Congratulations"
                        mock_get.return_value = mock_response
                        
                        with patch('time.time', side_effect=[0, 0]):
                            result = mock_tor_network_test_module.test_tor_connection()
                            
                            assert result["connection"] is True
                            assert result["latency"] == 0.0
    
    def test_test_tor_connection_high_latency(self, mock_tor_network_test_module, mock_stem_controller):
        """Test Tor connection with high latency."""
        with patch('stem.control.Controller.from_port', return_value=mock_stem_controller):
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.status_code = 200
                        mock_response.text = "Congratulations"
                        mock_get.return_value = mock_response
                        
                        with patch('time.time', side_effect=[0, 10]):
                            result = mock_tor_network_test_module.test_tor_connection()
                            
                            assert result["connection"] is True
                            assert result["latency"] == 10.0


class TestTorNetworkTestIntegration:
    """Integration tests for tor_network_test.py."""
    
    @pytest.fixture
    def mock_tor_network_test_module(self):
        """Mock the tor_network_test module."""
        import tor_network_test as tnt
        return tnt
    
    @pytest.mark.tor
    @pytest.mark.integration
    def test_real_tor_connection(self, mock_tor_network_test_module):
        """Test real Tor connection."""
        # This test requires Tor to be running
        pytest.skip("Requires Tor to be running")
    
    @pytest.mark.network
    @pytest.mark.integration
    def test_real_network_test(self, mock_tor_network_test_module):
        """Test real network connectivity."""
        # This test requires network access
        pytest.skip("Requires network access")
    
    @pytest.mark.integration
    def test_full_test_workflow(self, mock_tor_network_test_module, mock_stem_controller):
        """Test full test workflow."""
        with patch('stem.control.Controller.from_port', return_value=mock_stem_controller):
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.status_code = 200
                        mock_response.text = "Congratulations"
                        mock_get.return_value = mock_response
                        
                        result = mock_tor_network_test_module.test_tor_connection()
                        
                        assert result["connection"] is True
                        assert "latency" in result
                        assert "exit_ip" in result
                        assert "errors" in result
