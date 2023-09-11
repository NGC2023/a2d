#coding=utf-8
#!/usr/bin/env python3

import multiprocessing
from multiprocessing import Manager
from a2d.a2d_utils.get_aprs import get_aprs
from a2d.a2d_utils.post_dapnet import dapnet
from a2d.a2d_utils.a2d_utils import establish_connection, retrieve_data_from_table, create_table_if_not_exists

#Database directory
data_dir = f'/var/lib/a2d/dbs'

# Establish connection to the SQLite databases
callssid_db = f'{data_dir}/callssid.db'
callssid_conn, callssid_cursor = establish_connection(callssid_db)
rows = retrieve_data_from_table(callssid_cursor, 'callssid')
callssid_conn.close()

def find_new_msg():
    # Connect to the pseudo_aprs_messages database
    pseudo_aprs_db = f'{data_dir}/pseudo_aprs_messages.db'
    connection, pseudo_cursor = establish_connection(pseudo_aprs_db)
    pseudo_aprs_rows = retrieve_data_from_table(pseudo_cursor, 'pseudo_aprs_messages')
    connection.close()
    pseudo_aprs_set = set(row[0] for row in pseudo_aprs_rows)  # Extract the messageid from each row

    return pseudo_aprs_set

def new_msg(srccall, trgcall, message):
    new_msg_str = srccall + '(' + trgcall + '):' + message
    dapnet(new_msg_str)

def process_row(row, aprs_messages_db, pseudo_aprs_set, lock):
    conn, cursor = establish_connection(aprs_messages_db)

    try:
        # Acquire the lock before accessing the database
        lock.acquire()

        result = get_aprs(row)
        if result is None:
            return

        entries, trgcall = result

        if not entries:
            return

        for item in entries:
            messageid = item['messageid']
            srccall = item['srccall']
            message = item['message']

            # Check if messageid already exists in the SQLite table
            cursor.execute("SELECT messageid FROM aprs_messages WHERE messageid = ?", (messageid,))
            result = cursor.fetchone()

            # If messageid doesn't exist, insert the data into the SQLite table
            if not result:
                cursor.execute("INSERT INTO aprs_messages (messageid, srccall, message, trgcall) VALUES (?, ?, ?, ?)",
                               (messageid, srccall, message, trgcall))

                # Check if the messageid also doesn't exist in the pseudo_aprs_messages
                if messageid not in pseudo_aprs_set:
                    # Pass the new message to new_msg() function
                    new_msg(srccall, trgcall, message)

        conn.commit()
    finally:
        # Release the lock after the database operations are done
        lock.release()

    cursor.close()
    conn.close()

def APRS_messages():
    # Create a SQLite database
    aprs_messages_db = f'{data_dir}/aprs_messages.db'
    conn, cursor = establish_connection(aprs_messages_db)
    create_table_if_not_exists(cursor, 'aprs_messages', '(messageid TEXT PRIMARY KEY, srccall TEXT, message TEXT, trgcall TEXT)')
    cursor.close()
    conn.close()

    # Get pseudo_aprs_set using your find_new_msg() function
    pseudo_aprs_set = find_new_msg()

    # Number of processes to create
    num_processes = multiprocessing.cpu_count()

    # Create a process pool
    pool = multiprocessing.Pool(processes=num_processes)

    # Create a shared lock using Manager
    manager = Manager()
    lock = manager.Lock()

    # Prepare arguments for the process_row function
    args = [(row, aprs_messages_db, pseudo_aprs_set, lock) for row in rows]

    # Map the process_row function to the arguments in the pool
    pool.starmap(process_row, args)

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

if __name__ == "__main__":
    APRS_messages()
