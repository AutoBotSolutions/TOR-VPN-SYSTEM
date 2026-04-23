import logging
import os
import time
import platform
from stem.control import Controller
from stem import Signal
import requests
import subprocess
import socket

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_UNIX = not IS_WINDOWS

# Configuration
TORRC_PATHS = ["/etc/tor/torrc", "/usr/local/etc/tor/torrc", os.path.expanduser("~/.torrc")]  # Add common torrc paths
AUTH_COOKIE_PATHS = ["/run/tor/control.authcookie",
                     "/var/lib/tor/control_auth_cookie"]  # Add common Tor auth cookie paths

logging.basicConfig(level=logging.INFO)


def is_tor_running():
    """Check if the Tor service is running."""
    try:
        if IS_WINDOWS:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq tor.exe"],
                capture_output=True,
                text=True
            )
            if "tor.exe" in result.stdout:
                logging.info("Tor service is running.")
                return True
            else:
                logging.error("Tor service is not running. Please start the Tor service and try again.")
                return False
        else:
            result = subprocess.run(["pgrep", "-f", "tor"], capture_output=True, text=True)
            if result.stdout.strip():
                logging.info("Tor service is running.")
                return True
            else:
                logging.error("Tor service is not running. Please start the Tor service and try again.")
                return False
    except Exception as e:
        logging.error(f"Error checking Tor process: {e}")
        return False


def get_process_using_port(port):
    """Detects the process using the specified port."""
    try:
        if IS_WINDOWS:
            # Use netstat on Windows
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if f":{port}" in line and "LISTENING" in line:
                    logging.info(f"Detected process running on port {port}:\n{line}")
                    return line
            logging.warning(f"No process detected running on port {port}.")
            return None
        else:
            # Use lsof on Unix
            result = subprocess.run(
                ["lsof", "-i", f":{port}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                logging.info(f"Detected process running on port {port}:\n{result.stdout}")
                return result.stdout
            else:
                logging.warning(f"No process detected running on port {port}.")
                return None
    except Exception as e:
        logging.error(f"Failed to detect process on port {port}: {e}")
        return None


def check_port_status(host, port):
    """Check if the specified port is open and listening."""
    try:
        with socket.create_connection((host, port), timeout=2):
            logging.info(f"Port {port} is open and listening on {host}.")
            return True
    except ConnectionRefusedError:
        logging.error(f"Port {port} on {host} refused the connection.")
        return False
    except TimeoutError:
        logging.error(f"Connection to port {port} on {host} timed out.")
        return False
    except Exception as e:
        logging.error(f"Error checking port {port} on {host}: {e}")
        return False


def detect_tor_control_port():
    """Detect the Tor control port from the torrc file."""
    for torrc_path in TORRC_PATHS:
        try:
            with open(torrc_path, "r") as torrc_file:
                for line in torrc_file:
                    if line.startswith("ControlPort"):
                        port = int(line.split()[1])
                        logging.info(f"Detected ControlPort: {port} in {torrc_path}")
                        return port
        except FileNotFoundError:
            continue
    logging.warning("No ControlPort found in torrc. Using default: 9051.")
    return 9051


def detect_tor_password():
    """Tries to auto-detect the Tor Control Port password (if available)."""
    for torrc_path in TORRC_PATHS:
        try:
            with open(torrc_path, "r") as torrc_file:
                logging.info(f"Checking torrc file at: {torrc_path}")
                for line in torrc_file:
                    if "HashedControlPassword" in line:
                        logging.info("Detected hashed control password in torrc.")
                        return None  # Hashed passwords cannot be used directly for authentication
        except FileNotFoundError:
            continue  # Torrc not found, move to the next one

    logging.warning("No password found in torrc files.")
    return None


def detect_auth_cookie():
    """Tries to auto-detect the Tor Control Port authentication cookie."""
    for path in AUTH_COOKIE_PATHS:
        try:
            if os.path.exists(path):
                logging.info(f"Found control auth cookie at: {path}")
                return path
        except Exception as e:
            logging.error(f"Could not access the control auth cookie: {e}")

    logging.warning("No control auth cookie found.")
    return None


def is_control_port_accessible(port):
    """Check if the Tor control port is accessible."""
    try:
        with Controller.from_port(port=port) as controller:
            controller.close()
            logging.info(f"Control Port {port} is accessible.")
            return True
    except Exception as e:
        logging.error(f"Control Port {port} is not accessible: {e}")
        return False


def test_tor_connection():
    """Main function to test Tor network connectivity."""
    results = {
        "connection": False,
        "latency": None,
        "exit_ip": None,
        "errors": [],
    }

    # Check if Tor service is running
    if not is_tor_running():
        results["errors"].append("Tor service is not running.")
        return results

    # Detect Control Port
    tor_control_port = detect_tor_control_port()

    # Report what is running on the detected port
    process_details = get_process_using_port(tor_control_port)
    if process_details:
        logging.info(f"Process details for port {tor_control_port}:\n{process_details}")
    else:
        logging.warning(f"No process detected on port {tor_control_port}.")

    # Check if the port is open
    if not check_port_status("127.0.0.1", tor_control_port):
        results["errors"].append(
            f"Control Port {tor_control_port} is not open. Ensure the Tor process is binding to the port."
        )
        return results

    # Check if Control Port is accessible
    if not is_control_port_accessible(tor_control_port):
        results["errors"].append(f"Tor Control Port {tor_control_port} is not accessible.")
        return results

    # Try to auto-detect password or cookie
    detected_password = detect_tor_password()
    auth_cookie = detect_auth_cookie()

    try:
        # Connect to the Tor Controller
        with Controller.from_port(port=tor_control_port) as controller:
            if auth_cookie:
                controller.authenticate(cookie_path=auth_cookie)
                logging.info("Authenticated to Tor using control auth cookie.")
            elif detected_password:
                controller.authenticate(password=detected_password)
                logging.info("Authenticated to Tor using a detected password.")
            else:
                controller.authenticate()  # Attempt default authentication
                logging.info("Authenticated to Tor using default settings.")

            # Signal New Identity
            controller.signal(Signal.NEWNYM)
            logging.info("New Tor identity requested successfully.")
            results["connection"] = True

            # Test Latency
            start_time = time.monotonic()
            response = requests.get(
                "http://check.torproject.org",
                proxies={
                    "http": "socks5h://127.0.0.1:9050",
                    "https": "socks5h://127.0.0.1:9050",
                },
            )
            end_time = time.monotonic()
            results["latency"] = end_time - start_time

            if response.status_code == 200:
                logging.info("Tor is successfully routing traffic.")
                results["exit_ip"] = response.text.split("Your IP address appears to be: ")[1].split("<")[0]
                logging.info(f"Exit IP detected: {results['exit_ip']}")
            else:
                logging.error(f"Unexpected response from Tor check: {response.status_code}")
                results["errors"].append(f"Unexpected Tor check response: {response.status_code}")

            # Check Circuits
            circuits = controller.get_circuits()
            for circuit in circuits:
                logging.info(f"Circuit {circuit.id}: {circuit.purpose} | Build Flags: {circuit.build_flags}")

    except Exception as e:
        logging.error(f"Error during Tor network test: {e}")
        results["errors"].append(str(e))

    logging.info("Tor Network Test Results:")
    logging.info(results)
    return results


if __name__ == "__main__":
    # Call the test function when the script is executed directly
    test_tor_connection()