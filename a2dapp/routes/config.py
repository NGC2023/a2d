import os
import hashlib
import yaml
from flask import Blueprint, request, redirect, render_template, Response
from a2dapp.routes.auth import login_required
from a2dapp.modals.user import decrypt_user_passphrase
from a2dapp.modals.creds import get_credentials

config_routes = Blueprint('config', __name__)

file_paths = {
    "00": "/etc/a2d/a2d_adv_conf.ini",
    "01": "/etc/a2d/.creds/a2d_AnDinfo.conf",
    "10": "/etc/a2d/.keys/a2d_AnDinfo.key",
}

@config_routes.route("/export", methods=["POST"])
@login_required
def export_files():
    passphrase = request.form.get("passphrase")
    if not verify_passphrase(passphrase):
        return "Invalid Passphrase", 400

    all_files_exist = True
    for file_path in file_paths.values():
        if not os.path.exists(file_path):
            all_files_exist = False
            break

    if not all_files_exist:
        return "Files missing", 401

    if all_files_exist:
        data = {file_name: read_binary_file(file_path) for file_name, file_path in file_paths.items()}
        watermark = calculate_watermark(data)
        export_data = {"d": data, "f": watermark}
        yaml_data = yaml.dump(export_data)
        sha256 = hashlib.sha256()
        sha256.update(yaml_data.encode('utf-8'))

        response = Response(yaml_data, mimetype="application/x-yaml")
        response.headers["Content-Disposition"] = "attachment; filename=a2d_config_backup.yaml"

        return response

@config_routes.route("/import", methods=["POST"])
@login_required
def import_files():
    passphrase = request.form.get("passphrase")
    if not verify_passphrase(passphrase):
        return "Invalid Passphrase", 400

    import_file = request.files.get("import_file")
    if import_file and import_file.filename.endswith(".yaml"):
        yaml_data = import_file.read().decode('utf-8')
        data = yaml.safe_load(yaml_data)
        watermark = data.get("f")

        if verify_watermark(data["d"], watermark):
            if os.path.exists('/etc/a2d/.keys/a2d_AnDinfo.key'):
                os.chmod('/etc/a2d/.keys/a2d_AnDinfo.key', 0o644)
            for file_name, file_data in data["d"].items():
                if file_name in file_paths:
                    create_directory_if_not_exists(file_paths[file_name])
                    write_binary_file(file_paths[file_name], file_data)
            os.chmod('/etc/a2d/.keys/a2d_AnDinfo.key', 0o400)

            return redirect('/') #This wont work, implemented in client side
        else:
            return "File tampered", 401
    else:
        return "Invalid file", 402

def read_binary_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()

def write_binary_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(data)

def create_directory_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def calculate_watermark(data):
    yaml_data = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    sha256 = hashlib.sha256()
    sha256.update(yaml_data.encode('utf-8'))    
    return sha256.digest()

def verify_watermark(data, watermark):
    calculated_watermark = calculate_watermark(data)
    return calculated_watermark == watermark

def verify_passphrase(passphrase):
    stored_passphrase = decrypt_user_passphrase()
    return passphrase == stored_passphrase

@config_routes.route('/help-full')
@login_required
def help_full():
    creds = get_credentials
    return render_template('help_full.html', creds=creds)

@config_routes.route('/help-short')
def help_short():
    return render_template('help_short.html')
