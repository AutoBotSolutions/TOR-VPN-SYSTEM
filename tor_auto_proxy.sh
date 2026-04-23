#!/bin/bash

# Configuration
TOR_LOG_FILE="$HOME/tor_management_gui.log"  # Default to user home for compatibility
TOR_PORT=9050
CONTROL_PORT=9051

# Initialize script for macOS compatibility
is_macos=false
if [[ "$OSTYPE" == "darwin"* ]]; then
   is_macos=true
fi

# Check for Zenity availability
if ! command -v zenity &>/dev/null; then
   if $is_macos; then
       echo "Zenity is not installed. Install Zenity using Homebrew with 'brew install zenity' or install it manually. Exiting."
   else
       echo "Zenity is not installed. Install Zenity using package manager (e.g., 'sudo apt install zenity'). Exiting."
   fi
   exit 1
fi

# Adjust UI size dynamically
UI_WIDTH=500
UI_HEIGHT=500

# Functions to enable and disable Tor proxy system-wide
enable_tor_proxy() {
   export http_proxy="socks5h://127.0.0.1:$TOR_PORT"
   export https_proxy="socks5h://127.0.0.1:$TOR_PORT"
   export all_proxy="socks5h://127.0.0.1:$TOR_PORT"
   log_message "INFO" "Proxy set to route traffic through Tor (127.0.0.1:$TOR_PORT)"
}

disable_tor_proxy() {
   unset http_proxy https_proxy all_proxy
   log_message "INFO" "Proxy settings restored to default"
}

# Log messages
log_message() {
   local message_type="$1"
   local message="$2"
   echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$message_type] $message" >> "$TOR_LOG_FILE"
}

# Stream command output
stream_command_output() {
   local title="$1"
   local command="$2"
   local temp_file=$(mktemp)

   log_message "INFO" "Executing: $command"
   {
       echo "Running command: $command" > "$temp_file"
       eval "$command" >> "$temp_file" 2>&1
       echo "COMMAND FINISHED" >> "$temp_file"
   } &
   tail -f "$temp_file" | zenity --text-info --title="$title" --width=$UI_WIDTH --height=$UI_HEIGHT --ok-label="Close"
   rm -f "$temp_file"
}

# Function to open browsers with Tor proxy enabled
open_browser_with_tor() {
   local browser="$1"

   case "$browser" in
   chrome)
       log_message "INFO" "Opening Google Chrome with Tor proxy"
       stream_command_output "Opening Google Chrome" "google-chrome --proxy-server=\"socks5://127.0.0.1:$TOR_PORT\""
       ;;
   firefox)
       log_message "INFO" "Opening Firefox with Tor proxy"
       stream_command_output "Opening Firefox" "firefox --new-instance -private-window -no-remote -profile \"$(setup_firefox_temp_profile)\""
       ;;
   *)
       zenity --error --text="Invalid browser selected. Please try again."
       log_message "ERROR" "Invalid browser selected: $browser"
       ;;
   esac
}

# Function to configure a temporary Firefox profile for Tor
setup_firefox_temp_profile() {
   local temp_profile_dir
   temp_profile_dir=$(mktemp -d -t firefox-tor-profile-XXXX)

   echo 'user_pref("network.proxy.type", 1);' > "$temp_profile_dir/user.js"
   echo 'user_pref("network.proxy.socks", "127.0.0.1");' >> "$temp_profile_dir/user.js"
   echo "user_pref(\"network.proxy.socks_port\", $TOR_PORT);" >> "$temp_profile_dir/user.js"
   echo 'user_pref("network.proxy.socks_remote_dns", true);' >> "$temp_profile_dir/user.js"

   echo "$temp_profile_dir"
}

# Main Menu
while true; do
   CHOICE=$(zenity --list --title="Tor Management" --width=$UI_WIDTH --height=$UI_HEIGHT \
       --column="Command" --column="Description" \
       "enable_proxy" "Enable proxy system-wide for Tor" \
       "disable_proxy" "Disable proxy system-wide" \
       "open_chrome" "Open Google Chrome with traffic routed through Tor" \
       "open_firefox" "Open Firefox with traffic routed through Tor" \
       "exit" "Exit the Script")

   [ -z "$CHOICE" ] && log_message "INFO" "User exited." && break

   case "$CHOICE" in
   enable_proxy) enable_tor_proxy ;;
   disable_proxy) disable_tor_proxy ;;
   open_chrome) open_browser_with_tor "chrome" ;;
   open_firefox) open_browser_with_tor "firefox" ;;
   exit) break ;;
   *) zenity --error --text="Invalid option. Please try again." ;;
   esac
done

exit 0