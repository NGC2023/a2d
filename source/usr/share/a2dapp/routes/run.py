import os
import subprocess
import configparser
from crontab import CronTab
from flask import Blueprint, redirect, jsonify
from routes.auth import login_required

run_routes = Blueprint('run', __name__)

def generate_cron_job(interval_minutes, interval_hours, interval_hours_uni):
    cron_jobs = []
    if interval_minutes == 0 and interval_hours == 0:
        cron_jobs.append(f"*/15 * * * * /usr/bin/python /usr/share/a2d/runscripts.py")
    elif interval_minutes == 1 and interval_hours == 0:
        cron_jobs.append(f"*/2 * * * * /usr/bin/python /usr/share/a2d/runscripts.py")
    elif interval_minutes != 0 and interval_hours == 0:
        cron_jobs.append(f"*/{interval_minutes} * * * * /usr/bin/python /usr/share/a2d/runscripts.py")
    elif interval_minutes == 0 and interval_hours != 0:
        cron_jobs.append(f"0 */{interval_hours} * * * /usr/bin/python /usr/share/a2d/runscripts.py")    
    elif interval_minutes != 0 and interval_minutes != 1 and interval_hours != 0 and interval_hours != 1:
        cron_jobs.append(f"*/{interval_minutes} */{interval_hours} * * * /usr/bin/python /usr/share/a2d/runscripts.py")
    else:
        cron_jobs.append(f"0 */{interval_hours_uni} * * * /usr/bin/python /usr/share/a2d/runscripts.py")
        cron_jobs.append(f"0-59/{interval_minutes} * * * * /usr/bin/python /usr/share/a2d/runscripts.py")
    return cron_jobs

def add_cronjob():
    # Get the current user's cron table
    cron = CronTab(user=True)

    # Define the command to be executed by the cron job
    command = '/usr/bin/python /usr/share/a2d/runscripts.py'

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

    # Add each cron job individually
    for cron_schedule in cron_schedule_list:
        job = cron.new(command=command)
        cron_parts = cron_schedule.split()
        job.setall(' '.join(cron_parts[:5]))

    # Write the changes to the cron table
    cron.write()

def check_cronjob():
    # Get the current user's cron table
    cron = CronTab(user=True)

    # Find the cron job that matches the specified command
    command = '/usr/bin/python /usr/share/a2d/runscripts.py'
    runstatus = "Stopped"  # Set a default value before the loop
    for job in cron:
        if job.command == command:
            runstatus = "Running"  # Update runstatus only when a matching cron job is found
            break  # No need to continue the loop once a match is found

    return runstatus

def remove_cronjob():
    # Get the current user's cron table
    cron = CronTab(user=True)

    # Find the cron job that matches the specified command
    command = '/usr/bin/python /usr/share/a2d/runscripts.py'
    for job in cron:
        if job.command == command:
            # Remove the cron job
            cron.remove(job)

    # Write the changes to the cron table
    cron.write()

@run_routes.route('/start-service')
@login_required
def start_service():
    if os.path.isfile('/etc/a2d/.creds/a2d_AnDinfo.conf'):
        runstatus = check_cronjob()
        if runstatus == "Stopped":
            # Call the function to add the cron job
            add_cronjob()
            run_command = ["nohup", "/usr/share/a2d/scripts/run_a2d.sh", "&"]
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
