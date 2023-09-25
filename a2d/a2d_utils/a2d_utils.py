import sqlite3
import configparser

#db utils
def establish_connection(db_file):
    # Establish connection to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor

def retrieve_data_from_table(cursor, table_name):
    # Retrieve data from the specified table
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    return rows

def create_table_if_not_exists(cursor, table_name, columns):
    # Create a table if it doesn't exist in the database
    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} {columns}'
    cursor.execute(create_table_query)

def message_id_exists(cursor, table_name, message_id):
    # Check if the message ID exists in the specified table
    cursor.execute(f'SELECT messageid FROM {table_name} WHERE messageid = ?', (message_id,))
    result = cursor.fetchone()
    return bool(result)

#Cron util
def remove_cronjob():
    command = '/usr/bin/python3 -m a2d.runscripts'
    lines = []
    
    try:
        with open('/etc/cron.d/a2d', 'r') as cron_file:
            lines = cron_file.readlines()
    except FileNotFoundError:
        pass
    
    filtered_lines = [line for line in lines if not line.strip().endswith(command)]

    with open('/etc/cron.d/a2d', 'w') as cron_file:
        cron_file.writelines(filtered_lines)

#Ini read/write utils
def read_ini_data(ini_file):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(ini_file)
    return config

def write_ini_data(config, ini_file):
    with open(ini_file, 'w') as configfile:
        config.write(configfile)
