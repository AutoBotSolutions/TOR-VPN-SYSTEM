import os
import subprocess
import sys
import logging
import stat
import platform

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_UNIX = not IS_WINDOWS

# Directory and paths for custom torrc configuration
torrc_directory = os.path.join(os.path.expanduser("~"), ".tor_config")
torrc_path = os.path.join(torrc_directory, "torrc")

# Custom Tor configuration details
control_port = 9051
hashed_control_password = "16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD"
transparent_proxy_config = f"""
# Custom Tor configuration for transparent proxy
ControlPort {control_port}
HashedControlPassword {hashed_control_password}
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort 9040     # Transparent proxy port
DNSPort 5353       # DNS resolver port
"""

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("setup_tor.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)


def is_root():
    """Check if the script is being run as root."""
    if IS_WINDOWS:
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0


def stop_tor_if_running():
    """
    Checks if Tor is running and stops it if necessary.
    """
    print("[+] Checking if Tor is already running...")
    try:
        # Check for running Tor processes
        if IS_WINDOWS:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq tor.exe"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if "tor.exe" in result.stdout:
                print("[+] Found running Tor process. Stopping it...")
                subprocess.run(["taskkill", "/F", "/IM", "tor.exe"], check=True)
                print("[+] Successfully stopped Tor.")
            else:
                print("[+] No running instances of Tor detected.")
        else:
            result = subprocess.run(
                ["pgrep", "-x", "tor"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.stdout.strip():
                # Get the Tor process IDs
                tor_pids = result.stdout.strip().split("\n")
                print(f"[+] Found running Tor process(es): {', '.join(tor_pids)}. Stopping them...")

                # Terminate each Tor process
                for pid in tor_pids:
                    subprocess.run(["sudo", "kill", "-TERM", pid], check=True)
                print("[+] Successfully stopped running Tor instances.")
            else:
                print("[+] No running instances of Tor detected.")

    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to stop Tor process: {e}")
        sys.exit(1)


def create_directory(directory):
    """Create the specified directory if it doesn't exist, and set proper permissions."""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            os.chmod(directory, 0o700)  # Set permissions to 700
            logging.info(f"Directory created: {directory} with permissions 700")
        else:
            logging.info(f"Directory already exists: {directory}")
    except Exception as e:
        logging.error(f"Failed to create directory '{directory}': {e}")
        raise e


def create_torrc_file():
    """Create the torrc file, configure its permissions, and set ownership."""
    try:
        with open(torrc_path, "w") as file:
            file.write(transparent_proxy_config.strip())

        logging.info(f"Tor configuration file created at: {torrc_path}")

        # Set file permissions to 600
        os.chmod(torrc_path, 0o600)
        logging.info(f"Permissions for {torrc_path} set to 600")

        # Set ownership to the appropriate user (Unix only)
        if IS_UNIX:
            import getpass
            current_user = getpass.getuser()
            subprocess.run(["sudo", "chown", f"{current_user}:{current_user}", torrc_path], check=True)
            logging.info(f"Ownership for {torrc_path} set to '{current_user}'")
    except Exception as e:
        logging.error(f"Error in creating or configuring {torrc_path}: {e}")
        raise e


def install_packages():
    """Install necessary packages."""
    print("[+] Installing required packages...")
    try:
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "tor", "iptables-persistent"], check=True)
        print("[+] Required packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to install required packages: {e}")
        sys.exit(1)


def get_tor_uid():
    """Get the UID of the 'debian-tor' user."""
    try:
        result = subprocess.run(
            ["id", "-u", "debian-tor"], text=True, stdout=subprocess.PIPE, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to retrieve the UID of 'debian-tor': {e}")
        sys.exit(1)


def setup_iptables(tor_uid):
    """Set up iptables rules to redirect all traffic through Tor."""
    print("[+] Setting up iptables rules...")
    non_tor_network = "0.0.0.0/0"  # Replace with your local network range if needed

    try:
        # Flush iptables rules
        subprocess.run(["iptables", "-F"], check=True)
        subprocess.run(["iptables", "-t", "nat", "-F"], check=True)

        # Setup iptables rules
        commands = [
            ["iptables", "-t", "nat", "-A", "OUTPUT", "-o", "lo", "-j", "RETURN"],
            ["iptables", "-t", "nat", "-A", "OUTPUT", "-d", non_tor_network, "-j", "RETURN"],
            ["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "udp", "--dport", "53", "-j", "REDIRECT", "--to-ports",
             "5353"],
            ["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp", "--syn", "-j", "REDIRECT", "--to-ports", "9040"],
            ["iptables", "-t", "nat", "-A", "OUTPUT", "-m", "owner", "--uid-owner", tor_uid, "-j", "RETURN"],
            ["iptables", "-A", "OUTPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"],
            ["iptables", "-A", "OUTPUT", "-j", "REJECT"],
        ]

        for cmd in commands:
            subprocess.run(cmd, check=True)
        print("[+] iptables rules successfully set.")

        # Save for persistence
        subprocess.run(["iptables-save", ">", "/etc/iptables/rules.v4"], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to apply iptables rules: {e}")
        sys.exit(1)


def verify_tor_connection():
    """Verify that traffic is routed through Tor."""
    print("[+] Verifying Tor connection...")
    try:
        result = subprocess.run(
            ["curl", "-s", "https://check.torproject.org/"],
            text=True, stdout=subprocess.PIPE, check=True
        )
        if "Congratulations" in result.stdout:
            print("[+] Tor is working correctly. Traffic is routed through Tor.")
        else:
            print("[-] Tor is not set up correctly.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to verify Tor connection: {e}")


def main():
    """Main function."""
    if not is_root():
        print("[-] This script requires root privileges. Use 'sudo'.")
        sys.exit(1)

    print("[+] Starting Tor VPN setup script...")

    # Stop any existing Tor instances
    stop_tor_if_running()

    # Create directory & prepare torrc configuration
    create_directory(torrc_directory)
    create_torrc_file()

    # Install necessary packages
    install_packages()

    # Get the Tor user ID
    tor_uid = get_tor_uid()

    # Apply iptables rules
    setup_iptables(tor_uid)

    # Restart Tor with the custom configuration
    def restart_tor_with_custom_config():
        """Restart Tor with the custom torrc configuration."""
        print("[+] Restarting Tor with custom configuration...")
        try:
            # Stop Tor service using systemd or init.d
            if os.path.exists("/lib/systemd/system/tor.service"):
                subprocess.run(["sudo", "systemctl", "stop", "tor"], check=True)
            elif os.path.exists("/etc/init.d/tor"):
                subprocess.run(["sudo", "/etc/init.d/tor", "stop"], check=True)
            else:
                print("[-] Unable to locate Tor service management. Exiting.")
                sys.exit(1)

            # Use the custom configuration file to start Tor
            subprocess.run(["sudo", "tor", "-f", torrc_path], check=True)
            print("[+] Tor restarted successfully with custom configuration.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed to restart Tor with custom configuration: {e}")
            sys.exit(1)

    # Verify Tor connection
    verify_tor_connection()

    print("[+] Tor VPN setup complete. All traffic should route through Tor.")


if __name__ == "__main__":
    main()