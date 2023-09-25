import os
import subprocess
import datetime
import re
from a2dapp.routes.nginx import reload_nginx, read_nginx_config, disable_default_ng, enable_default_ng

def read_ssl(cert_file):
    if not cert_file or not os.path.exists(cert_file):
        return "None,None,None"

    try:
        # Use subprocess to run openssl commands
        subject = subprocess.check_output(['openssl', 'x509', '-noout', '-subject', '-in', cert_file]).decode()
        expiry_date = subprocess.check_output(['openssl', 'x509', '-noout', '-enddate', '-in', cert_file]).decode()

        common_name = None
        organization_name = None

        # Use regular expressions to extract CN and O fields
        cn_match = re.search(r'CN\s*=\s*([^/,]+)', subject)
        o_match = re.search(r'O\s*=\s*([^/,]+)', subject)

        if cn_match:
            common_name = cn_match.group(1).strip()
        if o_match:
            organization_name = o_match.group(1).strip()

        expiry_date = expiry_date.split('=')[1].strip()
        expiry_date = datetime.datetime.strptime(expiry_date, '%b %d %H:%M:%S %Y %Z')
        expiry_date = expiry_date.strftime('%Y-%m-%d %H:%M:%S')

        return f"{common_name},{organization_name},{expiry_date}"

    except Exception as e:
        return "None,None,None"

def a2d_self_ssl(common_name, validity_days, organization_name):
    ssl_cert_path = '/etc/nginx/ssl/a2d-ssl.crt'
    ssl_key_path = '/etc/nginx/ssl/a2d-ssl.key'
    try:
        # Check if the certificate and key already exist
        if os.path.exists(ssl_cert_path) and os.path.exists(ssl_key_path):
            os.remove(ssl_cert_path)
            os.remove(ssl_key_path)

        # Redirect stdout and stderr to /dev/null to avoid unknown output from openssl
        with open(os.devnull, 'w') as devnull:
            # Generate the self-signed certificate
            subprocess.run([
                "openssl", "req", "-new", "-newkey", "rsa:4096", "-days", str(validity_days),
                "-nodes", "-x509", "-keyout", ssl_key_path, "-out", ssl_cert_path,
                "-subj", f"/CN={common_name}/O={organization_name}"
            ], check=True, stdout=devnull, stderr=devnull)

        # Verify if the certificate and key were successfully generated
        if os.path.exists(ssl_cert_path) and os.path.exists(ssl_key_path):
            return "sSSL generated"
        else:
            return "Error generating SSL"

    except subprocess.CalledProcessError as e:
        return "Error generating SSL"
    except Exception as e:
        return "Error generating SSL"

def a2d_rm_cassl(common_name):
    try:
        # Execute the certbot command to delete the certificate
        subprocess.run(["certbot", "delete", "--cert-name", common_name, "--non-interactive"], check=True)
        return "caSSL removed"
    except subprocess.CalledProcessError as e:
        return "Error removing SSL"

def a2d_ca_ssl(common_name, email):
    disable_default_ng()
    reload_nginx()
    listen_port = read_nginx_config('listen')
    try:
        # Execute the certbot command to generate the certificate
        subprocess.run(["certbot", "certonly", "-d", common_name, "--standalone", "--preferred-challenges", "http", "--email", email, "--agree-tos", "--non-interactive"], check=True)
        if listen_port != '80':
            enable_default_ng()
        reload_nginx()
        return "caSSL generated"
    except subprocess.CalledProcessError as e:
        if listen_port != '80':
            enable_default_ng()
        reload_nginx()
        return "Error generating SSL"

def a2d_ca_list():
    try:
        # Execute the 'ls' and 'grep' commands
        result = subprocess.run(["ls", "/etc/letsencrypt/live/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Filter out the "README" entry
        certificates = [cert.strip() for cert in output.split('\n') if cert.strip() != "README"]
        
        return certificates

    except subprocess.CalledProcessError as e:
        return []

def a2d_rm_selfssl():
    ssl_cert_path = '/etc/nginx/ssl/a2d-ssl.crt'
    ssl_key_path = '/etc/nginx/ssl/a2d-ssl.key'
    # Check if the certificate and key already exist
    if os.path.exists(ssl_cert_path) and os.path.exists(ssl_key_path):
        os.remove(ssl_cert_path)
        os.remove(ssl_key_path)
