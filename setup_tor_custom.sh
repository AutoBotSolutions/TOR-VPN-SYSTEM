#!/bin/bash

# Ask for the admin password at the start of the script
echo "Please enter your admin password:"
read -s ADMIN_PASS
echo ""

# Define the custom torrc path
CUSTOM_TORRC_PATH="/home/tompots/.tor_config/torrc"
CUSTOM_TORRC_DIR="/home/tompots/.tor_config"
INIT_SCRIPT_PATH="/etc/init.d/tor"

# Function to check and set proper permissions
set_permissions() {
   echo "Setting permissions for custom torrc path..."

   # Detect Tor service user (default is debian-tor, fallback is root)
   SERVICE_USER=$(ps aux | grep "[t]or" | awk '{ print $1 }' | head -n 1)
   if [ -z "$SERVICE_USER" ]; then
       SERVICE_USER="debian-tor"  # Default Tor user on many Linux distributions
   fi
   echo "Detected service user: $SERVICE_USER"

   # Ensure the parent directory and configuration directory have proper permissions
   echo "$ADMIN_PASS" | sudo -S chown -R "$SERVICE_USER":"$SERVICE_USER" "$CUSTOM_TORRC_DIR"
   echo "$ADMIN_PASS" | sudo -S chmod 750 /home/tompots  # Allow execute permission for SERVICE_USER
   echo "$ADMIN_PASS" | sudo -S chmod -R 750 "$CUSTOM_TORRC_DIR"
   echo "$ADMIN_PASS" | sudo -S chmod 640 "$CUSTOM_TORRC_PATH"

   # Debug permission outputs for verification
   echo "Debug: Verifying permissions..."
   echo "$ADMIN_PASS" | sudo -S ls -ld /home/tompots
   echo "$ADMIN_PASS" | sudo -S ls -ld /home/tompots/.tor_config
   echo "$ADMIN_PASS" | sudo -S ls -l "$CUSTOM_TORRC_PATH"

   echo "Permissions set successfully for $CUSTOM_TORRC_PATH."
}

# Step 1: Stop any running Tor instances
echo "Stopping existing Tor processes..."
echo "$ADMIN_PASS" | sudo -S killall tor 2>/dev/null
if [ $? -eq 0 ]; then
   echo "All existing Tor processes stopped."
else
   echo "No existing Tor processes were running."
fi

# Step 2: Set proper permissions for the custom configuration
set_permissions

# Step 3: Modify the init.d script to use the custom torrc
echo "Updating the /etc/init.d/tor script to use custom configuration..."
if grep -q "$CUSTOM_TORRC_PATH" "$INIT_SCRIPT_PATH"; then
   echo "/etc/init.d/tor is already configured to use the custom torrc."
else
   # Update the script to point to the custom tor configuration file
   echo "$ADMIN_PASS" | sudo -S sed -i "s|/usr/bin/tor .*|/usr/bin/tor -f $CUSTOM_TORRC_PATH|" "$INIT_SCRIPT_PATH"
   if [ $? -eq 0 ]; then
       echo "Custom torrc configured in /etc/init.d/tor."
   else
       echo "Failed to update the init script. Please check permissions and try again."
       exit 1
   fi
fi

# Step 4: Enable Tor service to start on boot
echo "Enabling Tor to start on boot..."
echo "$ADMIN_PASS" | sudo -S update-rc.d tor defaults
if [ $? -eq 0 ]; then
   echo "Tor service enabled at startup."
else
   echo "Failed to enable Tor at startup. Please check the system's init configuration."
   exit 1
fi

# Step 5: Restart the Tor service to apply the configuration
echo "Restarting Tor service..."
echo "$ADMIN_PASS" | sudo -S /etc/init.d/tor restart
if [ $? -eq 0 ]; then
   echo "Tor service restarted successfully with the custom configuration."
else
   echo "Failed to restart Tor with the custom configuration."
   echo "Please check logs for issues. To debug, run: journalctl -xe | grep -i tor"
   exit 1
fi

# Step 6: Confirm Tor is running with the custom configuration
echo "Verifying Tor process..."
ps aux | grep "[t]or -f $CUSTOM_TORRC_PATH"
if [ $? -eq 0 ]; then
   echo "Tor is running with the custom configuration."
else
   echo "Failed to start Tor with the custom configuration. Please check logs for details."
   exit 1
fi

# Step 7: Check if Tor is listening on expected ports
echo "Checking Tor listening ports..."
echo "$ADMIN_PASS" | sudo -S netstat -tulnp | grep tor
if [ $? -eq 0 ]; then
   echo "Tor is listening on the expected ports."
else
   echo "No Tor listening ports were found. Please review the configuration file."
   exit 1
fi

echo "Setup completed successfully!"