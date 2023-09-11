from requests.auth import HTTPBasicAuth
import requests
from a2d.a2d_utils.decr_usrinfo import retrieve_usrinfo
from a2d.a2d_utils.a2d_utils import establish_connection, retrieve_data_from_table, remove_cronjob, read_ini_data, write_ini_data

# Retrieve values from the retrieve_usrinfo function
data = retrieve_usrinfo()
DAPNET_USER = data['dapnet_user']
DAPNET_PASS = data['dapnet_pass']

#File and Directories
data_dir = f'/var/lib/a2d/dbs'

# Establish connection to the SQLite database
ham_info_db = f'{data_dir}/ham_info.db'
conn, cursor = establish_connection(ham_info_db)
row = retrieve_data_from_table(cursor, 'ham_info')
conn.close()

# DAPNET function
def dapnet(new_msg_str):
    login = DAPNET_USER
    passwd = DAPNET_PASS
    text = new_msg_str
    callsign = [row[0][1]]
    url = 'http://www.hampager.de:8080/calls'
    txgroup = row[0][2]

	# DAPNET push functions
    def push_to_dapnet(text, callsign, login, passwd, url, txgroup):
        payload = {
            "text": text,
            "callSignNames": callsign,
            "transmitterGroupNames": [txgroup],
            "emergency": False
        }
        headers = {
        "Content-Type": "application/json"
        }
        auth = HTTPBasicAuth(login, passwd)
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        return response.status_code

	# DAPNET send
    status_code = push_to_dapnet(text, callsign, login, passwd, url, txgroup)
    
    # Update the configuration file with the status code
    dapnet_data = '/etc/a2d/dapnet_data.ini'
    config = read_ini_data(dapnet_data)
    status_code_str = str(status_code)
    config.set('DAPNETVerify', 'HTTPStatus', status_code_str)
    write_ini_data(config, dapnet_data)
    
    #Stop cron if the status code is not 201
    if status_code_str != '201':
        remove_cronjob()
