import os
import sqlite3

def reset_dbs():
    db_folder = '/var/lib/a2d/dbs'
    aprs_db_path = os.path.join(db_folder, 'aprs_messages.db')
    pseudo_aprs_db_path = os.path.join(db_folder, 'pseudo_aprs_messages.db')

    if os.path.exists(aprs_db_path) and os.path.exists(pseudo_aprs_db_path):
        clear_table(aprs_db_path, 'aprs_messages')
        clear_table(pseudo_aprs_db_path, 'pseudo_aprs_messages')
    elif os.path.exists(aprs_db_path):
        clear_table(aprs_db_path, 'aprs_messages')
    elif os.path.exists(pseudo_aprs_db_path):
        clear_table(pseudo_aprs_db_path, 'pseudo_aprs_messages')

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
