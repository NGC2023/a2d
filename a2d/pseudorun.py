import os
import sys
from a2d.a2d_utils.pseudo_aprs_utils import process_aprs_data_parallel
from a2d.a2d_utils.a2d_utils import establish_connection, retrieve_data_from_table, create_table_if_not_exists

# Database directory
data_dir = f'/var/lib/a2d/dbs'

def main():
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the 'utils' directory to the Python module search path if not already present
    utils_dir = os.path.join(current_dir, 'utils')
    if utils_dir not in sys.path:
        sys.path.append(utils_dir)

    # Establish connection to the APRS messages database
    aprs_messages_db = f'{data_dir}/pseudo_aprs_messages.db'
    aprs_conn, aprs_cursor = establish_connection(aprs_messages_db)

    # Create the table if it doesn't exist
    create_table_if_not_exists(aprs_cursor, 'pseudo_aprs_messages', '(messageid TEXT PRIMARY KEY, srccall TEXT, message TEXT, trgcall TEXT)')

    # Retrieve data from the 'callssid' table
    callssid_db = f'{data_dir}/callssid.db'
    callssid_conn, callssid_cursor = establish_connection(callssid_db)
    rows = retrieve_data_from_table(callssid_cursor, 'callssid')
    callssid_conn.close()

    # Close the connection to the APRS messages database
    aprs_conn.close()

    # Process APRS messages using multiprocessing
    process_aprs_data_parallel(rows, 'pseudo_aprs_messages')

if __name__ == "__main__":
    main()

# Create a SQLite empty aprs database
aprs_messages_db = f'{data_dir}/aprs_messages.db'
aprs_conn, aprs_cursor = establish_connection(aprs_messages_db)

# Create a table to store the data
create_table_if_not_exists(aprs_cursor, 'aprs_messages', '(messageid TEXT PRIMARY KEY, srccall TEXT, message TEXT, trgcall TEXT)')

# Commit the changes and close the connection
aprs_conn.commit()
aprs_conn.close()
