import sqlite3
import configparser
from crontab import CronTab

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
    # Get the current user's cron table
    cron = CronTab(user=True)

    # Find the cron job that matches the specified command
    command = '/usr/bin/python /usr/share/a2d/runscripts.py'
    for job in cron:
        if job.command == command:
            # Remove the cron job
            cron.remove(job)

    # Write the changes to the cron table
    cron.write()

#Ini read/write utils
def read_ini_data(ini_file):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(ini_file)
    return config

def write_ini_data(config, ini_file):
    with open(ini_file, 'w') as configfile:
        config.write(configfile)
