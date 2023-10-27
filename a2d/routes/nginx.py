import subprocess
import re

NGINX_CONFIG_PATH = '/etc/nginx/conf.d/00-a2d.conf'
CORE_NGINX_CONF = '/etc/nginx/nginx.conf'

def reload_nginx():
    try:
        subprocess.run(["systemctl", "reload", "nginx"], check=True)
    except subprocess.CalledProcessError as e:
        return "Error reloading nginx:", e

def read_nginx_config(key):
    try:
        with open(NGINX_CONFIG_PATH, 'r') as config_file:
            for line in config_file:
                if line.strip().startswith(f"{key} "):
                    return line.split()[-1].rstrip(';')
    except Exception as e:
        return f"Error reading nginx conf: {e}"

def disable_default_ng():
    with open(CORE_NGINX_CONF, 'r') as nginx_conf_file:
        nginx_conf_content = nginx_conf_file.readlines()

    # Search for the line with 'include /etc/nginx/sites-enabled/*;' and comment it out
    for i, line in enumerate(nginx_conf_content):
        if 'include /etc/nginx/sites-enabled/*;' in line:
            if not line.startswith('#'):
                nginx_conf_content[i] = '#' + line

    with open(CORE_NGINX_CONF, 'w') as nginx_conf_file:
        nginx_conf_file.writelines(nginx_conf_content)

def enable_default_ng():
    with open(CORE_NGINX_CONF, 'r') as nginx_conf_file:
        nginx_conf_content = nginx_conf_file.readlines()

    # Search for the line with 'include /etc/nginx/sites-enabled/*;' and uncomment it
    for i, line in enumerate(nginx_conf_content):
        if re.match(r'^\s*#\s*include /etc/nginx/sites-enabled/\*;', line):
            nginx_conf_content[i] = re.sub(r'^\s*#\s*', '', line)

    with open(CORE_NGINX_CONF, 'w') as nginx_conf_file:
        nginx_conf_file.writelines(nginx_conf_content)
