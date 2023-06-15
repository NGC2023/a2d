#coding=utf-8
#!/usr/bin/env python

import os
import sys
from requests.auth import HTTPBasicAuth
import sqlite3
import json
import requests
from utils.decr_usrinfo import retrieve_usrinfo
from cryptography.fernet import Fernet

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the 'utils' directory to the Python module search path if not already present
utils_dir = os.path.join(current_dir, 'utils')
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

# Retrieve values from the retrieve_usrinfo function
data = retrieve_usrinfo()
APRSAPI_KEY = data['APRSAPI_KEY']
DAPNET_USER = data['DAPNET_USER']
DAPNET_PASS = data['DAPNET_PASS']

#Database directory
data_dir = f'/var/lib/a2d/dbs'

# Establish connection to the SQLite databases
callssid_db = f'{data_dir}/callssid.db'
conn = sqlite3.connect(callssid_db)
cursor = conn.cursor()

# Retrieve data from the table
cursor.execute('SELECT * FROM callssid')
rows = cursor.fetchall()

# Establish connection to the SQLite database
ham_info_db = f'{data_dir}/ham_info.db'
conn = sqlite3.connect(ham_info_db)
cursor = conn.cursor()

# Retrieve data from the table
cursor.execute('SELECT * FROM ham_info')
row = cursor.fetchall()

# DAPNET function
def dapnet(new_msg):
    login = DAPNET_USER
    passwd = DAPNET_PASS
    text = new_msg
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
    push_to_dapnet(text, callsign, login, passwd, url, txgroup)

# Create a SQLite database
aprs_messages_db = f'{data_dir}/aprs_messages.db'
conn = sqlite3.connect(aprs_messages_db)
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''CREATE TABLE IF NOT EXISTS aprs_messages
             (messageid TEXT PRIMARY KEY, srccall TEXT, message TEXT, trgcall TEXT)''')

# Get the current number of rows in the table
cursor.execute("SELECT COUNT(*) FROM aprs_messages")
row_count = cursor.fetchone()[0]

for c in rows:
    if c[2] == 0:
        url = "https://api.aprs.fi/api/get?what=msg&dst=" + c[1] + "&apikey="+APRSAPI_KEY+"&format=json"
        trgcall = c[1]
    else:
        url = "https://api.aprs.fi/api/get?what=msg&dst=" + c[1] + "-" + c[2] + "&apikey="+APRSAPI_KEY+"&format=json"
        trgcall = c[2]

    aprs = requests.get(url)
    aprs = aprs.json()

    try: #If ARPS server returns "Get failed, query ratelimit" (because of too frequent requests)
        entries = aprs['entries']
    except KeyError:
        continue

    for item in aprs['entries']:
        messageid = item['messageid']
        srccall = item['srccall']
        message = item['message']

        # Check if messageid already exists in the SQLite table
        cursor.execute("SELECT messageid FROM aprs_messages WHERE messageid = ?", (messageid,))
        result = cursor.fetchone()

        # If messageid doesn't exist, insert the data into the SQLite table and print the new entry
        if not result:
            cursor.execute("INSERT INTO aprs_messages (messageid, srccall, message, trgcall) VALUES (?, ?, ?, ?)",
                           (messageid, srccall, message, trgcall))

            new_msg = srccall + '(' + trgcall + '):' + message
            print(new_msg)
            dapnet(new_msg)

# Commit the changes and close the connection
conn.commit()
conn.close()
