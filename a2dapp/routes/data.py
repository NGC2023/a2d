from flask import Blueprint, jsonify, request, redirect
import os
import sqlite3
import configparser
import datetime
from a2dapp.modals.creds import get_credentials
from a2dapp.routes.run import restart_service
from a2dapp.routes.auth import login_required
from a2dapp.routes.handle_db import reset_dbs

data_routes = Blueprint('data', __name__)

adv_conf = '/etc/a2d/a2d_adv_conf.ini'
runscript_data = '/etc/a2d/runscript_data.ini'

@data_routes.route('/fetch-logs')
@login_required
def fetch_logs():
    if os.path.exists('/var/lib/a2d/dbs/aprs_messages.db') and os.path.exists('/var/lib/a2d/dbs/pseudo_aprs_messages.db'):
        aprs_db_path = '/var/lib/a2d/dbs/aprs_messages.db'
        pseudo_db_path = '/var/lib/a2d/dbs/pseudo_aprs_messages.db'

        config = configparser.ConfigParser()
        config.optionxform = lambda option: option  # Preserve case sensitivity
        config.read(adv_conf)
        max_logs = config.getint('LOGS', 'NumberOfLogs', fallback='')

        try:
            # Connect to the aprs database
            connection = sqlite3.connect(aprs_db_path)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM aprs_messages')
            aprs_rows = cursor.fetchall()
            connection.close()

            # Connect to the pseudo_aprs_messages database
            connection = sqlite3.connect(pseudo_db_path)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM pseudo_aprs_messages')
            pseudo_aprs_rows = cursor.fetchall()
            connection.close()

            # Convert the lists of rows to sets for easy comparison
            aprs_set = set(aprs_rows)
            pseudo_aprs_set = set(pseudo_aprs_rows)

            # Find the difference between the two sets (rows present in aprs_messages but not in pseudo_aprs_messages)
            diff_set = aprs_set - pseudo_aprs_set

            # Sort the logs in descending order based on the first element (row[0])
            logs = []
            count = 0  # Counter to keep track of the number of logs added
            for row in sorted(diff_set, reverse=True, key=lambda x: x[0]):
                log = f'{row[0]} > {row[1]} ({row[3]}): {row[2]}'
                logs.append(log)
                count += 1
                if count >= max_logs:  # Limit the number of logs user setting
                    break

            return jsonify(logs)

        except sqlite3.OperationalError:
            pass

    return jsonify([])  # Return an empty list if an error occurs

@data_routes.route('/save-adv-conf', methods=['POST'])
@login_required
def save_adv_conf():
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option  # Preserve case sensitivity
    config.read(adv_conf)
    previous_ssids = config.get('SSID', 'PreferredSSIDs', fallback='').split(',')

    # Update the values in the config object
    intervalmin = request.form['intervalmin']
    intervalh = request.form['intervalh']
    ssids = ','.join(request.form.getlist('ssids[]'))
    ssids_list = ssids.split(',')
    logcounts = request.form['logcounts']

    config['LOGS']['NumberOfLogs'] = logcounts

    if intervalmin == '0' and intervalh == '0':
        config['Timer']['IntervalMinutes'] = '15'
        config['Timer']['IntervalHours'] = '0'
    elif intervalmin == '1' and intervalh == '0':
        config['Timer']['IntervalMinutes'] = '2'
        config['Timer']['IntervalHours'] = '0'
    else:
        config['Timer']['IntervalMinutes'] = intervalmin
        config['Timer']['IntervalHours'] = intervalh
    
    if previous_ssids != ssids_list:
        if ssids is None:
            config['SSID']['PreferredSSIDs'] = '0'
        else:
            config['SSID']['PreferredSSIDs'] = ssids
        reset_dbs()

    with open(adv_conf, 'w') as config_file:
        config.write(config_file, space_around_delimiters=False)

    restart_service()
    return redirect('/')

def get_adv_conf_values():
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option  # Preserve case sensitivity
    config.read(adv_conf)

    intervalmin = config.get('Timer', 'IntervalMinutes', fallback='')
    intervalh = config.get('Timer', 'IntervalHours', fallback='')
    ssids = config.get('SSID', 'PreferredSSIDs', fallback='').split(',')
    logcounts = config.get('LOGS', 'NumberOfLogs', fallback='')

    return intervalmin, intervalh, ssids, logcounts


@data_routes.route('/for-dash')
@login_required
def for_dash():
    credentials = get_credentials()
    #Get callsign and callsign2
    callsign = credentials.get('callsign', 'Setup Configuration')
    callsign2 = credentials.get('callsign')
    
    #ssids-display
    config = configparser.ConfigParser()
    config.read(adv_conf)
    ssids_display = config.get('SSID', 'PreferredSSIDs', fallback='').split(',')
    ssids_display = ['-{}'.format(ssid) for ssid in ssids_display if ssid.strip()]
    ssids_display = ' '.join(ssids_display)

    #Run interval
    intervalmin = config.get('Timer', 'IntervalMinutes', fallback='')
    intervalh = config.get('Timer', 'IntervalHours', fallback='')
    run_interval = f"{intervalh}h {intervalmin}min"
    
    #Last run
    config.read(runscript_data)
    # Get the values for last run unix time
    last_run_unix = config.get('InternalTimeStamp', 'LastRunTime', fallback='')
    last_run_human = 'None' if not last_run_unix else datetime.datetime.fromtimestamp(float(last_run_unix)).strftime('%Y-%m-%d %H:%M:%S')

    dash_data = {
        "callsign": callsign,
        "callsign2": callsign2,
        "ssids_display": ssids_display,
        "run_interval": run_interval,
        "last_run_human": last_run_human
    }

    return jsonify(dash_data)
