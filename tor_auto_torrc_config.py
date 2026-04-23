import os
import platform
import subprocess
import shutil
import sys

# Universal Tor Configuration File
TORRC_CONTENT = """
# Universal Tor Configuration File for Custom Software
ControlPort 9051
HashedControlPassword {hashed_password}
CookieAuthentication 1
SocksPort 9050
DataDirectory {data_directory}
Log notice file {log_directory}/notices.log
Log warn file {log_directory}/warnings.log
Log debug file {log_directory}/debug.log
"""

DEFAULT_DATA_DIR = "/var/lib/tor" if platform.system() != "Windows" else r"%APPDATA%\tor"
DEFAULT_LOG_DIR = "/var/log/tor" if platform.system() != "Windows" else r"%APPDATA%\tor\logs"
DEFAULT_USER_TORRC_PATH = os.path.expanduser("~/.tor/torrc")
IS_WINDOWS = platform.system() == "Windows"

DEFAULT_CONTROL_PASSWORD = "TorSecurePassword123!"


def check_if_tor_installed():
    """Check if Tor is already installed."""
    tor_bin = shutil.which("tor")
    if tor_bin:
        print(f"Tor is installed: {tor_bin}")
        return True
    print("Tor is not installed.")
    return False


def install_tor():
    """Install Tor depending on the operating system."""
    system = platform.system().lower()

    if system == "linux":
        print("Installing Tor on Linux...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "tor"], check=True)
    elif system == "darwin":
        print("Installing Tor on macOS...")
        subprocess.run(["brew", "install", "tor"], check=True)
    elif system == "windows":
        print("Please download and install Tor manually from https://www.torproject.org/.")
        exit(1)
    else:
        print(f"Unsupported system: {system}")
        exit(1)

    print("Tor installation completed.")


def generate_hashed_password(password):
    """Generate the hashed control password for Tor."""
    try:
        result = subprocess.run(
            ["tor", "--hash-password", password],
            text=True,
            capture_output=True,
            check=True
        )
        hashed_password = result.stdout.strip()
        print(f"Generated hashed password: {hashed_password}")
        return hashed_password
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate hashed password: {e}")
        exit(1)


def setup_directories(data_dir, log_dir):
    """Create necessary directories and set permissions."""
    print("Setting up directories...")

    # Create Data Directory
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        print(f"Created data directory: {data_dir}")
    else:
        print(f"Data directory already exists: {data_dir}")

    # Create Log Directory
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        print(f"Created log directory: {log_dir}")
    else:
        print(f"Log directory already exists: {log_dir}")


def apply_torrc(data_dir, log_dir, custom_torrc_path=None):
    """Generate and apply the custom torrc configuration file."""
    print("Creating and applying the custom torrc configuration file...")

    # Generate hashed control password
    hashed_password = generate_hashed_password(DEFAULT_CONTROL_PASSWORD)

    # Determine torrc path (default to user directory if not specified)
    torrc_path = custom_torrc_path or DEFAULT_USER_TORRC_PATH

    # Generate and write torrc file
    torrc_content = TORRC_CONTENT.format(
        data_directory=data_dir,
        log_directory=log_dir,
        hashed_password=hashed_password
    )

    # Ensure the directory for the torrc exists
    os.makedirs(os.path.dirname(torrc_path), exist_ok=True)

    with open(torrc_path, "w") as torrc_file:
        torrc_file.write(torrc_content)
    print(f"Custom torrc written to: {torrc_path}")


import getpass


def restart_tor():
    """Handle Tor service restart securely with password prompt."""
    print("Restarting Tor...")

    if IS_WINDOWS:
        print("Tor service management is not available on Windows. Please restart Tor manually.")
        return

    # Prompt the user for their sudo password securely
    try:
        password = getpass.getpass("Please enter your sudo password to restart Tor: ")
    except Exception as e:
        print(f"Error reading password: {e}")
        return

    if not password:
        print("Error: No password provided. Unable to restart Tor.")
        return

    # Attempt to restart Tor using the provided password
    try:
        process = subprocess.run(
            ["sudo", "-S", "/etc/init.d/tor", "restart"],
            input=password + "\n",  # Send the password followed by a newline
            text=True,
            capture_output=True,
            check=True
        )
        print("Tor restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Tor. Error: {e.stderr.strip()}")
        print("Please restart the Tor service manually using the following command:")
        print("    sudo /etc/init.d/tor restart")

def main():
    """Main function to automate Tor setup and configuration."""
    print("Automated Tor Setup and Configuration Script")
    print("===========================================")

    # Optional: Use command-line arguments for custom directories
    data_directory = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA_DIR
    log_directory = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_LOG_DIR
    torrc_path = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_USER_TORRC_PATH

    print(f"Using data directory: {data_directory}")
    print(f"Using log directory: {log_directory}")
    print(f"Using torrc path: {torrc_path}")

    # Check if Tor is installed
    if not check_if_tor_installed():
        install_tor()

    # Configure directories
    setup_directories(data_directory, log_directory)

    # Apply torrc configuration
    apply_torrc(data_directory, log_directory, custom_torrc_path=torrc_path)

    # Restart Tor to apply configuration
    restart_tor()

    print("Setup complete. Tor is now ready to use.")


if __name__ == "__main__":
    main()