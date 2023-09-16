import os
import pickle
import hashlib
from flask import Blueprint, request, send_file, redirect, render_template
from a2dapp.routes.auth import login_required
from a2dapp.modals.user import decrypt_user_passphrase
from a2dapp.modals.creds import get_credentials

config_routes = Blueprint('config', __name__)

file_paths = {
    "a2d_adv_conf.ini": "/etc/a2d/a2d_adv_conf.ini",
    "a2d_AnDinfo.conf": "/etc/a2d/.creds/a2d_AnDinfo.conf",
    "a2d_AnDinfo.key": "/etc/a2d/.keys/a2d_AnDinfo.key",
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
        binary_filename = "a2d_config_backup.bin"
        with open(binary_filename, "wb") as binary_file:
            data = {file_name: read_binary_file(file_path) for file_name, file_path in file_paths.items()}
            watermark = calculate_watermark(data)
            pickle.dump((data, watermark), binary_file)
        return send_file(binary_filename, as_attachment=True, mimetype="application/octet-stream")

@config_routes.route("/import", methods=["POST"])
@login_required
def import_files():
    passphrase = request.form.get("passphrase")
    if not verify_passphrase(passphrase):
        return "Invalid Passphrase", 400

    import_file = request.files.get("import_file")
    if import_file and import_file.filename.endswith(".bin"):
        data, watermark = pickle.load(import_file)
        if verify_watermark(data, watermark):
            if os.path.exists('/etc/a2d/.keys/a2d_AnDinfo.key'):
                os.chmod('/etc/a2d/.keys/a2d_AnDinfo.key', 0o644)
            for file_name, file_data in data.items():
                if file_name in file_paths:
                    create_directory_if_not_exists(file_paths[file_name])
                    write_binary_file(file_paths[file_name], file_data)
            os.chmod('/etc/a2d/.keys/a2d_AnDinfo.key', 0o400)

            return redirect('/') #This dont work, implemented in client side.
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
    data_bytes = pickle.dumps(data)
    sha256 = hashlib.sha256()
    sha256.update(data_bytes)
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
