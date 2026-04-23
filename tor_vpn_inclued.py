import os
import platform
import subprocess
import logging
import shutil
import getpass
import time

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

TORRC_DEFAULT_CONTENT = """SocksPort 9050
ControlPort 9051
HashedControlPassword {hashed_password}
DataDirectory {data_directory}
"""

OPERATING_SYSTEM = platform.system()


def is_tor_running():
    """Check if Tor is running."""
    try:
        if OPERATING_SYSTEM == "Windows":
            result = subprocess.run(
                ["tasklist"],
                stdout=subprocess.PIPE,
                text=True,
            )
            if "tor.exe" in result.stdout:
                logging.info("Tor is running.")
                return True
        else:  # Linux/macOS
            result = subprocess.run(
                ["pidof", "tor"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                logging.info("Tor is running.")
                return True
        return False
    except Exception as e:
        logging.error(f"Failed to check if Tor is running: {e}")
        return False


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
        logging.info(f"Generated hashed password: {hashed_password}")
        return hashed_password
    except Exception as e:
        logging.error(f"Failed to generate hashed password: {e}")
        raise


def start_tor_manual(torrc_path):
    """Start Tor manually without relying on system services."""
    try:
        tor_path = shutil.which("tor")
        if not tor_path:
            raise FileNotFoundError("Tor executable not found in PATH.")

        # Start Tor process manually
        logging.info(f"Starting Tor manually using configuration file: {torrc_path}")
        process = subprocess.Popen(
            [tor_path, "-f", torrc_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        time.sleep(5)  # Give it time to start
        if process.poll() is None:  # Check if the process is still running
            logging.info("Tor started successfully in manual mode.")
            return True
        else:
            error_output, _ = process.communicate()
            raise RuntimeError(f"Tor failed to start: {error_output}")
    except Exception as e:
        logging.error(f"Error manually starting Tor: {e}")
        return False


def validate_and_generate_config():
    """Validate and generate the Tor configuration file if missing."""
    try:
        # Determine the torrc configuration directory
        if OPERATING_SYSTEM == "Windows":
            tor_directory = os.path.expandvars(r"%APPDATA%\tor")
        elif OPERATING_SYSTEM == "Darwin":  # macOS
            tor_directory = os.path.expanduser("~/Library/Application Support/Tor")
        else:  # Linux
            tor_directory = os.path.expanduser("~/.tor")

        # Ensure DataDirectory exists
        data_directory = os.path.join(tor_directory, "data")
        os.makedirs(data_directory, exist_ok=True)

        # Prompt for a password
        plain_password = getpass.getpass("Enter a password for Tor control port access: ")
        hashed_password = generate_hashed_password(plain_password)

        # Check or create torrc
        torrc_path = os.path.join(tor_directory, "torrc")
        if not os.path.exists(torrc_path):
            logging.warning(f"Missing torrc file. Generating default torrc at {torrc_path}.")
            with open(torrc_path, "w") as f:
                f.write(
                    TORRC_DEFAULT_CONTENT.format(
                        data_directory=data_directory,
                        hashed_password=hashed_password
                    )
                )
        else:
            logging.info(f"Found existing torrc at {torrc_path}.")
            # Optionally: Append the hashed password if it doesn't already exist.

        return torrc_path, data_directory
    except Exception as e:
        logging.error(f"Error validating or generating configuration files: {e}")
        return None, None


def main():
    """Main execution flow."""
    try:
        if is_tor_running():
            print("Tor is already running.")
            return

        print("Tor is not running. Attempting to start...")
        torrc_path, data_directory = validate_and_generate_config()
        if not torrc_path or not data_directory:
            raise RuntimeError("Failed to validate or generate configuration files.")

        print("Retrying to start Tor manually...")
        if not start_tor_manual(torrc_path):
            raise RuntimeError("Failed to start Tor even after configuration validation.")

        print("Tor started successfully.")
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()