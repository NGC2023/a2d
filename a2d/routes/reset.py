import os
import sqlite3
import shutil
from flask import Blueprint, request
import configparser
from a2d.routes.auth import login_required
from a2d.modals.user import decrypt_user_passphrase
from a2d.a2d_utils.a2d_utils import remove_cronjob
from a2d.routes.dns import update_nginx_config
from a2d.routes.certs import a2d_rm_selfssl, a2d_ca_list, a2d_rm_cassl, reload_nginx, enable_default_ng

reset_routes = Blueprint('reset', __name__)

adv_conf = '/etc/a2d/a2d_adv_conf.ini'
dapnet_data = '/etc/a2d/dapnet_data.ini'
runscript_data = '/etc/a2d/runscript_data.ini'

@reset_routes.route('/reset-portal', methods=['POST'])
@login_required
def reset_account():
    passphrase = request.form.get("passphrase")
    if not verify_passphrase(passphrase):
        return "Invalid Passphrase", 400
    
    reset_confirm = request.form['reset_confirm']
    selfSSL_delete = request.form['self_ssl_delete'] == 'true'
    caSSL_delete = request.form['ca_ssl_delete'] == 'true'
    
    if reset_confirm.lower() == 'delete':
        remove_cronjob()
        rm_dbs()
        
        #a2d_adv_conf.ini
        config1 = configparser.ConfigParser()
        config1.optionxform = lambda option: option  # Preserve case sensitivity
        config1.read(adv_conf)
        config1.set('Timer', 'IntervalMinutes', '15')
        config1.set('Timer', 'IntervalHours', '0')
        config1.set('SSID', 'PreferredSSIDs', '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15')
        config1.set('LOGS', 'NumberOfLogs', '150')
        with open(adv_conf, 'w') as config_file1:
            config1.write(config_file1, space_around_delimiters=False)
        
        #dapnet_data.ini
        config2 = configparser.ConfigParser()
        config2.optionxform = lambda option: option  # Preserve case sensitivity
        config2.read(dapnet_data)
        config2.set('DAPNETVerify', 'HTTPStatus', '201')
        with open(dapnet_data, 'w') as config_file2:
            config2.write(config_file2, space_around_delimiters=False)
        
        #runscript_data.ini
        config3 = configparser.ConfigParser()
        config3.optionxform = lambda option: option  # Preserve case sensitivity
        config3.read(runscript_data)
        config3.set('InternalTimeStamp', 'LastRunTime', '')
        config3.set('APRSKeyVerify', 'apiKeyStatus', 'valid')
        config3.set('APRSTimeStamp', 'LastAPRSPull', '')
        config3.set('APRSCheck', 'APRSCheck', 'verified')
        config3.set('APRSCheck', 'LastCheck', '')
        with open(runscript_data, 'w') as config_file3:
            config3.write(config_file3, space_around_delimiters=False)
        
        if selfSSL_delete:
            a2d_rm_selfssl()
            a2d_default_dns()

        if caSSL_delete:
            cassl_certs_list = a2d_ca_list()
            for rm_cassl_certs in cassl_certs_list:
                a2d_rm_cassl(rm_cassl_certs)
            a2d_default_dns()

        try:
            #Remove all creds and keys
            shutil.rmtree('/etc/a2d/.creds')
            shutil.rmtree('/etc/a2d/.keys')
        except Exception as e:
            pass
        
        return 'logout'
    else:
        return 'Type delete'

def verify_passphrase(passphrase):
    stored_passphrase = decrypt_user_passphrase()
    return passphrase == stored_passphrase

def a2d_default_dns():
    listen_port = '9331'
    set_selfssl_status = 'disable'
    server_name = '_'
    set_cassl_status = ''
    update_nginx_config(listen_port, server_name, set_selfssl_status, set_cassl_status)
    enable_default_ng()
    reload_nginx()

def rm_dbs():
    db_folder = '/var/lib/a2d/dbs'
    aprs_db_path = os.path.join(db_folder, 'aprs_messages.db')
    pseudo_aprs_db_path = os.path.join(db_folder, 'pseudo_aprs_messages.db')
    callssid_db_path = os.path.join(db_folder, 'callssid.db')
    ham_info_db_path = os.path.join(db_folder, 'ham_info.db')
    previous_values_db_path = os.path.join(db_folder, 'previous_values.db')

    try:
        clear_table(aprs_db_path, 'aprs_messages')
        clear_table(pseudo_aprs_db_path, 'pseudo_aprs_messages')
        clear_table(callssid_db_path, 'callssid')
        clear_table(ham_info_db_path, 'ham_info')
        clear_table(previous_values_db_path, 'previous_values')
    except Exception as e:
        pass

def clear_table(db_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'DELETE FROM {table_name}')

        conn.commit()
        conn.close()

        os.remove(db_path)

    except Exception as e:
        pass
