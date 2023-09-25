import os
from flask import Flask, render_template, request, session, redirect
from a2dapp.routes.auth import auth_routes
from a2dapp.routes.run import run_routes
from a2dapp.routes.dns import dns_routes
from a2dapp.routes.system import system_routes
from a2dapp.routes.network import network_routes
from a2dapp.routes.config import config_routes
from a2dapp.routes.reset import reset_routes
from a2dapp.routes.data import data_routes, get_adv_conf_values
from a2dapp.modals.creds import get_credentials

app = Flask(__name__)

#Storing session key implemented to avoid nginx error
SESSION_KEY_FILE = "/etc/a2d/.keys/session_key.bin"
SESSION_KEY_DIR = os.path.dirname(SESSION_KEY_FILE)

def generate_and_store_session_key():
    if not os.path.exists(SESSION_KEY_DIR):
        try:
            os.makedirs(SESSION_KEY_DIR)
        except OSError as e:
            pass
    if os.path.exists(SESSION_KEY_DIR):
        session_key = os.urandom(32)
        with open(SESSION_KEY_FILE, "wb") as key_file:
            key_file.write(session_key)
    else:
        pass

def load_session_key():
    try:
        with open(SESSION_KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        return None

def set_session_key():
    session_key = load_session_key()
    if session_key is None:
        generate_and_store_session_key()
        session_key = load_session_key()
    return session_key

app.secret_key = set_session_key()

# Register the auth_routes blueprint
app.register_blueprint(auth_routes)
app.register_blueprint(run_routes)
app.register_blueprint(config_routes)
app.register_blueprint(data_routes)
app.register_blueprint(dns_routes)
app.register_blueprint(system_routes)
app.register_blueprint(network_routes)
app.register_blueprint(reset_routes)

@app.route('/')
def home():
    if 'pin' in session:
        creds = get_credentials()
        active = 'Dashboard'
        service_status = request.args.get('service_status')
        last_run_human = request.args.get('last_run_human')
        run_interval = request.args.get('run_interval')
        callsign = request.args.get('callsign')
        callsign2 = request.args.get('callsign2')
        all_files_exist = request.args.get('allFilesExist')
        intervalmin, intervalh, ssids, logcounts = get_adv_conf_values()
        return render_template(
            'index.html', 
            creds=creds, 
            active=active, 
            intervalmin=intervalmin, 
            intervalh=intervalh, 
            ssids=ssids, 
            logcounts=logcounts, 
            service_status=service_status, 
            last_run_human=last_run_human, 
            run_interval=run_interval, 
            callsign=callsign, 
            callsign2=callsign2, 
            all_files_exist=all_files_exist
        )
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9333)
