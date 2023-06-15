#!/bin/sh

# Open the INI file for editing
sudo nano /etc/a2d/adv_conf.ini

# Wait for the user to save and exit the editor
echo "Please save the INI file and exit the editor to continue..."
read -p "Press Enter to continue after saving the file"

# Run the Python script
sudo python /usr/bin/a2d/app_svc_tmr.py
