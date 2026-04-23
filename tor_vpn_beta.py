# --- Standard Library Imports ---
import os
import sys
import signal
import subprocess
import socket
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox, ttk
import logging
from logging.handlers import RotatingFileHandler

# --- Third-Party Imports ---
from stem.control import Controller
from stem import Signal

# --- Global Constants ---
TOR_PASSWORD_ENV = "TOR_PASSWORD"
TOR_DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".tor_config")
TOR_CONFIG_FILE = os.path.join(TOR_DEFAULT_DIR, "torrc")
DEFAULT_PASSWORD = "467rSeG7%tGd757575EwPLsaQ$BplwEQJ7676RLsa$3@4161"
PRECOMPUTED_HASHED_PASSWORD = "16:B76A6ED6F4E32AB16028702348A5E765C6A53BCE1F82E467C614392ECD"

LOG_FILE = "vpn_app_advanced.log"
SERVERS = {

    "Afghanistan": "af",
    "Albania": "al",
    "Algeria": "dz",
    "Andorra": "ad",
    "Angola": "ao",
    "Argentina": "ar",
    "Armenia": "am",
    "Australia": "au",
    "Austria": "at",
    "Azerbaijan": "az",
    "Bahamas": "bs",
    "Bangladesh": "bd",
    "Barbados": "bb",
    "Belarus": "by",
    "Belgium": "be",
    "Belize": "bz",
    "Benin": "bj",
    "Bhutan": "bt",
    "Bolivia": "bo",
    "Bosnia and Herzegovina": "ba",
    "Botswana": "bw",
    "Brazil": "br",
    "Brunei": "bn",
    "Bulgaria": "bg",
    "Burkina Faso": "bf",
    "Burundi": "bi",
    "Cambodia": "kh",
    "Cameroon": "cm",
    "Canada": "ca",
    "Cape Verde": "cv",
    "Central African Republic": "cf",
    "Chad": "td",
    "Chile": "cl",
    "China": "cn",
    "Colombia": "co",
    "Comoros": "km",
    "Congo": "cg",
    "Costa Rica": "cr",
    "Croatia": "hr",
    "Cuba": "cu",
    "Cyprus": "cy",
    "Czech Republic": "cz",
    "Denmark": "dk",
    "Djibouti": "dj",
    "Dominica": "dm",
    "Dominican Republic": "do",
    "Ecuador": "ec",
    "Egypt": "eg",
    "El Salvador": "sv",
    "Equatorial Guinea": "gq",
    "Eritrea": "er",
    "Estonia": "ee",
    "Eswatini": "sz",
    "Ethiopia": "et",
    "Fiji": "fj",
    "Finland": "fi",
    "France": "fr",
    "Gabon": "ga",
    "Gambia": "gm",
    "Georgia": "ge",
    "Germany": "de",
    "Ghana": "gh",
    "Greece": "gr",
    "Grenada": "gd",
    "Guatemala": "gt",
    "Guinea": "gn",
    "Guinea-Bissau": "gw",
    "Guyana": "gy",
    "Haiti": "ht",
    "Honduras": "hn",
    "Hungary": "hu",
    "Iceland": "is",
    "India": "in",
    "Indonesia": "id",
    "Iran": "ir",
    "Iraq": "iq",
    "Ireland": "ie",
    "Israel": "il",
    "Italy": "it",
    "Jamaica": "jm",
    "Japan": "jp",
    "Jordan": "jo",
    "Kazakhstan": "kz",
    "Kenya": "ke",
    "Kiribati": "ki",
    "Korea, South": "kr",
    "Kuwait": "kw",
    "Kyrgyzstan": "kg",
    "Laos": "la",
    "Latvia": "lv",
    "Lebanon": "lb",
    "Lesotho": "ls",
    "Liberia": "lr",
    "Libya": "ly",
    "Liechtenstein": "li",
    "Lithuania": "lt",
    "Luxembourg": "lu",
    "Madagascar": "mg",
    "Malawi": "mw",
    "Malaysia": "my",
    "Maldives": "mv",
    "Mali": "ml",
    "Malta": "mt",
    "Marshall Islands": "mh",
    "Mauritania": "mr",
    "Mauritius": "mu",
    "Mexico": "mx",
    "Micronesia": "fm",
    "Moldova": "md",
    "Monaco": "mc",
    "Mongolia": "mn",
    "Montenegro": "me",
    "Morocco": "ma",
    "Mozambique": "mz",
    "Myanmar": "mm",
    "Namibia": "na",
    "Nauru": "nr",
    "Nepal": "np",
    "Netherlands": "nl",
    "New Zealand": "nz",
    "Nicaragua": "ni",
    "Niger": "ne",
    "Nigeria": "ng",
    "North Macedonia": "mk",
    "Norway": "no",
    "Oman": "om",
    "Pakistan": "pk",
    "Palau": "pw",
    "Palestine": "ps",
    "Panama": "pa",
    "Papua New Guinea": "pg",
    "Paraguay": "py",
    "Peru": "pe",
    "Philippines": "ph",
    "Poland": "pl",
    "Portugal": "pt",
    "Qatar": "qa",
    "Romania": "ro",
    "Russia": "ru",
    "Rwanda": "rw",
    "Saint Kitts and Nevis": "kn",
    "Saint Lucia": "lc",
    "Saint Vincent and the Grenadines": "vc",
    "Samoa": "ws",
    "San Marino": "sm",
    "Sao Tome and Principe": "st",
    "Saudi Arabia": "sa",
    "Senegal": "sn",
    "Serbia": "rs",
    "Seychelles": "sc",
    "Sierra Leone": "sl",
    "Singapore": "sg",
    "Slovakia": "sk",
    "Slovenia": "si",
    "Solomon Islands": "sb",
    "Somalia": "so",
    "South Africa": "za",
    "South Sudan": "ss",
    "Spain": "es",
    "Sri Lanka": "lk",
    "Sudan": "sd",
    "Suriname": "sr",
    "Sweden": "se",
    "Switzerland": "ch",
    "Syria": "sy",
    "Taiwan": "tw",
    "Tajikistan": "tj",
    "Tanzania": "tz",
    "Thailand": "th",
    "Timor-Leste": "tl",
    "Togo": "tg",
    "Tonga": "to",
    "Trinidad and Tobago": "tt",
    "Tunisia": "tn",
    "Turkey": "tr",
    "Turkmenistan": "tm",
    "Tuvalu": "tv",
    "Uganda": "ug",
    "Ukraine": "ua",
    "United Arab Emirates": "ae",
    "United Kingdom": "gb",
    "United States": "us",
    "Uruguay": "uy",
    "Uzbekistan": "uz",
    "Vanuatu": "vu",
    "Vatican City": "va",
    "Venezuela": "ve",
    "Vietnam": "vn",
    "Yemen": "ye",
    "Zambia": "zm",
    "Zimbabwe": "zw",
}
TOR_CONFIG = {
    "port": 9050,
    "control_port": 9051,
    "control_password": None,  # To be dynamically set
    "torrc": TOR_CONFIG_FILE,
}

logging.getLogger("stem").setLevel(logging.WARNING)


# --- Logging and Signal Handling ---
def setup_logging(log_file=LOG_FILE):
    """Setup logging with rotating file handlers."""
    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def setup_signal_handlers():
    """Setup signal handlers for clean termination."""

    def signal_handler(sig, frame):
        logging.critical(f"Received termination signal: {sig}. Exiting...")
        sys.exit(1)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


# --- Admin Privilege Verification ---
def ensure_admin_privileges():
    """Ensure the script is running with administrator privileges."""
    if os.name != "nt" and os.geteuid() != 0:
        logging.error("This script must be run with sudo/root privileges.")
        sys.exit(1)
    elif os.name == "nt":
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showerror("Error", "Please run this script as an Administrator.")
            sys.exit(1)




def update_tor_config_file(hashed_password):
    """
    Update the Tor configuration file (torrc) with hashed password and control port.
    """
    try:
        os.makedirs(TOR_DEFAULT_DIR, exist_ok=True)
        with open(TOR_CONFIG["torrc"], "w") as file:
            file.write(f"ControlPort {TOR_CONFIG['control_port']}\n")
            file.write(f"HashedControlPassword {hashed_password}\n")
        os.chmod(TOR_CONFIG["torrc"], 0o600)
        logging.debug(f"Updated torrc with precomputed hashed password: {hashed_password}")
    except Exception as e:
        logging.error(f"Failed to update torrc file: {e}")
        raise




def restart_tor_service():
    """Restart the Tor service to ensure updated configuration is loaded."""
    try:
        subprocess.run(["sudo", "service", "tor", "restart"], text=True, check=True)
        logging.info("Tor service restarted successfully, new configuration applied.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Tor service restart failed: {e}")
        raise




def validate_tor_control_port():
    """Check if the Tor control port is accessible."""
    try:
        with socket.create_connection(("127.0.0.1", TOR_CONFIG["control_port"]), timeout=5):
            return True
    except socket.error:
        return False


def initialize_tor_config():
    """
    Initialize Tor configuration:
    - Use precomputed hashed password.
    - Update the configuration file.
    - Verify the Tor service.
    """
    try:
        logging.info("Initializing Tor configuration...")

        # Use the precomputed hashed password
        hashed_password = PRECOMPUTED_HASHED_PASSWORD
        TOR_CONFIG["control_password"] = DEFAULT_PASSWORD  # Plain password passed during authentication
        logging.debug(f"Using precomputed hashed password: {hashed_password}")

        # Write hashed password to torrc
        update_tor_config_file(hashed_password)

        # Validate Tor and restart the service if necessary
        if not validate_tor_control_port():
            logging.warning("Tor control port not accessible. Restarting Tor service...")
            restart_tor_service()

        logging.info("Tor configuration initialized successfully.")
    except Exception as e:
        logging.critical(f"Failed to initialize Tor configuration: {e}")
        sys.exit(1)




def connect_to_tor(country_code):
    """
    Connect to Tor using the specified country code for the exit node.
    """
    try:
        logging.debug("Opening Tor controller connection...")

        with Controller.from_port(port=TOR_CONFIG["control_port"]) as controller:
            logging.debug("Authenticating with Tor controller...")
            controller.authenticate(password=TOR_CONFIG["control_password"])  # Authenticate with plain password

            # Validate and configure the exit node
            if country_code.lower() not in SERVERS.values():
                raise ValueError(f"Invalid country code: {country_code}")

            # Signal for a new identity to apply the new exit node
            logging.debug("Setting exit node for country: %s", country_code.upper())
            controller.signal(Signal.NEWNYM)
            controller.set_conf("ExitNodes", f"{{{country_code}}}")
            controller.set_conf("__LeaveStreamsUnattached", "1")  # Ensure streams are handled normally

            logging.info(f"Connected to Tor with exit node: {country_code.upper()}.")

    except Exception as e:
        logging.error(f"Failed to connect to Tor: {e}")
        raise




def disconnect_tor():
    """
    Disconnect from Tor by resetting exit node configurations.
    """
    try:
        logging.debug("Opening Tor controller connection...")

        with Controller.from_port(port=TOR_CONFIG["control_port"]) as controller:
            logging.debug("Authenticating with Tor controller to disconnect...")
            controller.authenticate(password=TOR_CONFIG["control_password"])  # Plain password for authentication

            # Reset exit node configuration
            controller.reset_conf("ExitNodes")
            logging.info("Cleared Tor exit node configuration. Disconnected from custom routing.")

    except Exception as e:
        logging.error(f"Failed to disconnect from Tor: {e}")
        raise



# --- GUI Components ---
class VPNInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Tor VPN Client")
        self.master.geometry("600x400")
        self.master.configure(bg="#2b2b2b")

        self.create_widgets()

    def create_widgets(self):
        """Build the GUI components."""
        self.main_frame = tk.Frame(self.master, bg="#34495e", bd=2, relief="raised")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        tk.Label(self.main_frame, text="Tor VPN Client", font=("Helvetica", 18, "bold"),
                 bg="#2980b9", fg="white", pady=10).pack(fill="x")

        # Tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)

        self.status_tab = tk.Frame(self.notebook, bg="#2b3e50")
        self.servers_tab = tk.Frame(self.notebook, bg="#2b3e50")

        self.notebook.add(self.status_tab, text="Status")
        self.notebook.add(self.servers_tab, text="Servers")

        self.create_status_tab()
        self.create_servers_tab()

    def create_status_tab(self):
        """Build the Status tab."""
        tk.Label(self.status_tab, text="Connection Status",
                 font=("Helvetica", 14, "bold"), bg="#2b3e50", fg="white").pack(pady=10)

        self.connection_status_label = tk.Label(
            self.status_tab,
            text="Not Connected",
            font=("Helvetica", 12, "bold"),
            bg="#c0392b",
            fg="white",
            width=20
        )
        self.connection_status_label.pack(pady=10)

        self.connect_btn = tk.Button(
            self.status_tab, text="Connect", font=("Helvetica", 12),
            bg="#27ae60", fg="white", command=self.connect
        )
        self.connect_btn.pack(pady=5)

        self.disconnect_btn = tk.Button(
            self.status_tab, text="Disconnect", font=("Helvetica", 12),
            bg="#c0392b", fg="white", state=tk.DISABLED, command=self.disconnect
        )
        self.disconnect_btn.pack(pady=5)

    def create_servers_tab(self):
        """Build the Servers tab."""
        tk.Label(self.servers_tab, text="Available Servers",
                 font=("Helvetica", 14, "bold"), bg="#2b3e50", fg="white").pack(pady=10)

        self.server_tree = ttk.Treeview(self.servers_tab, columns=("ID", "Country", "Code"), show="headings")
        self.server_tree.heading("ID", text="ID")
        self.server_tree.heading("Country", text="Country")
        self.server_tree.heading("Code", text="Code")
        self.server_tree.pack(fill="both", expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(self.servers_tab, orient=tk.VERTICAL, command=self.server_tree.yview)
        self.server_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for idx, (country, code) in enumerate(SERVERS.items(), start=1):
            self.server_tree.insert("", "end", values=(idx, country, code))

    def connect(self):
        """Connect to Tor."""
        country = askstring("Country Code", "Enter a valid country code (e.g., US):")
        if not country:
            messagebox.showwarning("Error", "No country code provided.")
            return
        try:
            connect_to_tor(country)
            self.connection_status_label.config(text="Connected", bg="#27ae60")
            self.connect_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Success", f"Connected to {country.upper()}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def disconnect(self):
        """Disconnect from Tor."""
        try:
            disconnect_tor()
            self.connection_status_label.config(text="Not Connected", bg="#c0392b")
            self.connect_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Disconnected successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# --- Main Entry Point ---
def main():
    """Main entry point of the application."""
    try:
        setup_logging()
        setup_signal_handlers()
        ensure_admin_privileges()
        initialize_tor_config()

        root = tk.Tk()
        app = VPNInterface(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()