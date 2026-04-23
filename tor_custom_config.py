import os
import logging
import stat
import subprocess
import getpass
import platform

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_UNIX = not IS_WINDOWS

# Unix-only imports
if IS_UNIX:
    import pwd
    import grp

# Directory and file paths
torrc_directory = os.path.join(os.path.expanduser("~"), ".tor_config")
torrc_path = os.path.join(torrc_directory, "torrc")

# Tor configuration details
control_port = 9051
torrc_template = """
ControlPort {control_port}
HashedControlPassword {hashed_password}
"""

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("create_torrc.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)


def generate_hashed_password(password):
    """
    Generate the hashed control password for Tor.
    """
    try:
        result = subprocess.run(
            ["tor", "--hash-password", password],
            text=True,
            capture_output=True,
            check=True,
        )
        hashed_password = result.stdout.strip()
        logging.info(f"Generated hashed password successfully.")
        return hashed_password
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating hashed password: {e}")
        raise e


def change_ownership(file_path, user_name, group_name):
    """
    Changes the ownership of a file to the specified user and group.
    Only works on Unix systems.
    """
    if IS_WINDOWS:
        logging.warning("Ownership change not supported on Windows.")
        return
    
    try:
        # Get the user and group IDs
        uid = pwd.getpwnam(user_name).pw_uid
        gid = grp.getgrnam(group_name).gr_gid

        # Change the ownership of the file
        os.chown(file_path, uid, gid)
        logging.info(f"Ownership of file {file_path} changed to {user_name}:{group_name}")
    except KeyError:
        logging.error(f"User '{user_name}' or group '{group_name}' does not exist.")
        raise
    except PermissionError:
        logging.error(f"Permission denied while changing ownership of file {file_path}.")
        raise
    except Exception as e:
        logging.error(f"Failed to change ownership for file {file_path}: {e}")
        raise


def create_directory(directory):
    """
    Create the specified directory if it doesn't exist, and set proper permissions.
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            # Set permissions to 700 for the directory
            os.chmod(directory, 0o700)
            logging.info(f"Directory created: {directory} with permissions 700")
        else:
            logging.info(f"Directory already exists: {directory}")
    except Exception as e:
        logging.error(f"Failed to create directory '{directory}': {e}")
        raise e


def create_torrc_file():
    """
    Create the torrc file, set permissions, and set ownership.
    """
    try:
        # Prompt the user for a plain-text control password
        plain_password = getpass.getpass("Enter a password for Tor control port access: ")
        hashed_password = generate_hashed_password(plain_password)

        # Customize the torrc content dynamically
        torrc_content = torrc_template.format(
            control_port=control_port,
            hashed_password=hashed_password,
        )

        # Write the torrc configuration to the file
        with open(torrc_path, "w") as file:
            file.write(torrc_content.strip())

        logging.info(f"Tor configuration file written successfully at: {torrc_path}")

        # Set file permissions to 600 (read and write for owner only)
        os.chmod(torrc_path, 0o600)
        logging.info(f"Permissions for {torrc_path} set to 600")

        # Change file ownership directly without sudo (Unix only)
        if IS_UNIX:
            import getpass
            current_user = getpass.getuser()
            change_ownership(torrc_path, current_user, current_user)

    except PermissionError as e:
        logging.error(f"Permission denied while creating or setting permissions for '{torrc_path}': {e}")
        raise e
    except Exception as e:
        logging.error(f"Failed to create or configure the torrc file: {e}")
        raise e


def verify_file_access(file_path):
    """
    Verify the file permissions and accessibility.
    """
    try:
        # Get file info and permissions
        file_stat = os.stat(file_path)
        file_permissions = stat.filemode(file_stat.st_mode)

        # Check if the file permissions are restricted
        if file_permissions != "-rw-------":
            logging.warning(f"File permissions for {file_path} are not secure: {file_permissions}")
        else:
            logging.info(f"File permissions for {file_path} are properly set: {file_permissions}")

        # Verify readable and writable access
        if os.access(file_path, os.R_OK) and os.access(file_path, os.W_OK):
            logging.info(f"File {file_path} is accessible (read and write).")
        else:
            logging.warning(f"File {file_path} is NOT accessible (read/write privileges missing).")

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error verifying file access for {file_path}: {e}")


if __name__ == "__main__":
    # Ensure the directory for the torrc file exists with proper permissions
    create_directory(torrc_directory)

    # Create the torrc file, set permissions, and set ownership
    create_torrc_file()

    # Verify the file permissions and accessibility
    verify_file_access(torrc_path)