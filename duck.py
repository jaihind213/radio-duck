import logging

import duckdb

import config

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

    import random
    n = random.randint(1, 213)
    logging.info("initializing duck db...")
    connection.execute(f"CREATE OR REPLACE TABLE pond(duck_type text, total INTEGER); insert into pond values ('mallard', {n});insert into pond values ('wood_duck', {n+1});")
    logging.info("inserted {} ducks into pond...".format(n+n+1))

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
