import os
from flask import Blueprint, render_template, request, redirect, session
from modals.user import verify_pin, create_user, create_user_passphrase, decrypt_user_passphrase
from modals.creds import save_credentials, get_credentials
from routes.handle_db import reset_dbs
from functools import wraps
import configparser

auth_routes = Blueprint('auth', __name__)

def handle_digits():
    digit1 = request.form['digit1']
    digit2 = request.form['digit2']
    digit3 = request.form['digit3']
    digit4 = request.form['digit4']
    digit5 = request.form['digit5']
    digit6 = request.form['digit6']
    pin = digit1 + digit2 + digit3 + digit4 + digit5 + digit6
    return pin

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = handle_digits()
        if verify_pin(pin):
            session['pin'] = pin
            return redirect('/')
        else:
            return render_template('login.html', error=True)
    return render_template('login.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Check if the user is authenticated before accessing protected routes
def passphrase_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if check_passphrase_file() == "user_passphrase.bin does not exist." or passphrase_authenticated():
            return f(*args, **kwargs)
        return render_template('verifypassphrase.html')
    return decorated_function

# Check if the user has entered the correct passphrase
def passphrase_authenticated():
    return session.get('pp_authenticated', False)

@auth_routes.route('/create-passphrase', methods=['GET', 'POST'])
@passphrase_required
def passphrase_change():
    if request.method == 'POST':
        pin = handle_digits()
        create_user(pin)
        session['pin'] = pin
        passphrase = request.form['passphrase']
        create_user_passphrase(passphrase)
        session['passphrase'] = passphrase
        return redirect('/logout')
    return render_template('updatepin.html')

@auth_routes.route('/verify-passphrase', methods=['POST'])
def verify_passphrase():
    passphrase = request.form.get('passphrase')
    stored_passphrase = decrypt_user_passphrase()
    if passphrase == stored_passphrase:
        session['passphrase'] = passphrase
        session['pp_authenticated'] = True
        return redirect('/create-passphrase')
    else:
        return redirect('/logout')

@auth_routes.route('/pin-change', methods=['GET', 'POST'])
def pin_change():
    if request.method == 'POST':
        pin = handle_digits()
        create_user(pin)
        session['pin'] = pin
        return redirect('/logout')
    else:
        if check_passphrase_file() == "user_passphrase.bin does not exist.":
            return redirect('/create-passphrase')
        return render_template('verifypassphrase.html')

@auth_routes.route('/check_pin_file')
def check_pin_file():
    pin_file_exists = os.path.isfile('/etc/a2d/.creds/user_pin.bin')
    if pin_file_exists:
        message = "7965732062696e"
    else:
        message = "6e6f2062696e"
    return message

def check_passphrase_file():
    passphrase_file_exists = os.path.isfile('/etc/a2d/.creds/user_passphrase.bin')
    if passphrase_file_exists:
        message = "user_passphrase.bin exists."
    else:
        message = "user_passphrase.bin does not exist."
    return message

# Define a decorator function to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'pin' not in session:
            return redirect('/logout')
        return f(*args, **kwargs)
    return decorated_function

@auth_routes.route('/AnD-creds', methods=['POST'])
@login_required
def handle_creds():
    callsign = request.form['callsign']
    txgroup = request.form['txgroup']
    dapnetuser = request.form['dapnetuser']
    dapnetpass = request.form['dapnetpass']
    aprsapi = request.form['aprsapi']

    credentials = get_credentials()
    previous_callsign = credentials.get('callsign')
    previous_txgroup = credentials.get('txgroup')
    previous_dapnetuser = credentials.get('dapnetuser')
    previous_dapnetpass = credentials.get('dapnetpass')

    if previous_callsign != callsign or previous_txgroup != txgroup or previous_dapnetuser != dapnetuser or previous_dapnetpass != dapnetpass:
        reset_dbs()
        # Update the configuration file with the status code
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config.read('/etc/a2d/dapnet_data.ini')
        reset_dapnet_http_code = '201'
        config.set('DAPNETVerify', 'HTTPStatus', reset_dapnet_http_code)   
        with open('/etc/a2d/dapnet_data.ini', 'w') as configfile:
            config.write(configfile)     
        
        runconfig = configparser.ConfigParser()
        runconfig.optionxform = lambda option: option
        runconfig.read('/etc/a2d/runscript_data.ini')
        reset_aprs_check_ini = 'unverified'
        runconfig.set('APRSCheck', 'APRSCheck', reset_aprs_check_ini)
        with open('/etc/a2d/runscript_data.ini', 'w') as runconfigfile:
            runconfig.write(runconfigfile)
    
    save_credentials(callsign, txgroup, dapnetuser, dapnetpass, aprsapi)
    return redirect('/')
