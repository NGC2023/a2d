#!/bin/bash

# This script removes a ca-signed SSL certificate and key

COMMON_NAME="$1"

sudo certbot delete --cert-name "$COMMON_NAME" --non-interactive
