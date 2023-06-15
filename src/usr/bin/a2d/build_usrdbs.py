import os
import configparser
import sqlite3
from utils.decr_usrinfo import retrieve_usrinfo
from cryptography.fernet import Fernet

data = retrieve_usrinfo()

# Retrieve values from the decrypted data
callsign_nossid = data['callsign_nossid']
txgroup = data['txgroup']

# DB directory path
data_dir = '/var/lib/a2d/dbs'

# Create the table if it doesn't exist
previous_values_db = f'{data_dir}/previous_values.db'
conn = sqlite3.connect(previous_values_db)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS previous_values (
    id INTEGER PRIMARY KEY,
    callsign TEXT,
    txgroup TEXT
)
''')

# Retrieve previous values from the database
cursor.execute('SELECT callsign, txgroup FROM previous_values')
row = cursor.fetchone()

# Check if there are changes in the decrypted data
if row is None or row[0] != callsign_nossid or row[1] != txgroup:
    # Store the new values in the database
    cursor.execute('DELETE FROM previous_values')
    cursor.execute('INSERT INTO previous_values (callsign, txgroup) VALUES (?, ?)', (callsign_nossid, txgroup))
    conn.commit()
    is_conf_changed = True
else:
    is_conf_changed = False

# Close the connection
conn.close()

# Read the configuration file
config = configparser.ConfigParser()
config.read("/etc/a2d/adv_conf.ini")

# Retrieve the PreferredSSIDs value
preferred_ssids = config.get("SSID", "PreferredSSIDs", fallback="")

# Update callssid.db if there are changes in is_conf_changed or PreferredSSIDs
update_callssid = is_conf_changed or preferred_ssids != ""

# Connect to the callssid.db
callssid_db = f'{data_dir}/callssid.db'
conn = sqlite3.connect(callssid_db)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS callssid (
    id INTEGER PRIMARY KEY,
    callsign TEXT,
    ssid TEXT
)
''')

# Delete existing entries from the table if is_conf_changed
if is_conf_changed:
    cursor.execute("DELETE FROM callssid")

# Check if PreferredSSIDs is empty or changed
if preferred_ssids:
    # Split PreferredSSIDs into a list of SSIDs
    ssids = preferred_ssids.split(",")

    # Delete the existing entries for the current callsign
    cursor.execute("DELETE FROM callssid WHERE callsign = ?", (callsign_nossid,))

    # Populate the table with SSIDs
    for i, ssid in enumerate(ssids):
        cursor.execute('''
        INSERT INTO callssid VALUES
        (?, ?, ?)''', (i, callsign_nossid, ssid.strip()))
else:
    # Delete the existing entries for the current callsign
    cursor.execute("DELETE FROM callssid WHERE callsign = ?", (callsign_nossid,))

    # Populate the table with 16 entries
    for i in range(16):
        cursor.execute('''
        INSERT INTO callssid VALUES
        (?, ?, ?)''', (i, callsign_nossid, str(i)))

# Commit the changes
conn.commit()

# Close the connection
conn.close()

# Update ham_info.db if is_conf_changed
if is_conf_changed:
    # Update ham_info.db
    ham_info_db = f'{data_dir}/ham_info.db'
    conn = sqlite3.connect(ham_info_db)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ham_info (
        id INTEGER PRIMARY KEY,
        callsign TEXT,
        txgroup TEXT
    )
    ''')
    cursor.execute('''
        REPLACE INTO ham_info VALUES
        (?, ?, ?)''', (1, callsign_nossid, txgroup)
    )
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
