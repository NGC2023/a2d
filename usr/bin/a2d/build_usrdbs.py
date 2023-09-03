#coding=utf-8
#!/usr/bin/env python

import configparser
import multiprocessing
from utils.decr_usrinfo import retrieve_usrinfo
from utils.utils import establish_connection, create_table_if_not_exists, retrieve_data_from_table

def update_previous_values_db(previous_values_db, callsign_nossid, txgroup, condition1, condition2):
    conn, cursor = establish_connection(previous_values_db)

    create_table_if_not_exists(cursor, "previous_values", "(id INTEGER PRIMARY KEY, callsign TEXT, txgroup TEXT)")

    cursor.execute('SELECT callsign, txgroup FROM previous_values WHERE id = 1')
    row = cursor.fetchone()

    if row is None or row[0] != callsign_nossid:
        cursor.execute('REPLACE INTO previous_values (id, callsign, txgroup) VALUES (1, ?, ?)', (callsign_nossid, txgroup))
        conn.commit()
        condition1 = True
    elif row[1] != txgroup:
        cursor.execute('REPLACE INTO previous_values (id, callsign, txgroup) VALUES (1, ?, ?)', (callsign_nossid, txgroup))
        conn.commit()
        condition2 = True
    else:
        condition1 = False
        condition2 = False

    conn.close()
    return condition1, condition2

def update_callssid_db(callssid_db, callsign_nossid, ssids, condition1):
    conn, cursor = establish_connection(callssid_db)

    create_table_if_not_exists(cursor, "callssid", "(id INTEGER PRIMARY KEY, callsign TEXT, ssid TEXT)")

    callssid_conn, callssid_cursor = establish_connection(callssid_db)
    rows = retrieve_data_from_table(callssid_cursor, 'callssid')
    callssid_conn.close()

    # Get the SSIDs from the callssid database
    existing_ssids = [row[2] for row in rows if row[1] == callsign_nossid]

    if condition1:
        cursor.execute("DELETE FROM callssid")

    if ssids != existing_ssids:  # Compare SSIDs from the database with those in a2d_adv_conf.ini
        cursor.execute("DELETE FROM callssid WHERE callsign = ?", (callsign_nossid,))
        data = [(callsign_nossid, ssid.strip()) for ssid in ssids]
        cursor.executemany('INSERT OR REPLACE INTO callssid (callsign, ssid) VALUES (?, ?)', data)

    conn.commit()
    conn.close()
    pass

def update_ham_info_db(ham_info_db, callsign_nossid, txgroup, condition1, condition2):
    conn, cursor = establish_connection(ham_info_db)

    create_table_if_not_exists(cursor, "ham_info", "(id INTEGER PRIMARY KEY, callsign TEXT, txgroup TEXT)")

    if condition1 or condition2:
        cursor.execute('''
            REPLACE INTO ham_info VALUES
            (?, ?, ?)''', (1, callsign_nossid, txgroup)
        )
        conn.commit()
    conn.close()
    pass

if __name__ == "__main__":
    data = retrieve_usrinfo()
    callsign_nossid = data['callsign_nossid']
    txgroup = data['txgroup']

    config = configparser.ConfigParser()
    config.read("/etc/a2d/a2d_adv_conf.ini")
    preferred_ssids = config.get("SSID", "PreferredSSIDs", fallback="")
    ssids = preferred_ssids.split(",")

    condition1 = False
    condition2 = False

    data_dir = '/var/lib/a2d/dbs'
    previous_values_db = f'{data_dir}/previous_values.db'
    callssid_db = f'{data_dir}/callssid.db'
    ham_info_db = f'{data_dir}/ham_info.db'

    # Call the database update functions
    condition1, condition2 = update_previous_values_db(previous_values_db, callsign_nossid, txgroup, condition1, condition2)
    
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    
    result1 = pool.apply_async(update_callssid_db, (callssid_db, callsign_nossid, ssids, condition1))
    result2 = pool.apply_async(update_ham_info_db, (ham_info_db, callsign_nossid, txgroup, condition1, condition2))
    
    pool.close()
    pool.join()
