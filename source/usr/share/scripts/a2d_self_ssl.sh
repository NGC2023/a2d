#!/bin/bash

# This script generates a self-signed SSL certificate and key

COMMON_NAME="$1"
VALIDITY_DAYS="$2"
ORGANIZATION_NAME="$3"

SSL_CERT_PATH="/etc/nginx/ssl/a2d-ssl.crt"
SSL_KEY_PATH="/etc/nginx/ssl/a2d-ssl.key"

# Check if the certificate and key already exist
if [[ -e "$SSL_CERT_PATH" && -e "$SSL_KEY_PATH" ]]; then
  rm "$SSL_CERT_PATH" "$SSL_KEY_PATH"
fi;

# Generate the self-signed certificate
openssl req -new -newkey rsa:4096 -days "$VALIDITY_DAYS" -nodes -x509 -keyout "$SSL_KEY_PATH" -out "$SSL_CERT_PATH" -subj "/CN=$COMMON_NAME/O=$ORGANIZATION_NAME"

# Verify if the certificate and key were successfully generated
if [[ $? -eq 0 && -e "$SSL_CERT_PATH" && -e "$SSL_KEY_PATH" ]]; then
  echo "Self-signed SSL Certificate generated successfully!"
else
  echo "Error generating self-signed certificate."
fi
