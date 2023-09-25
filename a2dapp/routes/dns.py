import os
import subprocess
import re
from datetime import datetime
from flask import Blueprint, request, render_template, jsonify
from a2dapp.modals.creds import get_credentials
from a2dapp.routes.auth import login_required
from a2dapp.routes.certs import read_ssl, a2d_self_ssl, a2d_rm_cassl, a2d_ca_ssl, a2d_ca_list
from a2dapp.routes.nginx import reload_nginx, read_nginx_config, disable_default_ng, enable_default_ng

dns_routes = Blueprint('dns', __name__)

# Define the directory paths
NGINX_CONFIG_PATH = '/etc/nginx/conf.d/00-a2dapp.conf'
SSL_CERT_PATH = '/etc/nginx/ssl/a2d-ssl.crt'
SSL_KEY_PATH = '/etc/nginx/ssl/a2d-ssl.key'

#DNS data to HTML
@dns_routes.route('/local-dns-setting', methods=['GET'])
@login_required
def local_dns_setting():
    creds = get_credentials()  # Need this to display Navbar_full in dns.html
    
    #SSL status and server name
    current_listen_port = read_nginx_config('listen')
    if current_listen_port == 'ssl': #Strip from nginx conifg file
        current_listen_port = '443'
    current_server_name = read_nginx_config('server_name')
    current_ssl_status = current_listen_port == '443'
    a2d_default_dns = (current_listen_port == '9331' and current_server_name == '_' and not current_ssl_status)

    #Self SSL details
    output = read_ssl(SSL_CERT_PATH)
    stored_selfcommon_name, stored_selforganization_name, _ = output.split(',')
    if stored_selfcommon_name == '':
        stored_selfcommon_name = 'None'
    if stored_selforganization_name == '':
        stored_selforganization_name = 'None'

    #Get cassl list
    cassl_certs_list = list_cassl_certs()

    return render_template(
        'dns.html', 
        listen_port=current_listen_port, 
        server_name=current_server_name, 
        current_ssl_status=current_ssl_status, 
        a2d_default_dns=a2d_default_dns, 
        stored_selfcommon_name=stored_selfcommon_name, 
        stored_selforganization_name=stored_selforganization_name, 
        cassl_certs=cassl_certs_list, 
        creds=creds
    )

#Set server config
@dns_routes.route('/server-config', methods=['POST'])
@login_required
def server_config():
    set_selfssl_status = 'disable'
    set_cassl_status = 'disable'
    cassl_certs_list = list_cassl_certs()

    listen_port = request.form['listen_port']
    server_name = request.form['server_name']
    enable_self_ssl = request.form.get('enable_ssl') == 'true'
    set_cassl_certs = request.form['set_cassl_certs']
    enable_ca_ssl = request.form.get('enable_cassl') == 'true'
    set_default_dns = request.form.get('set_default_dns') == 'true'

    if enable_self_ssl and not enable_ca_ssl:
        # Check if the self-signed certificate and key files exist
        if (os.path.exists(SSL_CERT_PATH) and os.path.exists(SSL_KEY_PATH)):
            set_selfssl_status = 'enable'
        else:
            return "Create SSL"

    elif enable_ca_ssl and not enable_self_ssl:
        if set_cassl_certs in cassl_certs_list:
            if set_cassl_certs == server_name:    
                set_cassl_status = 'enable'
            elif set_cassl_certs == '':
                return "Create caSSL"
            else:
                set_cassl_status = 'enable'
                server_name = set_cassl_certs
        else:
            return "Create caSSL"

    elif listen_port == '443' and not enable_self_ssl and not set_default_dns:
        if not (os.path.exists(SSL_CERT_PATH) and os.path.exists(SSL_KEY_PATH)):
            return "Create SSL"
        else:
            set_selfssl_status = 'enable'
    
    elif listen_port == '443' and set_default_dns:
        listen_port = '9331'
        set_selfssl_status = 'disable'
        server_name = '_'

    elif set_default_dns:
        listen_port = '9331'
        set_selfssl_status = 'disable'
        server_name = '_'

    else:
        pass

    # Update the Nginx configuration
    update_nginx_config(listen_port, server_name, set_selfssl_status, set_cassl_status)
    
    if listen_port == '80':
        disable_default_ng()
    elif listen_port != '80':
        enable_default_ng()

    reload_nginx()

    if set_selfssl_status == 'enable':
        return "SSL enabled"
    elif set_cassl_status == 'enable':
        return "caSSL enabled"
    elif listen_port == '9331' and set_selfssl_status == 'disable' and server_name == '_':
        return "Set default"
    else:
        return "Server updated"

#Update nginx config
def update_nginx_config(listen_port, server_name, set_selfssl_status, set_cassl_status):
    try:
        with open(NGINX_CONFIG_PATH, 'r') as config_file:
            lines = config_file.readlines()

        if server_name != '_' or '':
            CASSL_CERT_PATH = f'/etc/letsencrypt/live/{server_name}/fullchain.pem'
            CASSL_KEY_PATH = f'/etc/letsencrypt/live/{server_name}/privkey.pem'
        else:
            CASSL_CERT_PATH, CASSL_KEY_PATH = 'None', 'None'

        updated_lines = []
        
        ssl_line = "listen 443 ssl;"
        self_ssl_line1 = f"ssl_certificate {SSL_CERT_PATH};"
        self_ssl_line2 = f"ssl_certificate_key {SSL_KEY_PATH};"
        ca_ssl_line1 = f"ssl_certificate {CASSL_CERT_PATH};"
        ca_ssl_line2 = f"ssl_certificate_key {CASSL_KEY_PATH};"

        updated_listen = False  # Flag to keep track of whether the "listen" line has been updated

        for line in lines:
            if line.strip().startswith("listen "):
                if not updated_listen:  # Only add one "listen" line
                    if set_selfssl_status == 'enable':
                        updated_lines.append(f"    {ssl_line}\n    {self_ssl_line1}\n    {self_ssl_line2}\n")
                    elif set_cassl_status == 'enable':
                        updated_lines.append(f"    {ssl_line}\n    {ca_ssl_line1}\n    {ca_ssl_line2}\n")
                    else:
                        updated_lines.append(f"    listen {listen_port};\n")
                    updated_listen = True
            elif line.strip().startswith("ssl_certificate"):
                if set_selfssl_status != 'enable' or set_cassl_status != 'enable':
                    # Skip these lines if self-signed SSL is not enabled
                    continue
            elif line.strip().startswith("server_name "):
                updated_lines.append(f"    server_name {server_name};\n")
            else:
                updated_lines.append(line)

        with open(NGINX_CONFIG_PATH, 'w') as config_file:
            config_file.writelines(updated_lines)

    except Exception as e:
        return f"Error updating nginx conf: {e}"

#Generate self-signed SSL
@dns_routes.route('/gen-self-signed-ssl', methods=['POST'])
@login_required
def gen_self_signed_ssl():
    common_name = request.form["common_name"]
    validity_days = int(request.form["validity_days"])
    organization_name = request.form["organization_name"]
    self_ssl_result = a2d_self_ssl(common_name, validity_days, organization_name)
    if self_ssl_result == "sSSL generated":
        reload_nginx()
        return "sSSL generated"
    else:
        return "Error generating SSL"

#Generate CN signed SSL
@dns_routes.route('/gen-ca-ssl', methods=['POST'])
@login_required
def gen_ca_ssl():
    ca_common_name = request.form["ca_common_name"]
    email_id = request.form["email_id"]
    cassl_certs_list = list_cassl_certs()

    if ca_common_name not in cassl_certs_list:
        if is_valid_email(email_id):
            ca_ssl = a2d_ca_ssl(ca_common_name, email_id)
            if ca_ssl == "caSSL generated":
                return "caSSL generated"
            else:
                return "Error generating SSL"
        else:
            return "invalid email"
    else:
        return "caSSL exist"

#Email syntax check
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

#Remove CN signed SSL
@dns_routes.route('/rm-ca-ssl', methods=['POST'])
@login_required
def rm_ca_ssl():
    rm_cassl_certs = request.form['rm_cassl_certs']
    cassl_certs_list = list_cassl_certs()
    current_server_name = read_nginx_config('server_name')

    if rm_cassl_certs in cassl_certs_list:
        if rm_cassl_certs != current_server_name:
            rm_cassl = a2d_rm_cassl(rm_cassl_certs)
            if rm_cassl == "caSSL removed":
                reload_nginx()
                return "caSSL removed"
            else:
                return "Error removing SSL"
        else:
            return "caSSL in use"
    else:
        return "No caSSL"

#Get the list of CA SSL
def list_cassl_certs():
    result = a2d_ca_list()
    return result

#HTML data display
@dns_routes.route('/for-html', methods=['GET'])
@login_required
def for_html():
    # Read the current DNS configuration values
    current_listen_port = read_nginx_config('listen')
    if current_listen_port == 'ssl':
        current_listen_port = '443'
    current_server_name = read_nginx_config('server_name')
    current_SSL_crt = read_nginx_config('ssl_certificate')

    if current_SSL_crt:
        CASSL_CERT_PATH = f'/etc/letsencrypt/live/{current_server_name}/fullchain.pem'
    else:
        CASSL_CERT_PATH = 'None'

    if current_SSL_crt == SSL_CERT_PATH:
        current_ssl_status = 'Self-Signed'
    elif current_SSL_crt == CASSL_CERT_PATH:
        current_ssl_status = 'CA Validated'
    else:
        current_ssl_status = 'Disabled'

    #Read SSL certificate status
    if current_SSL_crt:
        output = read_ssl(current_SSL_crt)
        common_name, organization_name, expiry_date = output.split(',')

        # Handle empty values by replacing them with None
        if common_name == '':
            common_name = 'None'
        if organization_name == '':
            organization_name = 'None'
        if expiry_date == '':
            expiry_date = 'None'

        current_date = datetime.now()
        current_date =current_date.strftime('%Y-%m-%d %H:%M:%S')

        if expiry_date and expiry_date < current_date:
            expiry_date = 'Expired'
    else:
        common_name, organization_name, expiry_date = 'None', 'None', 'None'

    #Read service status
    nginx_status = get_ctl_status('nginx')
    gunicorn_status = get_ctl_status('a2d')

    response_data = {
        "listen_port": current_listen_port,
        "server_name": current_server_name,
        "current_ssl_status": current_ssl_status,
        "common_name": common_name,
        "organization_name": organization_name,
        "expiry_date": expiry_date,
        "nginx_status": nginx_status,
        "gunicorn_status": gunicorn_status
    }
    
    return jsonify(response_data)

#Get systemctl status
def get_ctl_status(ctl_name):
    try:
        output = subprocess.check_output(['systemctl', 'status', ctl_name], text=True)
        ctl_status = re.search(r'since\s(.*)', output).group(1)
        ctl_status = ctl_status.split(";")[1].strip()
        ctl_status = str(ctl_status)
        return ctl_status
        
    except subprocess.CalledProcessError as e:
        ctl_status = str(e)
        return ctl_status
