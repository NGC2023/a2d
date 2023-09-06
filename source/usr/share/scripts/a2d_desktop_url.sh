#!/bin/bash

# Define the path to the nginx configuration file
NGINX_CONF="/etc/nginx/sites-available/a2dapp"

# Extract the value of the 'listen' directive from the nginx configuration
LISTEN_VALUE=$(grep -oP 'listen\s+\K[^;]+' "$NGINX_CONF")

# Determine the URL based on the 'listen' value
if [[ "$LISTEN_VALUE" == "443 ssl" ]]; then
    URL="https://localhost"
elif [[ "$LISTEN_VALUE" == "80" ]]; then
    URL="http://localhost"
else
    URL="http://localhost:$LISTEN_VALUE"
fi

# Open the determined URL
xdg-open "$URL"
