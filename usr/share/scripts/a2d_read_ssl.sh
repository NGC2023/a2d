#!/bin/bash

read_ca_ssl() {
    cert_file="$1"

    if [ -e "$cert_file" ]; then
        common_name=$(openssl x509 -noout -subject -in "$cert_file" | grep -o 'CN =[^,]*' | cut -d= -f2)
        organization_name=$(openssl x509 -noout -subject -in "$cert_file" | grep -o 'O =[^,]*' | cut -d= -f2)
        expiry_date=$(openssl x509 -noout -enddate -in "$cert_file" | cut -d= -f2)
        expiry_date=$(date -d "$expiry_date" '+%Y-%m-%d %H:%M:%S')

        echo "$common_name,$organization_name,$expiry_date"
    else
        echo "None,None,None"
    fi
}

# Check the number of arguments
if [ $# -ne 1 ]; then
    echo "Usage: $0 <cert_file>"
    exit 1
fi

cert_file="$1"
read_ca_ssl "$cert_file"
