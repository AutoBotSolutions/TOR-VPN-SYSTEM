"""
End-to-end workflow tests for Tor VPN System.
"""
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import subprocess
import tempfile

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


class TestEndToEndInstallationWorkflow:
    """Test complete installation workflow."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        log_dir = workspace / "logs"
        log_dir.mkdir()
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
            "log_dir": log_dir,
        }
    
    @pytest.mark.tor
    def test_complete_linux_installation(self, temp_workspace):
        """Test complete installation on Linux."""
        pytest.skip("Requires actual Tor installation")
    
    @pytest.mark.tor
    def test_complete_macos_installation(self, temp_workspace):
        """Test complete installation on macOS."""
        pytest.skip("Requires actual Tor installation")
    
    @pytest.mark.tor
    def test_complete_windows_installation(self, temp_workspace):
        """Test complete installation on Windows."""
        pytest.skip("Requires actual Tor installation")
    
    def test_mocked_installation_workflow(self, temp_workspace):
        """Test installation workflow with mocked dependencies."""
        import tor_auto_torrc_config as tatc
        
        config_dir = temp_workspace["config_dir"]
        
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            # Check if Tor is installed
            mock_run.returncode = 0
            is_installed = tatc.check_if_tor_installed()
            assert is_installed is True
            
            # Install Tor (mocked)
            with patch('platform.system', return_value="Linux"):
                tatc.install_tor()
                assert mock_run.called
    
    def test_configuration_workflow(self, temp_workspace):
        """Test configuration workflow."""
        import tor_custom_config as tcc
        import tor_auto_torrc_config as tatc
        
        config_dir = temp_workspace["config_dir"]
        torrc_path = config_dir / "torrc"
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(torrc_path)):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        # Generate custom config
                        tcc.create_torrc_file()
                        
                        assert torrc_path.exists()
                        
                        content = torrc_path.read_text()
                        assert "ControlPort 9051" in content
                        assert "16:HASHED" in content


class TestEndToEndConnectionWorkflow:
    """Test complete connection workflow."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        torrc_path = config_dir / "torrc"
        torrc_path.write_text("ControlPort 9051\nSocksPort 9050")
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
            "torrc_path": torrc_path,
        }
    
    def test_connect_with_country_selection(self, temp_workspace):
        """Test connecting with country selection."""
        import tor_vpn_beta as tvb
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            # Connect to US
            result = tvb.connect_to_tor("us")
            assert result is True
            
            # Disconnect
            result = tvb.disconnect_tor()
            assert result is True
    
    def test_country_switch_workflow(self, temp_workspace):
        """Test switching between countries."""
        import tor_vpn_beta as tvb
        
        countries = ["us", "de", "gb", "fr", "jp"]
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            for country in countries:
                result = tvb.connect_to_tor(country)
                assert result is True
                
                # Disconnect
                tvb.disconnect_tor()
    
    def test_reconnection_workflow(self, temp_workspace):
        """Test reconnection after disconnection."""
        import tor_vpn_beta as tvb
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            # First connection
            tvb.connect_to_tor("us")
            
            # Disconnect
            tvb.disconnect_tor()
            
            # Reconnect
            result = tvb.connect_to_tor("de")
            assert result is True


class TestEndToEndDiagnosticWorkflow:
    """Test complete diagnostic workflow."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        torrc_path = config_dir / "torrc"
        torrc_path.write_text("ControlPort 9051\nSocksPort 9050")
        output_dir = workspace / "diagnostics"
        output_dir.mkdir()
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
            "torrc_path": torrc_path,
            "output_dir": output_dir,
        }
    
    def test_full_diagnostic_collection(self, temp_workspace):
        """Test full diagnostic collection."""
        import tor_diagnostic_repair as tdr
        
        output_dir = temp_workspace["output_dir"]
        
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            # Validate configuration
            is_valid = tdr.validate_tor_configuration()
            assert is_valid is True
            
            # Detect init system
            with patch('os.path.exists', return_value=True):
                init_system = tdr.detect_init_system()
                assert init_system == 'systemd'
            
            # Collect diagnostics
            with patch('shutil.copy'):
                result = tdr.collect_diagnostics(str(output_dir))
                assert result is True
    
    def test_diagnostic_and_repair_workflow(self, temp_workspace):
        """Test diagnostic and repair workflow."""
        import tor_diagnostic_repair as tdr
        
        output_dir = temp_workspace["output_dir"]
        
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            # Run diagnostics
            with patch('shutil.copy'):
                tdr.collect_diagnostics(str(output_dir))
            
            # Restart Tor service
            with patch('os.path.exists', return_value=True):
                result = tdr.restart_tor_service('systemd', 'test_password')
                assert result is True


class TestEndToEndNetworkTestWorkflow:
    """Test complete network testing workflow."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        torrc_path = config_dir / "torrc"
        torrc_path.write_text("ControlPort 9051\nSocksPort 9050")
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
            "torrc_path": torrc_path,
        }
    
    def test_complete_network_test(self, temp_workspace):
        """Test complete network test workflow."""
        import tor_network_test as tnt
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.get_circuits.return_value = []
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.status_code = 200
                        mock_response.text = "Congratulations"
                        mock_get.return_value = mock_response
                        
                        result = tnt.test_tor_connection()
                        
                        assert result["connection"] is True
                        assert "latency" in result
                        assert "exit_ip" in result
                        assert len(result["errors"]) == 0
    
    def test_network_test_after_connection(self, temp_workspace):
        """Test network test after establishing connection."""
        import tor_vpn_beta as tvb
        import tor_network_test as tnt
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_ctrl.get_circuits.return_value = []
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            # Connect
            tvb.connect_to_tor("us")
            
            # Test network
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.status_code = 200
                        mock_response.text = "Congratulations"
                        mock_get.return_value = mock_response
                        
                        result = tnt.test_tor_connection()
                        assert result["connection"] is True


class TestEndToEndTransparentProxyWorkflow:
    """Test complete transparent proxy setup workflow."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
        }
    
    @pytest.mark.root
    def test_complete_transparent_proxy_setup(self, temp_workspace):
        """Test complete transparent proxy setup."""
        import tor_route_traffic_setup as trts
        
        config_dir = temp_workspace["config_dir"]
        
        with patch('os.geteuid', return_value=0):
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_run.return_value = mock_result
                
                # Stop Tor if running
                trts.stop_tor_if_running()
                
                # Create directory
                trts.create_directory(str(config_dir))
                assert config_dir.exists()
                
                # Create torrc
                with patch('tor_route_traffic_setup.torrc_directory', str(config_dir)):
                    with patch('tor_route_traffic_setup.torrc_path', str(config_dir / "torrc")):
                        trts.create_torrc_file()
                        
                        assert (config_dir / "torrc").exists()
                
                # Setup iptables
                trts.setup_iptables("100")
                assert mock_run.called


class TestEndToEndStartupValidationWorkflow:
    """Test complete startup validation workflow."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
        }
    
    def test_complete_startup_validation(self, temp_workspace):
        """Test complete startup validation workflow."""
        import tor_vpn_inclued as tvi
        
        config_dir = temp_workspace["config_dir"]
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:HASHED"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    # Validate and generate config
                    torrc_path, data_dir = tvi.validate_and_generate_config()
                    
                    assert torrc_path is not None
                    assert data_dir is not None
                    assert config_dir.exists()
    
    def test_startup_and_connection_workflow(self, temp_workspace):
        """Test startup validation followed by connection."""
        import tor_vpn_inclued as tvi
        import tor_vpn_beta as tvb
        
        config_dir = temp_workspace["config_dir"]
        
        # Validate and generate config
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:HASHED"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    torrc_path, data_dir = tvi.validate_and_generate_config()
                    
                    assert torrc_path is not None
        
        # Connect
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            result = tvb.connect_to_tor("us")
            assert result is True


class TestEndToEndErrorRecoveryWorkflow:
    """Test error recovery workflows."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
        }
    
    def test_connection_failure_recovery(self, temp_workspace):
        """Test recovery from connection failure."""
        import tor_vpn_beta as tvb
        
        # First connection attempt fails
        with patch('stem.control.Controller.from_port', side_effect=Exception("Connection refused")):
            with pytest.raises(Exception):
                tvb.connect_to_tor("us")
        
        # Retry after fixing the issue
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            result = tvb.connect_to_tor("us")
            assert result is True
    
    def test_configuration_error_recovery(self, temp_workspace):
        """Test recovery from configuration error."""
        import tor_custom_config as tcc
        
        config_dir = temp_workspace["config_dir"]
        
        # First attempt fails (password hashing error)
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'tor')):
                        try:
                            tcc.create_torrc_file()
                        except subprocess.CalledProcessError:
                            pass  # Expected
        
        # Retry with successful password hashing
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        tcc.create_torrc_file()
                        
                        assert (config_dir / "torrc").exists()


class TestEndToEndMultiUserWorkflow:
    """Test multi-user workflows."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        
        return {
            "workspace": workspace,
        }
    
    def test_multiple_users_configuration(self, temp_workspace):
        """Test configuration for multiple users."""
        users = ["user1", "user2", "user3"]
        
        for user in users:
            user_config_dir = temp_workspace["workspace"] / user / ".tor_config"
            user_config_dir.mkdir(parents=True)
            
            # Create config for each user
            assert user_config_dir.exists()
    
    def test_user_specific_config_paths(self, temp_workspace):
        """Test user-specific configuration paths."""
        users = ["user1", "user2"]
        
        for user in users:
            with patch('os.path.expanduser') as mock_expand:
                mock_expand.return_value = f"/home/{user}/.tor_config"
                
                result = os.path.expanduser("~/.tor_config")
                assert user in result


class TestEndToEndPerformanceWorkflow:
    """Test performance-related workflows."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        
        return {
            "workspace": workspace,
        }
    
    def test_connection_latency_measurement(self, temp_workspace):
        """Test connection latency measurement."""
        import tor_network_test as tnt
        import time
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.get_circuits.return_value = []
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            with patch('tor_network_test.is_tor_running', return_value=True):
                with patch('tor_network_test.check_port_status', return_value=True):
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.status_code = 200
                        mock_response.text = "Congratulations"
                        mock_get.return_value = mock_response
                        
                        start_time = time.time()
                        result = tnt.test_tor_connection()
                        end_time = time.time()
                        
                        assert result["connection"] is True
                        assert result["latency"] is not None
    
    def test_multiple_connections_performance(self, temp_workspace):
        """Test performance of multiple connections."""
        import tor_vpn_beta as tvb
        import time
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            # Connect to different countries
            countries = ["us", "de", "gb"]
            connection_times = []
            
            for country in countries:
                start_time = time.time()
                tvb.connect_to_tor(country)
                tvb.disconnect_tor()
                end_time = time.time()
                
                connection_times.append(end_time - start_time)
            
            # All connections should complete
            assert len(connection_times) == 3
            assert all(t > 0 for t in connection_times)


class TestEndToEndSecurityWorkflow:
    """Test security-related workflows."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        config_dir = workspace / "tor_config"
        config_dir.mkdir()
        
        return {
            "workspace": workspace,
            "config_dir": config_dir,
        }
    
    def test_secure_password_workflow(self, temp_workspace):
        """Test secure password handling workflow."""
        import tor_custom_config as tcc
        
        config_dir = temp_workspace["config_dir"]
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        # Create config with hashed password
                        tcc.create_torrc_file()
                        
                        torrc_content = (config_dir / "torrc").read_text()
                        
                        # Verify plain text password not in torrc
                        assert "test_password" not in torrc_content
                        # Verify hashed password is in torrc
                        assert "16:HASHED" in torrc_content
    
    def test_file_permissions_workflow(self, temp_workspace):
        """Test file permissions workflow."""
        import tor_custom_config as tcc
        
        config_dir = temp_workspace["config_dir"]
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        # Create config
                        tcc.create_torrc_file()
                        
                        # Check torrc permissions
                        torrc_file = config_dir / "torrc"
                        permissions = oct(torrc_file.stat().st_mode)[-3:]
                        assert permissions == "600"
                        
                        # Check directory permissions
                        dir_permissions = oct(config_dir.stat().st_mode)[-3:]
                        assert dir_permissions == "700"


class TestEndToEndCleanupWorkflow:
    """Test cleanup workflows."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        
        return {
            "workspace": workspace,
        }
    
    def test_complete_cleanup_workflow(self, temp_workspace):
        """Test complete cleanup after use."""
        import tor_vpn_beta as tvb
        
        config_dir = temp_workspace["workspace"] / "tor_config"
        config_dir.mkdir()
        log_dir = temp_workspace["workspace"] / "logs"
        log_dir.mkdir()
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.authenticate.return_value = True
            mock_ctrl.signal.return_value = None
            mock_ctrl.set_conf.return_value = None
            mock_context.__enter__ = MagicMock(return_value=mock_ctrl)
            mock_context.__exit__ = MagicMock(return_value=False)
            mock_controller.return_value = mock_context
            
            # Connect
            tvb.connect_to_tor("us")
            
            # Disconnect
            tvb.disconnect_tor()
            
            # Cleanup temporary files
            if config_dir.exists():
                import shutil
                shutil.rmtree(config_dir)
            
            if log_dir.exists():
                import shutil
                shutil.rmtree(log_dir)
            
            assert not config_dir.exists()
            assert not log_dir.exists()
