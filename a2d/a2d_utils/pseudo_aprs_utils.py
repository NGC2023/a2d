from a2d.a2d_utils.a2d_utils import message_id_exists, establish_connection
from a2d.a2d_utils.get_aprs import get_aprs
import multiprocessing

def process_aprs_data(rows, table_name):
    # SQLite database
    aprs_messages_db = f'/var/lib/a2d/dbs/{table_name}.db'
    conn, cursor = establish_connection(aprs_messages_db)

    data_to_insert = []

    for c in rows:
        result = get_aprs(c)
        if result is None:
            continue

        entries, trgcall = result

        if not entries:
            continue

        for item in entries:
            messageid = item['messageid']
            srccall = item['srccall']
            message = item['message']

            # Check if messageid already exists in the SQLite table
            if not message_id_exists(cursor, table_name, messageid):
                data_to_insert.append((messageid, srccall, message, trgcall))

    # Close the connection to the database before creating the table
    conn.close()

    # Re-establish connection to the database to create the table and insert data
    conn, cursor = establish_connection(aprs_messages_db)

    # Batch insert the data into the SQLite table
    cursor.executemany(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?)', data_to_insert)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def process_aprs_data_parallel(rows, table_name):
    num_processes = max(1, min(multiprocessing.cpu_count(), len(rows)))
    chunk_size = max(1, len(rows) // num_processes)
    chunks = [rows[i:i + chunk_size] for i in range(0, len(rows), chunk_size)]

    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=process_aprs_data, args=(chunk, table_name))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
