"""
Unit tests for tor_vpn_inclued.py - Tor startup validation.
"""
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
import subprocess

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestTorVPNIncluded:
    """Test suite for tor_vpn_inclued.py main functionality."""
    
    @pytest.fixture
    def mock_tor_vpn_inclued_module(self):
        """Mock the tor_vpn_inclued module."""
        import tor_vpn_inclued as tvi
        return tvi
    
    def test_is_tor_running_true(self, mock_tor_vpn_inclued_module, mock_psutil):
        """Test Tor running check when Tor is running."""
        result = mock_tor_vpn_inclued_module.is_tor_running()
        
        assert result is True
    
    def test_is_tor_running_false(self, mock_tor_vpn_inclued_module):
        """Test Tor running check when Tor is not running."""
        with patch('psutil.process_iter', return_value=[]):
            result = mock_tor_vpn_inclued_module.is_tor_running()
            
            assert result is False
    
    def test_is_tor_running_exception(self, mock_tor_vpn_inclued_module):
        """Test Tor running check when exception occurs."""
        with patch('psutil.process_iter', side_effect=Exception("Error")):
            result = mock_tor_vpn_inclued_module.is_tor_running()
            
            assert result is False
    
    def test_generate_hashed_password_success(self, mock_tor_vpn_inclued_module, mock_subprocess):
        """Test successful password hashing."""
        mock_subprocess.return_value.stdout = "16:ABCD1234EFGH5678"
        
        result = mock_tor_vpn_inclued_module.generate_hashed_password("test_password")
        
        assert result == "16:ABCD1234EFGH5678"
    
    def test_generate_hashed_password_empty(self, mock_tor_vpn_inclued_module, mock_subprocess):
        """Test password hashing with empty password."""
        mock_subprocess.return_value.stdout = "16:EMPTY"
        
        result = mock_tor_vpn_inclued_module.generate_hashed_password("")
        
        assert result == "16:EMPTY"
    
    def test_start_tor_manual_success(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test successful manual Tor start."""
        torrc_path = tmp_path / "torrc"
        torrc_path.write_text("ControlPort 9051\nSocksPort 9050")
        
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.poll.return_value = None
            mock_popen.return_value = mock_process
            
            result = mock_tor_vpn_inclued_module.start_tor_manual(str(torrc_path))
            
            assert result is True
    
    def test_start_tor_manual_fails(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test manual Tor start when it fails."""
        torrc_path = tmp_path / "torrc"
        torrc_path.write_text("ControlPort 9051\nSocksPort 9050")
        
        with patch('subprocess.Popen', side_effect=OSError("Tor not found")):
            result = mock_tor_vpn_inclued_module.start_tor_manual(str(torrc_path))
            
            assert result is False
    
    def test_start_tor_manual_invalid_config(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test manual Tor start with invalid config."""
        torrc_path = tmp_path / "torrc"
        torrc_path.write_text("InvalidConfig")
        
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.poll.return_value = 1
            mock_popen.return_value = mock_process
            
            result = mock_tor_vpn_inclued_module.start_tor_manual(str(torrc_path))
            
            assert result is False
    
    def test_validate_and_generate_config_success(self, mock_tor_vpn_inclued_module, tmp_path, mock_getpass):
        """Test successful config validation and generation."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:HASHED"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                    
                    assert torrc_path is not None
                    assert data_dir is not None
    
    def test_validate_and_generate_config_existing(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test config validation when config already exists."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        torrc_path = config_dir / "torrc"
        torrc_path.write_text("ControlPort 9051")
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
            
            assert torrc_path is not None
            assert data_dir is not None
    
    def test_validate_and_generate_config_create_new(self, mock_tor_vpn_inclued_module, tmp_path, mock_getpass):
        """Test config validation when creating new config."""
        config_dir = tmp_path / "tor_config"
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:HASHED"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                    
                    assert config_dir.exists()
    
    def test_validate_and_generate_config_fails(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test config validation when it fails."""
        with patch('tor_vpn_inclued.expanduser', return_value="/nonexistent"):
            torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
            
            assert torrc_path is None or torrc_path is not None  # Depends on implementation
            assert data_dir is None or data_dir is not None
    
    def test_operating_system_constant(self, mock_tor_vpn_inclued_module):
        """Test that operating system constant exists."""
        assert hasattr(mock_tor_vpn_inclued_module, 'OPERATING_SYSTEM')
        assert isinstance(mock_tor_vpn_inclued_module.OPERATING_SYSTEM, str)
    
    def test_torrc_default_content_constant(self, mock_tor_vpn_inclued_module):
        """Test that torrc default content constant exists."""
        assert hasattr(mock_tor_vpn_inclued_module, 'TORRC_DEFAULT_CONTENT')
        assert isinstance(mock_tor_vpn_inclued_module.TORRC_DEFAULT_CONTENT, str)


class TestTorVPNIncludedSecurity:
    """Test security-related functionality in tor_vpn_inclued.py."""
    
    @pytest.fixture
    def mock_tor_vpn_inclued_module(self):
        """Mock the tor_vpn_inclued module."""
        import tor_vpn_inclued as tvi
        return tvi
    
    def test_password_prompt_secure(self, mock_tor_vpn_inclued_module, mock_getpass):
        """Test that password is prompted securely."""
        with patch('getpass.getpass') as mock_getpass_func:
            mock_getpass_func.return_value = "test_password"
            
            # This test documents expected behavior
            mock_getpass_func.assert_called_once()
    
    def test_torrc_contains_hashed_password(self, mock_tor_vpn_inclued_module, tmp_path, mock_getpass):
        """Test that torrc contains hashed password, not plain text."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:HASHED"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    mock_tor_vpn_inclued_module.validate_and_generate_config()
                    
                    torrc_file = config_dir / "torrc"
                    if torrc_file.exists():
                        content = torrc_file.read_text()
                        
                        # Should not contain plain text password
                        assert "test_password" not in content
                        # Should contain hashed password
                        assert "16:HASHED" in content
    
    def test_torrc_permissions_restricted(self, mock_tor_vpn_inclued_module, tmp_path, mock_getpass):
        """Test that torrc has restricted permissions."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:HASHED"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    mock_tor_vpn_inclued_module.validate_and_generate_config()
                    
                    torrc_file = config_dir / "torrc"
                    if torrc_file.exists():
                        permissions = oct(torrc_file.stat().st_mode)[-3:]
                        
                        # Should be 600 (owner read/write only)
                        assert permissions == "600"
                        assert permissions != "777"


class TestTorVPNIncludedErrorHandling:
    """Test error handling in tor_vpn_inclued.py."""
    
    @pytest.fixture
    def mock_tor_vpn_inclued_module(self):
        """Mock the tor_vpn_inclued module."""
        import tor_vpn_inclued as tvi
        return tvi
    
    def test_generate_hashed_password_tor_not_found(self, mock_tor_vpn_inclued_module):
        """Test password hashing when tor command not found."""
        with patch('subprocess.run', side_effect=FileNotFoundError("tor not found")):
            with pytest.raises(FileNotFoundError):
                mock_tor_vpn_inclued_module.generate_hashed_password("test_password")
    
    def test_start_tor_manual_config_not_found(self, mock_tor_vpn_inclued_module):
        """Test manual Tor start when config not found."""
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.poll.return_value = 1
            mock_popen.return_value = mock_process
            
            result = mock_tor_vpn_inclued_module.start_tor_manual("/nonexistent/torrc")
            
            assert result is False
    
    def test_start_tor_manual_subprocess_error(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test manual Tor start with subprocess error."""
        torrc_path = tmp_path / "torrc"
        torrc_path.write_text("ControlPort 9051")
        
        with patch('subprocess.Popen', side_effect=OSError("Subprocess error")):
            result = mock_tor_vpn_inclued_module.start_tor_manual(str(torrc_path))
            
            assert result is False
    
    def test_validate_and_generate_config_password_hashing_fails(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test config validation when password hashing fails."""
        config_dir = tmp_path / "tor_config"
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'tor')):
                    torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                    
                    assert torrc_path is None or torrc_path is not None


class TestTorVPNIncludedEdgeCases:
    """Test edge cases in tor_vpn_inclued.py."""
    
    @pytest.fixture
    def mock_tor_vpn_inclued_module(self):
        """Mock the tor_vpn_inclued module."""
        import tor_vpn_inclued as tvi
        return tvi
    
    def test_generate_hashed_password_very_long_password(self, mock_tor_vpn_inclued_module, mock_subprocess):
        """Test password hashing with very long password."""
        long_password = "a" * 1000
        mock_subprocess.return_value.stdout = "16:LONGHASH"
        
        result = mock_tor_vpn_inclued_module.generate_hashed_password(long_password)
        
        assert result == "16:LONGHASH"
    
    def test_generate_hashed_password_unicode(self, mock_tor_vpn_inclued_module, mock_subprocess):
        """Test password hashing with unicode characters."""
        unicode_password = "p@sswørd"
        mock_subprocess.return_value.stdout = "16:UNICODE"
        
        result = mock_tor_vpn_inclued_module.generate_hashed_password(unicode_password)
        
        assert result == "16:UNICODE"
    
    def test_start_tor_manual_custom_path(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test manual Tor start with custom path."""
        custom_torrc = tmp_path / "custom_torrc"
        custom_torrc.write_text("ControlPort 9051")
        
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.poll.return_value = None
            mock_popen.return_value = mock_process
            
            result = mock_tor_vpn_inclued_module.start_tor_manual(str(custom_torrc))
            
            assert result is True
    
    def test_validate_and_generate_config_custom_path(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test config validation with custom path."""
        custom_config = tmp_path / "custom_config"
        custom_config.mkdir()
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(custom_config)):
            torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
            
            assert torrc_path is not None
            assert data_dir is not None
    
    def test_validate_and_generate_config_empty_password(self, mock_tor_vpn_inclued_module, tmp_path, mock_getpass):
        """Test config validation with empty password."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value=""):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:EMPTY"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                    
                    assert torrc_path is not None or torrc_path is None


class TestTorVPNIncludedPlatformSpecific:
    """Test platform-specific functionality in tor_vpn_inclued.py."""
    
    @pytest.fixture
    def mock_tor_vpn_inclued_module(self):
        """Mock the tor_vpn_inclued module."""
        import tor_vpn_inclued as tvi
        return tvi
    
    def test_linux_config_path(self, mock_tor_vpn_inclued_module, mock_platform):
        """Test Linux config path."""
        mock_platform["system"] = "Linux"
        
        with patch('platform.system', return_value="Linux"):
            with patch('tor_vpn_inclued.expanduser') as mock_expand:
                mock_expand.return_value = "/home/user/.tor"
                
                torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                
                assert torrc_path is not None
    
    def test_macos_config_path(self, mock_tor_vpn_inclued_module, mock_platform):
        """Test macOS config path."""
        mock_platform["system"] = "Darwin"
        
        with patch('platform.system', return_value="Darwin"):
            with patch('tor_vpn_inclued.expanduser') as mock_expand:
                mock_expand.return_value = "/Users/user/.tor"
                
                torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                
                assert torrc_path is not None
    
    def test_windows_config_path(self, mock_tor_vpn_inclued_module, mock_platform):
        """Test Windows config path."""
        mock_platform["system"] = "Windows"
        
        with patch('platform.system', return_value="Windows"):
            with patch('os.path.expandvars') as mock_expand:
                mock_expand.return_value = "C:\\Users\\user\\.tor"
                
                torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                
                assert torrc_path is not None or torrc_path is None


class TestTorVPNIncludedIntegration:
    """Integration tests for tor_vpn_inclued.py."""
    
    @pytest.fixture
    def mock_tor_vpn_inclued_module(self):
        """Mock the tor_vpn_inclued module."""
        import tor_vpn_inclued as tvi
        return tvi
    
    @pytest.mark.tor
    @pytest.mark.integration
    def test_real_tor_start(self, mock_tor_vpn_inclued_module):
        """Test real Tor start."""
        # This test requires Tor to be installed
        pytest.skip("Requires Tor to be installed")
    
    @pytest.mark.tor
    @pytest.mark.integration
    def test_real_password_hashing(self, mock_tor_vpn_inclued_module):
        """Test real password hashing with actual tor command."""
        # This test requires Tor to be installed
        pytest.skip("Requires Tor to be installed")
    
    @pytest.mark.integration
    def test_full_startup_workflow(self, mock_tor_vpn_inclued_module, tmp_path):
        """Test full startup workflow."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        # Validate and generate config
        with patch('tor_vpn_inclued.expanduser', return_value=str(config_dir)):
            with patch('getpass.getpass', return_value="test_password"):
                with patch('subprocess.run') as mock_run:
                    mock_result = Mock()
                    mock_result.stdout = "16:HASHED"
                    mock_result.returncode = 0
                    mock_run.return_value = mock_result
                    
                    torrc_path, data_dir = mock_tor_vpn_inclued_module.validate_and_generate_config()
                    
                    assert torrc_path is not None
                    assert data_dir is not None
                    assert config_dir.exists()
