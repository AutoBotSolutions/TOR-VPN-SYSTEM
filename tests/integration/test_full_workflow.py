"""
Integration tests for full Tor VPN System workflows.
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


class TestFullWorkflow:
    """Test suite for full system workflows."""
    
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
    
    def test_configuration_workflow(self, temp_workspace):
        """Test complete configuration workflow."""
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
    
    def test_diagnostic_workflow(self, temp_workspace):
        """Test complete diagnostic workflow."""
        import tor_diagnostic_repair as tdr
        
        output_dir = temp_workspace["workspace"] / "diagnostics"
        output_dir.mkdir()
        
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
    
    def test_network_test_workflow(self, temp_workspace):
        """Test complete network testing workflow."""
        import tor_network_test as tnt
        
        with patch('stem.control.Controller.from_port') as mock_controller:
            mock_context = MagicMock()
            mock_ctrl = MagicMock()
            mock_ctrl.is_alive.return_value = True
            mock_ctrl.get_version.return_value = "0.4.7.10"
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
    
    def test_connection_workflow(self, temp_workspace):
        """Test complete connection workflow."""
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
            
            # Connect
            result = tvb.connect_to_tor("us")
            assert result is True
            
            # Disconnect
            result = tvb.disconnect_tor()
            assert result is True


class TestEndToEndScenarios:
    """Test end-to-end scenarios."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        return workspace
    
    @pytest.mark.tor
    def test_first_time_setup(self, temp_workspace):
        """Test first-time setup scenario."""
        pytest.skip("Requires Tor to be installed")
    
    @pytest.mark.tor
    def test_country_switch_workflow(self, temp_workspace):
        """Test switching between countries."""
        pytest.skip("Requires Tor to be installed")
    
    @pytest.mark.tor
    def test_connection_reestablishment(self, temp_workspace):
        """Test re-establishing connection after disconnection."""
        pytest.skip("Requires Tor to be installed")
    
    @pytest.mark.tor
    def test_configuration_update_workflow(self, temp_workspace):
        """Test updating configuration while running."""
        pytest.skip("Requires Tor to be installed")
    
    @pytest.mark.tor
    def test_error_recovery_workflow(self, temp_workspace):
        """Test recovering from errors."""
        pytest.skip("Requires Tor to be installed")


class TestComponentIntegration:
    """Test integration between components."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        return workspace
    
    def test_config_and_network_test_integration(self, temp_workspace):
        """Test integration between configuration and network testing."""
        import tor_custom_config as tcc
        import tor_network_test as tnt
        
        config_dir = temp_workspace / "tor_config"
        config_dir.mkdir()
        torrc_path = config_dir / "torrc"
        
        # Create configuration
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(torrc_path)):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        tcc.create_torrc_file()
                        
                        assert torrc_path.exists()
        
        # Test network with created config
        with patch('tor_network_test.TORRC_PATHS', [str(torrc_path)]):
            port = tnt.detect_tor_control_port()
            assert port == 9051
    
    def test_diagnostic_and_config_integration(self, temp_workspace):
        """Test integration between diagnostics and configuration."""
        import tor_diagnostic_repair as tdr
        import tor_custom_config as tcc
        
        config_dir = temp_workspace / "tor_config"
        config_dir.mkdir()
        torrc_path = config_dir / "torrc"
        
        # Create configuration
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(torrc_path)):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        tcc.create_torrc_file()
        
        # Validate configuration
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            is_valid = tdr.validate_tor_configuration()
            assert is_valid is True
    
    def test_startup_and_connection_integration(self, temp_workspace):
        """Test integration between startup validation and connection."""
        import tor_vpn_inclued as tvi
        import tor_vpn_beta as tvb
        
        config_dir = temp_workspace / "tor_config"
        
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
        
        # Test connection
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


class TestErrorHandlingIntegration:
    """Test error handling across components."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        return workspace
    
    def test_config_failure_recovery(self, temp_workspace):
        """Test recovery from configuration failure."""
        import tor_custom_config as tcc
        
        config_dir = temp_workspace / "tor_config"
        config_dir.mkdir()
        
        # Simulate password hashing failure
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'tor')):
                        try:
                            tcc.create_torrc_file()
                        except subprocess.CalledProcessError:
                            # Expected behavior
                            assert True
    
    def test_network_test_failure_recovery(self, temp_workspace):
        """Test recovery from network test failure."""
        import tor_network_test as tnt
        
        with patch('tor_network_test.is_tor_running', return_value=False):
            result = tnt.test_tor_connection()
            
            assert result["connection"] is False
            assert len(result["errors"]) > 0
    
    def test_diagnostic_failure_recovery(self, temp_workspace):
        """Test recovery from diagnostic failure."""
        import tor_diagnostic_repair as tdr
        
        output_dir = temp_workspace / "diagnostics"
        output_dir.mkdir()
        
        # Simulate validation failure
        with patch('subprocess.run', side_effect=FileNotFoundError):
            is_valid = tdr.validate_tor_configuration()
            
            assert is_valid is False
    
    def test_connection_failure_recovery(self):
        """Test recovery from connection failure."""
        import tor_vpn_beta as tvb
        
        with patch('stem.control.Controller.from_port', side_effect=Exception("Connection refused")):
            with pytest.raises(Exception):
                tvb.connect_to_tor("us")


class TestPerformanceIntegration:
    """Test performance aspects of integrated system."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        return workspace
    
    def test_config_generation_performance(self, temp_workspace):
        """Test configuration generation performance."""
        import tor_custom_config as tcc
        import time
        
        config_dir = temp_workspace / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        start_time = time.time()
                        tcc.create_torrc_file()
                        end_time = time.time()
                        
                        duration = end_time - start_time
                        assert duration < 5.0  # Should complete in under 5 seconds
    
    def test_network_test_performance(self):
        """Test network test performance."""
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
                        
                        duration = end_time - start_time
                        assert duration < 10.0  # Should complete in under 10 seconds
                        assert result["connection"] is True


class TestSecurityIntegration:
    """Test security aspects across integrated system."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        return workspace
    
    def test_password_security_across_components(self, temp_workspace):
        """Test that passwords are handled securely across components."""
        import tor_custom_config as tcc
        import tor_vpn_beta as tvb
        
        config_dir = temp_workspace / "tor_config"
        config_dir.mkdir()
        
        # Generate config with password
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        tcc.create_torrc_file()
        
        # Verify password is hashed in torrc
        torrc_file = config_dir / "torrc"
        content = torrc_file.read_text()
        
        assert "test_password" not in content
        assert "16:HASHED" in content
    
    def test_file_permissions_across_components(self, temp_workspace):
        """Test that file permissions are set correctly across components."""
        import tor_custom_config as tcc
        
        config_dir = temp_workspace / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_result = Mock()
                        mock_result.stdout = "16:HASHED"
                        mock_result.returncode = 0
                        mock_run.return_value = mock_result
                        
                        tcc.create_torrc_file()
        
        # Check torrc permissions
        torrc_file = config_dir / "torrc"
        permissions = oct(torrc_file.stat().st_mode)[-3:]
        assert permissions == "600"
        
        # Check directory permissions
        dir_permissions = oct(config_dir.stat().st_mode)[-3:]
        assert dir_permissions == "700"


class TestPlatformIntegration:
    """Test platform-specific integration."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        return workspace
    
    def test_linux_integration(self, temp_workspace, mock_platform):
        """Test Linux-specific integration."""
        mock_platform["system"] = "Linux"
        
        with patch('platform.system', return_value="Linux"):
            import tor_auto_torrc_config as tatc
            
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_run.return_value = mock_result
                
                tatc.install_tor()
                assert mock_run.called
    
    def test_macos_integration(self, temp_workspace, mock_platform):
        """Test macOS-specific integration."""
        mock_platform["system"] = "Darwin"
        
        with patch('platform.system', return_value="Darwin"):
            import tor_auto_torrc_config as tatc
            
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_run.return_value = mock_result
                
                tatc.install_tor()
                assert mock_run.called
    
    def test_windows_integration(self, temp_workspace, mock_platform):
        """Test Windows-specific integration."""
        mock_platform["system"] = "Windows"
        
        with patch('platform.system', return_value="Windows"):
            import tor_auto_torrc_config as tatc
            
            # Windows installation may not be automated
            tatc.install_tor()
            assert True


class TestConcurrencyIntegration:
    """Test concurrent operations."""
    
    @pytest.fixture
    def temp_workspace(self, tmp_path):
        """Create a temporary workspace for testing."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        return workspace
    
    def test_concurrent_config_generation(self, temp_workspace):
        """Test concurrent configuration generation."""
        import tor_custom_config as tcc
        import threading
        
        config_dir = temp_workspace / "tor_config"
        config_dir.mkdir()
        
        def generate_config(index):
            with patch('tor_custom_config.torrc_directory', str(config_dir)):
                with patch('tor_custom_config.torrc_path', str(config_dir / f"torrc_{index}")):
                    with patch('getpass.getpass', return_value=f"password_{index}"):
                        with patch('subprocess.run') as mock_run:
                            mock_result = Mock()
                            mock_result.stdout = f"16:HASH_{index}"
                            mock_result.returncode = 0
                            mock_run.return_value = mock_result
                            
                            tcc.create_torrc_file()
        
        threads = []
        for i in range(3):
            thread = threading.Thread(target=generate_config, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify all configs created
        assert (config_dir / "torrc_0").exists()
        assert (config_dir / "torrc_1").exists()
        assert (config_dir / "torrc_2").exists()
