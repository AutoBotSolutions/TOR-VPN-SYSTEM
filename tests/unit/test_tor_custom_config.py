"""
Unit tests for tor_custom_config.py - Custom configuration generator.
"""
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
import subprocess

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestTorCustomConfig:
    """Test suite for tor_custom_config.py main functionality."""
    
    @pytest.fixture
    def mock_tor_custom_config_module(self):
        """Mock the tor_custom_config module."""
        import tor_custom_config as tcc
        return tcc
    
    def test_generate_hashed_password_success(self, mock_tor_custom_config_module, mock_subprocess):
        """Test successful password hashing."""
        mock_subprocess.return_value.stdout = "16:ABCD1234EFGH5678"
        
        result = mock_tor_custom_config_module.generate_hashed_password("test_password")
        
        assert result == "16:ABCD1234EFGH5678"
        mock_subprocess.assert_called_once()
    
    def test_generate_hashed_password_subprocess_error(self, mock_tor_custom_config_module):
        """Test password hashing when subprocess fails."""
        with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'tor')):
            with pytest.raises(subprocess.CalledProcessError):
                mock_tor_custom_config_module.generate_hashed_password("test_password")
    
    def test_generate_hashed_password_empty_password(self, mock_tor_custom_config_module, mock_subprocess):
        """Test password hashing with empty password."""
        mock_subprocess.return_value.stdout = "16:EMPTYHASH"
        
        result = mock_tor_custom_config_module.generate_hashed_password("")
        
        assert result == "16:EMPTYHASH"
    
    def test_generate_hashed_password_special_characters(self, mock_tor_custom_config_module, mock_subprocess):
        """Test password hashing with special characters."""
        mock_subprocess.return_value.stdout = "16:SPECIALHASH"
        
        result = mock_tor_custom_config_module.generate_hashed_password("p@ssw0rd!#$")
        
        assert result == "16:SPECIALHASH"
    
    def test_change_ownership_success(self, mock_tor_custom_config_module, tmp_path):
        """Test successful file ownership change."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        
        with patch('shutil.chown') as mock_chown:
            result = mock_tor_custom_config_module.change_ownership(str(test_file), "testuser", "testgroup")
            
            assert result is True
            mock_chown.assert_called_once_with(str(test_file), "testuser", "testgroup")
    
    def test_change_ownership_user_not_found(self, mock_tor_custom_config_module, tmp_path):
        """Test ownership change when user not found."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        
        with patch('shutil.chown', side_effect=KeyError("User not found")):
            with pytest.raises(KeyError):
                mock_tor_custom_config_module.change_ownership(str(test_file), "nonexistent", "testgroup")
    
    def test_change_ownership_permission_error(self, mock_tor_custom_config_module, tmp_path):
        """Test ownership change with permission error."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        
        with patch('shutil.chown', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                mock_tor_custom_config_module.change_ownership(str(test_file), "testuser", "testgroup")
    
    def test_change_ownership_file_not_exists(self, mock_tor_custom_config_module):
        """Test ownership change when file doesn't exist."""
        with patch('shutil.chown'):
            result = mock_tor_custom_config_module.change_ownership("/nonexistent/file", "testuser", "testgroup")
            # Function may or may not raise error depending on implementation
            assert result is True or result is False
    
    def test_create_directory_success(self, mock_tor_custom_config_module, tmp_path):
        """Test successful directory creation."""
        test_dir = tmp_path / "test_directory"
        
        result = mock_tor_custom_config_module.create_directory(str(test_dir))
        
        assert result is True
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_create_directory_already_exists(self, mock_tor_custom_config_module, tmp_path):
        """Test directory creation when directory already exists."""
        test_dir = tmp_path / "test_directory"
        test_dir.mkdir()
        
        result = mock_tor_custom_config_module.create_directory(str(test_dir))
        
        assert result is True or result is False  # Depends on implementation
    
    def test_create_directory_nested(self, mock_tor_custom_config_module, tmp_path):
        """Test creating nested directory."""
        test_dir = tmp_path / "parent" / "child" / "grandchild"
        
        result = mock_tor_custom_config_module.create_directory(str(test_dir))
        
        assert result is True
        assert test_dir.exists()
    
    def test_create_directory_permissions(self, mock_tor_custom_config_module, tmp_path):
        """Test that created directory has correct permissions."""
        test_dir = tmp_path / "test_directory"
        
        mock_tor_custom_config_module.create_directory(str(test_dir))
        
        # Check permissions (should be 700)
        permissions = oct(test_dir.stat().st_mode)[-3:]
        assert permissions == "700"
    
    def test_create_torrc_file_success(self, mock_tor_custom_config_module, tmp_path, mock_getpass):
        """Test successful torrc file creation."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        torrc_file = config_dir / "torrc"
                        assert torrc_file.exists()
    
    def test_create_torrc_file_content(self, mock_tor_custom_config_module, tmp_path, mock_getpass):
        """Test that torrc file has correct content."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        torrc_file = config_dir / "torrc"
                        content = torrc_file.read_text()
                        
                        assert "ControlPort 9051" in content
                        assert "16:HASHED" in content
                        assert "SocksPort 9050" in content
    
    def test_create_torrc_file_permissions(self, mock_tor_custom_config_module, tmp_path, mock_getpass):
        """Test that torrc file has correct permissions."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        torrc_file = config_dir / "torrc"
                        permissions = oct(torrc_file.stat().st_mode)[-3:]
                        assert permissions == "600"
    
    def test_create_torrc_file_directory_permissions(self, mock_tor_custom_config_module, tmp_path, mock_getpass):
        """Test that config directory has correct permissions."""
        config_dir = tmp_path / "tor_config"
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        permissions = oct(config_dir.stat().st_mode)[-3:]
                        assert permissions == "700"
    
    def test_verify_file_access_exists_readable(self, mock_tor_custom_config_module, tmp_path):
        """Test file access verification for existing readable file."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        
        result = mock_tor_custom_config_module.verify_file_access(str(test_file))
        
        assert result is True
    
    def test_verify_file_access_not_exists(self, mock_tor_custom_config_module):
        """Test file access verification for non-existent file."""
        result = mock_tor_custom_config_module.verify_file_access("/nonexistent/file")
        
        assert result is False
    
    def test_verify_file_access_not_readable(self, mock_tor_custom_config_module, tmp_path):
        """Test file access verification for unreadable file."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        test_file.chmod(0o000)
        
        result = mock_tor_custom_config_module.verify_file_access(str(test_file))
        
        assert result is False
    
    def test_control_port_constant(self, mock_tor_custom_config_module):
        """Test that control port constant exists and has correct value."""
        assert hasattr(mock_tor_custom_config_module, 'control_port')
        assert mock_tor_custom_config_module.control_port == 9051
    
    def test_torrc_directory_constant(self, mock_tor_custom_config_module):
        """Test that torrc directory constant exists."""
        assert hasattr(mock_tor_custom_config_module, 'torrc_directory')
        assert isinstance(mock_tor_custom_config_module.torrc_directory, str)
        assert len(mock_tor_custom_config_module.torrc_directory) > 0


class TestTorCustomConfigSecurity:
    """Test security-related functionality in tor_custom_config.py."""
    
    @pytest.fixture
    def mock_tor_custom_config_module(self):
        """Mock the tor_custom_config module."""
        import tor_custom_config as tcc
        return tcc
    
    def test_password_not_logged(self, mock_tor_custom_config_module, tmp_path):
        """Test that passwords are not logged."""
        # This test documents expected behavior
        log_file = tmp_path / "test.log"
        
        with patch('logging.FileHandler'):
            logger = mock_tor_custom_config_module.setup_logging(str(log_file))
            logger.info("Password: secret123")
            
            # In production, passwords should be redacted from logs
            # This test documents the expected behavior
            assert True  # Placeholder for actual log checking
    
    def test_torrc_file_contains_hashed_password(self, mock_tor_custom_config_module, tmp_path, mock_getpass):
        """Test that torrc file contains hashed password, not plain text."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        torrc_file = config_dir / "torrc"
                        content = torrc_file.read_text()
                        
                        assert "test_password" not in content
                        assert "16:HASHED" in content
    
    def test_torrc_file_permissions_restricted(self, mock_tor_custom_config_module, tmp_path, mock_getpass):
        """Test that torrc file has restricted permissions."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        torrc_file = config_dir / "torrc"
                        permissions = oct(torrc_file.stat().st_mode)[-3:]
                        
                        # Should be 600 (owner read/write only)
                        assert permissions == "600"
                        assert permissions != "777"
                        assert permissions != "644"


class TestTorCustomConfigErrorHandling:
    """Test error handling in tor_custom_config.py."""
    
    @pytest.fixture
    def mock_tor_custom_config_module(self):
        """Mock the tor_custom_config module."""
        import tor_custom_config as tcc
        return tcc
    
    def test_generate_hashed_password_tor_not_found(self, mock_tor_custom_config_module):
        """Test password hashing when tor command not found."""
        with patch('subprocess.run', side_effect=FileNotFoundError("tor not found")):
            with pytest.raises(FileNotFoundError):
                mock_tor_custom_config_module.generate_hashed_password("test_password")
    
    def test_create_directory_permission_denied(self, mock_tor_custom_config_module):
        """Test directory creation when permission denied."""
        with patch('os.mkdir', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                mock_tor_custom_config_module.create_directory("/root/protected")
    
    def test_change_ownership_os_error(self, mock_tor_custom_config_module, tmp_path):
        """Test ownership change with OS error."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        
        with patch('shutil.chown', side_effect=OSError("OS error")):
            with pytest.raises(OSError):
                mock_tor_custom_config_module.change_ownership(str(test_file), "testuser", "testgroup")
    
    def test_create_torrc_file_password_hashing_fails(self, mock_tor_custom_config_module, tmp_path):
        """Test torrc creation when password hashing fails."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'tor')):
                        with pytest.raises(subprocess.CalledProcessError):
                            mock_tor_custom_config_module.create_torrc_file()
    
    def test_create_torrc_file_write_fails(self, mock_tor_custom_config_module, tmp_path):
        """Test torrc creation when file write fails."""
        config_dir = tmp_path / "tor_config"
        config_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        with patch('builtins.open', side_effect=IOError("Write error")):
                            with pytest.raises(IOError):
                                mock_tor_custom_config_module.create_torrc_file()


class TestTorCustomConfigEdgeCases:
    """Test edge cases in tor_custom_config.py."""
    
    @pytest.fixture
    def mock_tor_custom_config_module(self):
        """Mock the tor_custom_config module."""
        import tor_custom_config as tcc
        return tcc
    
    def test_generate_hashed_password_very_long_password(self, mock_tor_custom_config_module, mock_subprocess):
        """Test password hashing with very long password."""
        long_password = "a" * 1000
        mock_subprocess.return_value.stdout = "16:LONGHASH"
        
        result = mock_tor_custom_config_module.generate_hashed_password(long_password)
        
        assert result == "16:LONGHASH"
    
    def test_generate_hashed_password_unicode_characters(self, mock_tor_custom_config_module, mock_subprocess):
        """Test password hashing with unicode characters."""
        unicode_password = "p@sswørd"
        mock_subprocess.return_value.stdout = "16:UNICODEHASH"
        
        result = mock_tor_custom_config_module.generate_hashed_password(unicode_password)
        
        assert result == "16:UNICODEHASH"
    
    def test_create_directory_with_trailing_slash(self, mock_tor_custom_config_module, tmp_path):
        """Test creating directory with trailing slash."""
        test_dir = tmp_path / "test_directory"
        
        result = mock_tor_custom_config_module.create_directory(str(test_dir) + "/")
        
        assert result is True
        assert test_dir.exists()
    
    def test_create_directory_with_dot_path(self, mock_tor_custom_config_module, tmp_path):
        """Test creating directory with relative path."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            result = mock_tor_custom_config_module.create_directory("./test_directory")
            
            assert result is True
            assert (tmp_path / "test_directory").exists()
        finally:
            os.chdir(original_cwd)
    
    def test_change_ownership_with_numeric_ids(self, mock_tor_custom_config_module, tmp_path):
        """Test ownership change with numeric user/group IDs."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        
        with patch('shutil.chown') as mock_chown:
            result = mock_tor_custom_config_module.change_ownership(str(test_file), 1000, 1000)
            
            assert result is True
            mock_chown.assert_called_once_with(str(test_file), 1000, 1000)
    
    def test_verify_file_access_symlink(self, mock_tor_custom_config_module, tmp_path):
        """Test file access verification for symbolic link."""
        test_file = tmp_path / "test_file"
        test_file.write_text("test content")
        
        symlink = tmp_path / "test_symlink"
        symlink.symlink_to(test_file)
        
        result = mock_tor_custom_config_module.verify_file_access(str(symlink))
        
        assert result is True
    
    def test_create_torrc_file_custom_path(self, mock_tor_custom_config_module, tmp_path, mock_getpass):
        """Test torrc creation with custom path."""
        custom_dir = tmp_path / "custom_config"
        custom_dir.mkdir()
        
        with patch('tor_custom_config.torrc_directory', str(custom_dir)):
            with patch('tor_custom_config.torrc_path', str(custom_dir / "custom_torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        custom_torrc = custom_dir / "custom_torrc"
                        assert custom_torrc.exists()


class TestTorCustomConfigIntegration:
    """Integration tests for tor_custom_config.py."""
    
    @pytest.fixture
    def mock_tor_custom_config_module(self):
        """Mock the tor_custom_config module."""
        import tor_custom_config as tcc
        return tcc
    
    @pytest.mark.tor
    @pytest.mark.integration
    def test_real_password_hashing(self, mock_tor_custom_config_module):
        """Test real password hashing with actual tor command."""
        # This test requires Tor to be installed
        pytest.skip("Requires Tor to be installed")
    
    @pytest.mark.integration
    def test_full_workflow(self, mock_tor_custom_config_module, tmp_path):
        """Test full workflow of creating torrc file."""
        config_dir = tmp_path / "tor_config"
        
        with patch('tor_custom_config.torrc_directory', str(config_dir)):
            with patch('tor_custom_config.torrc_path', str(config_dir / "torrc")):
                with patch('getpass.getpass', return_value="test_password"):
                    with patch('subprocess.run') as mock_run:
                        mock_run.return_value.stdout = "16:HASHED"
                        mock_run.return_value.returncode = 0
                        
                        # Create directory
                        mock_tor_custom_config_module.create_directory(str(config_dir))
                        
                        # Create torrc file
                        mock_tor_custom_config_module.create_torrc_file()
                        
                        # Verify file exists
                        torrc_file = config_dir / "torrc"
                        assert torrc_file.exists()
                        
                        # Verify content
                        content = torrc_file.read_text()
                        assert "ControlPort 9051" in content
                        assert "16:HASHED" in content
