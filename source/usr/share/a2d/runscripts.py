#coding=utf-8
#!/usr/bin/env python

import os
import subprocess
import time
from utils.get_aprs import aprs_check
from utils.utils import remove_cronjob, read_ini_data, write_ini_data

runscript_data = '/etc/a2d/runscript_data.ini'

def run_script():
    config = read_ini_data(runscript_data)
    current_time = time.time()
    str_current_time = str(current_time)

    #Check when was the last APRS Check
    last_aprs_check_ini = config.get('APRSCheck', 'LastCheck', fallback='')
    if last_aprs_check_ini:
        last_aprs_check_ini = float(last_aprs_check_ini)
        last_check_interval = current_time - last_aprs_check_ini

        if last_check_interval >= 60 * 3:
            config.set('APRSCheck', 'APRSCheck', 'unverified')
            write_ini_data(config, runscript_data)

    aprs_check_ini = config.get('APRSCheck', 'APRSCheck', fallback='')
    if aprs_check_ini == 'unverified':
        config.set('APRSCheck', 'LastCheck', str_current_time)

        # Check the APRS API response for the current callsign and API key
        entries_check = aprs_check()

        if entries_check is not None and "code" in entries_check:
            code = entries_check["code"]
            if code == "apikey-wrong":
                # Write the key status in /etc/a2d/runscript_data.ini
                config.set('APRSKeyVerify', 'apiKeyStatus', 'wrong')
                write_ini_data(config, runscript_data)
                
                # Terminate the script if the API key is wrong
                remove_cronjob()
                return

            elif code == "apikey-invalid":
                # Write the key status in /etc/a2d/runscript_data.ini
                config.set('APRSKeyVerify', 'apiKeyStatus', 'invalid')
                write_ini_data(config, runscript_data)

                # Terminate the script if the API key is invalid
                remove_cronjob()
                return

        config.set('APRSKeyVerify', 'apiKeyStatus', 'valid')
        config.set('APRSCheck', 'APRSCheck', 'verified')
        write_ini_data(config, runscript_data)

    # Continue running the script to restrict aprs pull
    last_aprs_pull = config.get('APRSTimeStamp', 'LastAPRSPull', fallback='')
    if last_aprs_pull:
        last_aprs_pull = float(last_aprs_pull)
        time_difference = current_time - last_aprs_pull
        ideal_aprs_interval = 121
    
        if time_difference <= ideal_aprs_interval:
            time_to_sleep = ideal_aprs_interval - time_difference
            time.sleep(time_to_sleep)

    # Continue running the script and write the start time
    #Write start time
    config.set('InternalTimeStamp', 'LastRunTime', str_current_time)
    write_ini_data(config, runscript_data)

    db_file_path = "/var/lib/a2d/dbs/aprs_messages.db"
    if os.path.exists(db_file_path):
        scripts = ["build_usrdbs.py", "push_a2d.py"]
    else:
        scripts = ["build_usrdbs.py", "pseudorun.py"]

    for script in scripts:
        script_path = "/usr/share/a2d/" + script
        subprocess.call(["python", script_path])

    str_current_time2 = str(time.time())
    config.set('APRSTimeStamp', 'LastAPRSPull', str_current_time2)
    write_ini_data(config, runscript_data)

if __name__ == '__main__':
    run_script()
