import logging

import duckdb

import config


default_schema = "main"
database_name = ""

#primary connection
connection = None

def setup_duck():
    duckdb_file = config.get_config()['duck']['db_file']
    logging.warning(f"using duckdb data file: {duckdb_file}.")
    duckdb_mem_str = config.get_config()['duck']['memory']
    if duckdb_file is None or "" == duckdb_file:
        raise ValueError("duckdb file path not set!")

    global connection
    connection = duckdb.connect(duckdb_file)
    logging.warning(f"setting memory for duckdb as {duckdb_mem_str}.")
    connection.sql("SET memory_limit='" + duckdb_mem_str + "';")

    curr_db_result = connection.execute("SELECT current_database()")
    global database_name
    database_name = curr_db_result.fetchone()[0]

    _prepare_pond_table()

def get_db_connection() -> duckdb.DuckDBPyConnection:
    #If you want to create a second connection to an existing database, you can use the cursor() method.
    #todo pool of cursors
    cursor = None
    try:
        cursor = connection.cursor()
        #its used as a fastapi dependency, so fastapi will call second time to enter finally block
        yield cursor
    finally:
        if not cursor:
            duckdb.close(cursor)


def _prepare_pond_table():
    import random
    n = random.randint(1, 213)
    logging.info("initializing duck db...")
    connection.execute("CREATE OR REPLACE TABLE pond(duck_type text, total INTEGER);")
    ducks = ["mallard", "wood_duck", "west_indian_whistling_duck", "marbled_duck", "mighty_duck"]
    for duck in ducks:
        connection.execute("INSERT INTO pond VALUES (?, ?)", [duck, n])
        n = n+1
    logging.info("inserted {} ducks into pond...".format(n+n+1))
