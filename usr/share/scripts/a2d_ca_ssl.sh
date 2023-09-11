#!/bin/bash

# This script generates a ca-signed SSL certificate and key

COMMON_NAME="$1"
EMAIL="$2"

sudo certbot certonly -d "$COMMON_NAME" --standalone --preferred-challenges http --email "$EMAIL" --agree-tos --non-interactive
