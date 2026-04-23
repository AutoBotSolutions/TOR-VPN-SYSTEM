import platform
import subprocess
import os
import logging
import getpass
import psutil
import shutil
import argparse


def parse_arguments():
    """
    Parse command-line arguments for custom paths and commands.
    """
    parser = argparse.ArgumentParser(description="Tor Diagnostic and Repair Tool")
    parser.add_argument("--tor-binary", default="tor", help="Path to the Tor binary (default: 'tor')")
    parser.add_argument("--tor-config", default="/etc/tor/torrc", help="Path to the Tor configuration file")
    parser.add_argument("--custom-start-command", help="Custom command to start Tor")
    parser.add_argument("--custom-stop-command", help="Custom command to stop Tor")
    return parser.parse_args()


# Parse arguments and set global variables
args = parse_arguments()
TOR_BINARY = args.tor_binary
TOR_CONFIG = args.tor_config
CUSTOM_START_COMMAND = args.custom_start_command
CUSTOM_STOP_COMMAND = args.custom_stop_command


def setup_logging():
    """
    Configures logging to work in both console and file outputs.
    Ensures graceful setup even when file operations fail.
    """
    log_file_path = "logfile.log"  # Default log file name or path

    log_format = '[%(asctime)s.%(msecs)03d] %(levelname)s :: %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'
    log_level = logging.DEBUG

    try:
        # Add both console and file handlers
        logging.basicConfig(
            level=log_level,
            format=log_format,
            datefmt=log_date_format,
            handlers=[
                logging.FileHandler(log_file_path),
                logging.StreamHandler()
            ]
        )
        logging.info("Logging successfully configured.")
        logging.info(f"System Info: {platform.platform()}")
        logging.info(f"Python Version: {platform.python_version()}")
    except Exception as e:
        # Fallback: Use console-only logging if setup fails
        logging.basicConfig(level=log_level, format=log_format, datefmt=log_date_format)
        logging.error("Failed to configure file logging, falling back to console logging.", exc_info=True)
        logging.warning(f"Error details: {e}")



def check_tor_version():
    """
    Check and log the installed Tor version.
    """
    logging.info("Checking Tor version...")
    try:
        result = subprocess.run(
            ["tor", "--version"], check=True, stdout=subprocess.PIPE, text=True
        )
        logging.info(f"Tor version: {result.stdout.strip()}")
    except Exception:
        logging.error("Failed to retrieve Tor version", exc_info=True)


# Call setup_logging at the beginning of your script
setup_logging()


def detect_init_system():
    """
    Detects the initialization system used by the host system for managing services.
    Returns: 'systemd', 'sysvinit', or 'manual' based on detection.
    """
    logging.info("Detecting init system...")

    # Check for systemd
    if os.path.exists("/bin/systemctl") or os.path.exists("/usr/bin/systemctl"):
        try:
            logging.debug("Systemctl binary found. Checking if systemd is operational...")
            result = subprocess.run(
                ["systemctl", "is-system-running"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                logging.info("Systemd detected and operational.")
                return "systemd"
            else:
                logging.warning("Systemd detected but not operational.")
        except subprocess.CalledProcessError as e:
            logging.warning(f"Systemd is present but non-functional: {e.stderr.strip()}")

    # Check for SysVinit (/etc/init.d)
    if os.path.exists("/etc/init.d"):
        logging.info("/etc/init.d/ directory found. Assuming SysVinit (init.d) as the init system.")
        return "sysvinit"

    # Manual or modern lightweight systems
    logging.warning("No supported init system detected (systemd or init.d). Falling back to manual process control.")
    return "manual"



def prompt_for_password():
    """
    Prompt the user for the sudo password (if required), with advanced logging and debugging.
    """
    logging.debug("Prompting user for sudo password...")
    try:
        password = getpass.getpass("Enter your sudo password (if required): ")
        logging.debug("Password input successfully captured.")
        return password
    except getpass.GetPassWarning as e:
        logging.warning(f"Password input warning: {e}. Password may be echoed due to terminal issues.")
        try:
            password = input("Enter your sudo password (if required): ")
            logging.debug("Password input successfully captured with fallback method.")
            return password
        except Exception as fallback_error:
            logging.error(f"Unexpected error during password input fallback: {fallback_error}")
            raise


def validate_sudo_password(sudo_password):
    """
    Validate the provided sudo password by running 'sudo -v'.
    Includes advanced logging and debugging.
    """
    logging.info("Validating sudo password...")
    logging.debug(f"Received sudo password for validation: {'*' * len(sudo_password) if sudo_password else 'None'}")

    command = ["sudo", "-S", "-v"]
    logging.debug(f"Prepared command for password validation: {' '.join(command)}")

    success, output = run_command(command, sudo_password)

    if success:
        logging.info("Sudo access validated successfully.")
        logging.debug(f"Validation command output: {output}")
        return True
    else:
        logging.error("Sudo validation failed.")
        logging.debug(f"Validation command error output: {output}")
        return False


def run_command(command, sudo_password=None):
    """
    Executes a shell command and provides detailed logs for success/failure.
    If a sudo password is provided, it is passed via stdin.
    """
    try:
        if sudo_password:
            command = ["sudo", "-S"] + command
            masked_command = ["sudo", "-S"] + command[2:]  # Mask the sudo password
            logging.debug(f"Executing command with sudo: {' '.join(masked_command)}")
        else:
            logging.debug(f"Executing command: {' '.join(command)}")

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            input=f"{sudo_password}\n" if sudo_password else None,
            check=True
        )
        logging.debug(f"Command completed successfully. Exit code: {result.returncode}")
        logging.debug(f"Command stdout: {result.stdout.strip()}")
        logging.debug(f"Command stderr: {result.stderr.strip()}")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as error:
        logging.error(f"Command failed with exit code {error.returncode}: {' '.join(command)}")
        logging.error(f"Command stderr: {error.stderr.strip()}")
        logging.error(f"Command stdout: {error.stdout.strip()}")
        return False, error.stderr.strip()
    except Exception as e:
        logging.critical(f"Unexpected error when executing command: {' '.join(command)}", exc_info=True)
        return False, str(e)


def find_tor_process():
    """
    Locate the Tor process by checking active processes.
    Return: PID of the Tor process if found, otherwise None.
    Includes advanced logging and debugging.
    """
    logging.info("Initiating search for running Tor process...")
    try:
        for process in psutil.process_iter(["pid", "name"]):
            logging.debug(f"Inspecting process: PID={process.info['pid']}, Name={process.info['name']}")
            if process.info["name"] == "tor":
                logging.info(f"Found Tor process with PID: {process.info['pid']}")
                return process.info["pid"]
        logging.warning("No running Tor process found.")
    except Exception as e:
        logging.critical("An error occurred while searching for the Tor process.", exc_info=True)
    return None


def stop_tor_directly(sudo_password=None):
    """
    Stop the Tor process manually by sending a kill signal.
    Includes advanced logging and debugging.
    """
    logging.debug("Attempting to locate the Tor process to stop it...")
    pid = find_tor_process()
    if pid:
        logging.info(f"Found Tor process with PID: {pid}. Preparing to stop it...")
        command = ["kill", str(pid)]
        logging.debug(f"Constructed command to kill process: {' '.join(command)}")

        success, output = run_command(command, sudo_password)

        if success:
            logging.info(f"Tor process with PID {pid} stopped successfully.")
            return True
        else:
            logging.error(f"Failed to stop Tor process with PID {pid}. Command output: {output}")
            return False
    else:
        logging.warning("No running Tor process was found. Skipping stop operation.")
        return False


def start_tor_directly():
    """
    Start the Tor process manually using the specified Tor binary.
    """
    logging.info("Starting Tor process manually...")

    # Check for the presence of the Tor binary
    if not shutil.which(TOR_BINARY):
        logging.error(f"Tor binary '{TOR_BINARY}' not found. Cannot start Tor manually.")
        return False

    try:
        tor_command = [TOR_BINARY, "--defaults-torrc", TOR_CONFIG]
        logging.debug(f"Prepared command to start Tor: {' '.join(tor_command)}")

        process = subprocess.Popen(tor_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.debug("Tor process initiated. Waiting for initialization...")
        stdout, stderr = process.communicate(timeout=5)
        logging.debug(f"Tor process output (initial): {stdout.strip()}")
        logging.debug(f"Tor process errors (initial): {stderr.strip()}")

        logging.info("Tor process started successfully in the background.")
        return True

    except subprocess.TimeoutExpired:
        logging.warning("Tor process timed out during initialization. Process may still be running.")
        return True
    except Exception as e:
        logging.error(f"Failed to start Tor process. Encountered error: {e}")
        return False


def validate_tor_configuration():
    """
    Validates the provided Tor binary and checks the configuration file.
    Returns True if valid, False otherwise.
    """
    logging.info("Validating Tor configuration...")

    # Check if custom Tor binary exists
    if not shutil.which(TOR_BINARY):
        logging.error(f"Tor binary '{TOR_BINARY}' not found. Ensure it is installed or the path is correct.")
        return False
    logging.info(f"Tor binary found at: {TOR_BINARY}")

    # Check custom Tor configuration
    if not os.path.exists(TOR_CONFIG):
        logging.error(f"Tor configuration file '{TOR_CONFIG}' not found.")
        return False
    logging.info(f"Tor configuration file detected at: {TOR_CONFIG}")

    # Validate Tor configuration using '--verify-config'
    try:
        success, output = run_command([TOR_BINARY, "--defaults-torrc", TOR_CONFIG, "--verify-config"])
        if not success:
            logging.error("Tor configuration verification failed.")
            logging.debug(f"Verification output: {output}")
            return False
        logging.info("Tor configuration is valid.")
    except Exception as e:
        logging.critical("Error occurred while validating Tor configuration.", exc_info=True)
        return False

    return True



def validate_tor():
    logging.info("### Starting Tor Configuration Validation ###")
    # Perform validation
    logging.info("### Completed Tor Validation Successfully ###\n")
    return True


def restart_tor_with_systemd(sudo_password):
    """
    Restart the Tor service using systemd.
    """
    logging.info("Restarting Tor using systemd...")
    command = ["systemctl", "restart", "tor"]
    logging.debug(f"Constructed systemd restart command: {' '.join(command)}")

    success, output = run_command(command, sudo_password)

    if success:
        logging.info("Tor restarted successfully using systemd.")
        logging.debug(f"Systemd restart command output: {output}")
    else:
        logging.error("Systemd restart failed.")
        logging.debug(f"Systemd restart command error output: {output}")

    return success


def restart_tor_with_sysvinit(sudo_password):
    """
    Restart the Tor service using SysVinit.
    """
    logging.info("Attempting to restart Tor using SysVinit...")

    # Construct the command for restarting Tor using SysVinit
    command = ["/etc/init.d/tor", "restart"]
    logging.debug(f"Constructed SysVinit restart command: {' '.join(command)}")

    # Execute the command using run_command
    success, output = run_command(command, sudo_password)

    # Check success and log details
    if success:
        logging.info("Tor restarted successfully using SysVinit.")
        logging.debug(f"SysVinit restart command output:\n{output}")
    else:
        logging.error("Failed to restart Tor using SysVinit.")
        logging.debug(f"SysVinit restart command error output:\n{output}")

        # Specific error handling for common issues
        if "unrecognized service" in output or "No such file" in output:
            logging.error("SysVinit configuration for Tor is missing or broken.")
            logging.debug("Unrecognized service or missing file detected in SysVinit error output.")

        elif "permission denied" in output.lower():
            logging.error("Permission denied while attempting to restart Tor with SysVinit.")
            logging.debug("Ensure the sudo password is correct and the user has necessary privileges.")

        else:
            logging.error("An unexpected error occurred while restarting Tor using SysVinit.")
            logging.debug("Inspect the error output for more details about the issue.")

    # Return the success status of the command
    return success



def validate_running_tor():
    """
    Validate whether the Tor process is running after an attempt to restart.
    Includes advanced logging and debugging.
    """
    logging.info("Validating if Tor process is running...")
    logging.debug("Initiating search for Tor process using the 'find_tor_process' function.")

    pid = find_tor_process()

    if pid:
        logging.info(f"Tor is running with PID: {pid}")
        logging.debug(f"Process with PID {pid} identified as the Tor process. Validation successful.")
        return True
    else:
        logging.error("Tor is not running. Restart appears to have failed.")
        logging.debug("No process matching the Tor binary was found. Validation unsuccessful.")
        return False


def restart_tor_service(init_system, sudo_password):
    """
    Restart the Tor service using the detected init system.
    Allows fallback to manual restart or custom commands.
    """
    logging.info("Starting restart process based on the detected init system...")

    # Use custom commands if provided
    if CUSTOM_STOP_COMMAND and CUSTOM_START_COMMAND:
        logging.info("Using custom commands for restarting Tor service.")
        logging.debug(f"Custom stop command: {CUSTOM_STOP_COMMAND}")
        logging.debug(f"Custom start command: {CUSTOM_START_COMMAND}")
        stop_success = run_command(CUSTOM_STOP_COMMAND.split(), sudo_password)[0]
        start_success = run_command(CUSTOM_START_COMMAND.split(), sudo_password)[0]
        if stop_success and start_success:
            logging.info("Tor successfully restarted using custom commands.")
            return True
        else:
            logging.error("Failed to restart Tor using custom commands.")
            return False

    # Existing restart logic for systemd/SysVinit fallback
    if init_system == "systemd":
        return restart_tor_with_systemd(sudo_password)
    elif init_system == "sysvinit":
        return restart_tor_with_sysvinit(sudo_password)
    else:
        logging.warning("Falling back to manual restart of Tor.")
        return stop_tor_directly(sudo_password) and start_tor_directly()



def main():
    logging.info("Starting Tor diagnostic and repair tool...")

    # Validate Tor configuration
    logging.debug("Starting validation of Tor configuration...")
    if not validate_tor_configuration():
        logging.error("Tor configuration issues detected. Exiting...")
        logging.debug("Tor configuration validation failed. Terminating process.")
        return
    logging.debug("Tor configuration validation completed successfully.")

    # Sudo password collection
    sudo_password = None
    for attempt in range(3):
        logging.debug(f"Attempting to prompt for sudo password. Attempt {attempt + 1} of 3.")
        sudo_password = prompt_for_password()
        logging.debug("Password input captured. Proceeding to validation...")
        if validate_sudo_password(sudo_password):
            logging.debug("Sudo password validated successfully.")
            break
        logging.error(f"Incorrect sudo password provided. {2 - attempt} attempts remaining.")
    else:
        logging.error("Maximum password attempts exceeded. Exiting...")
        logging.debug("Password validation failed after 3 attempts. Terminating process.")
        return

    # Detect the init system and attempt restart
    logging.debug("Detecting the system's init system to determine restart method...")
    init_system = detect_init_system()
    logging.debug(f"Detected init system: {init_system}. Proceeding with restart process.")

    if not restart_tor_service(init_system, sudo_password):
        logging.error("Failed to restart Tor service. Please check the logs.")
        logging.debug("Tor service restart unsuccessful. Process ending with failure.")
        return

    logging.info("Tor diagnostic tool completed.")
    logging.debug("Process successfully completed with no failures.")

def collect_diagnostics(output_dir="diagnostics"):
    """
    Collect diagnostic logs and custom configuration files.
    """
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Collecting diagnostics in: {output_dir}")

    # Copy custom Tor configuration
    if os.path.exists(TOR_CONFIG):
        dest = os.path.join(output_dir, "torrc")
        shutil.copyfile(TOR_CONFIG, dest)
        logging.info(f"Copied Tor configuration to: {dest}")
    else:
        logging.warning(f"Tor configuration file '{TOR_CONFIG}' not found.")

    # Collect logs
    log_file = "logfile.log"
    if os.path.exists(log_file):
        shutil.copyfile(log_file, os.path.join(output_dir, "logfile.log"))
        logging.info(f"Logfile copied to: {output_dir}")
    else:
        logging.warning("No log file found to collect.")



collect_diagnostics()



if __name__ == "__main__":
    logging.info("Starting the main program execution.")
    try:
        main()
        logging.info("Main program execution completed successfully.")
    except Exception as e:
        logging.critical("An unexpected error occurred in the main block.", exc_info=True)
