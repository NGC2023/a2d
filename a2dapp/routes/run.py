import os
import subprocess
import configparser
from flask import Blueprint, redirect, jsonify
from a2dapp.routes.auth import login_required

run_routes = Blueprint('run', __name__)

def generate_cron_job(interval_minutes, interval_hours, interval_hours_uni):
    cron_jobs = []
    if interval_minutes == 0 and interval_hours == 0:
        cron_jobs.append(f"*/15 * * * * root /usr/bin/python3 -m a2d.runscripts")
    elif interval_minutes == 1 and interval_hours == 0:
        cron_jobs.append(f"*/2 * * * * root /usr/bin/python3 -m a2d.runscripts")
    elif interval_minutes != 0 and interval_hours == 0:
        cron_jobs.append(f"*/{interval_minutes} * * * * root /usr/bin/python3 -m a2d.runscripts")
    elif interval_minutes == 0 and interval_hours != 0:
        cron_jobs.append(f"0 */{interval_hours} * * * root /usr/bin/python3 -m a2d.runscripts")    
    elif interval_minutes != 0 and interval_minutes != 1 and interval_hours != 0 and interval_hours != 1:
        cron_jobs.append(f"*/{interval_minutes} */{interval_hours} * * * root /usr/bin/python3 -m a2d.runscripts")
    else:
        cron_jobs.append(f"0 */{interval_hours_uni} * * * root /usr/bin/python3 -m a2d.runscripts")
        cron_jobs.append(f"0-59/{interval_minutes} * * * * root /usr/bin/python3 -m a2d.runscripts")
    return cron_jobs

def add_cronjob():
    # Read values from the configuration file
    config_file = '/etc/a2d/a2d_adv_conf.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    # Get the values for IntervalMinutes and IntervalHours
    interval_minutes = int(config.get('Timer', 'IntervalMinutes'))
    interval_hours = int(config.get('Timer', 'IntervalHours'))
    interval_hours_uni = interval_hours + 1

    # Generate the cron job schedule using the updated function
    cron_schedule_list = generate_cron_job(interval_minutes, interval_hours, interval_hours_uni)

    # Create and write the cron job to /etc/cron.d/a2d.cron
    with open('/etc/cron.d/a2d', 'a') as cron_file:
        for cron_schedule in cron_schedule_list:
            cron_file.write(f'{cron_schedule}\n')

def check_cronjob():
    # Find the cron job that matches the specified command
    command = '/usr/bin/python3 -m a2d.runscripts'
    runstatus = "Stopped"  # Set a default value before the loop
    try:
        with open('/etc/cron.d/a2d', 'r') as cron_file:
            for line in cron_file:
                if line.strip().endswith(command):
                    runstatus = "Running"
                    break  # No need to continue reading the file once a match is found
    except FileNotFoundError:
        pass  # Handle the case when the file doesn't exist

    return runstatus

def remove_cronjob():
    # Find the cron job that matches the specified command
    command = '/usr/bin/python3 -m a2d.runscripts'

    # Initialize the lines variable to an empty list to avoid error if file not found
    lines = []
    
    try:
        with open('/etc/cron.d/a2d', 'r') as cron_file:
            lines = cron_file.readlines()
    except FileNotFoundError:
        return  # Handle the case when the file doesn't exist
    
    # Filter out lines that do not contain the specified command
    filtered_lines = [line for line in lines if not line.strip().endswith(command)]

    # Write the filtered lines back to the /etc/cron.d/a2d.cron file
    with open('/etc/cron.d/a2d', 'w') as cron_file:
        cron_file.writelines(filtered_lines)

@run_routes.route('/start-service')
@login_required
def start_service():
    if os.path.isfile('/etc/a2d/.creds/a2d_AnDinfo.conf'):
        runstatus = check_cronjob()
        if runstatus == "Stopped":
            # Call the function to add the cron job
            add_cronjob()
            run_command = ["nohup", "/usr/share/scripts/run_a2d.sh", "&"]
            subprocess.Popen(run_command)
        return redirect('/')
    return redirect('/')

@run_routes.route('/stop-service')
@login_required
def stop_service():
    runstatus = check_cronjob()
    if runstatus == "Running":
        # Call the function to remove the cron job
        remove_cronjob()
    return redirect('/')

def restart_service():
    runstatus = check_cronjob()
    if runstatus == "Running":
        remove_cronjob()
        add_cronjob()

@run_routes.route('/service-status')
@login_required
def service_status():
    runconfig_file = '/etc/a2d/runscript_data.ini'
    runconfig = configparser.ConfigParser()
    runconfig.read(runconfig_file)
    aprs_server = runconfig.get('APRSKeyVerify', 'apiKeyStatus', fallback='')
    
    dapconfig = configparser.ConfigParser()
    dapconfig_file = '/etc/a2d/dapnet_data.ini'
    dapconfig.read(dapconfig_file)
    dapnet_server = dapconfig.get('DAPNETVerify', 'HTTPStatus', fallback='')

    status_messages = {
        ('invalid', '201'): 'Invalid APRS API key',
        ('wrong', '201'): 'Wrong APRS API key',
        ('valid', '401'): 'Wrong DAPNET user or passwd',
        ('valid', '400'): 'Wrong callsign or txgroup',
        ('invalid', '401'): 'Invalid APRS API key/Wrong DAPNET user or passwd',
        ('wrong', '401'): 'Wrong APRS API key/Wrong DAPNET user or passwd',
        ('invalid', '400'): 'Invalid APRS API key/Wrong callsign or txgroup',
        ('wrong', '400'): 'Wrong APRS API key/Wrong callsign or txgroup',
    }

    if aprs_server == 'valid' and dapnet_server == '201':
        service_status = {
            "color_status": True,
            "status_message": check_cronjob()
        }
    
    elif aprs_server == 'valid' and dapnet_server not in ('201', '401', '400'):
        service_status = {
            "color_status": False,
            "status_message": "DAPNET HTTP" + dapnet_server
        }
    else:
        service_status = {
            "color_status": False,
            "status_message": status_messages.get((aprs_server, dapnet_server))
        }

    return jsonify({"service_status": service_status})
