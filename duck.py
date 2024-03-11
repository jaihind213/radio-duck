import logging
from datetime import date, datetime

import duckdb

import config

default_schema = "main"
database_name = ""

# primary connection
connection = None


def setup_duck():
    duckdb_file = config.get_config()["duck"]["db_file"]
    logging.warning(f"using duckdb data file: {duckdb_file}.")
    duckdb_mem_str = config.get_config()["duck"]["memory"]
    if duckdb_file is None or "" == duckdb_file:
        raise ValueError("duckdb file path not set!")

    global connection
    connection = duckdb.connect(duckdb_file)
    logging.warning(f"setting memory for duckdb as {duckdb_mem_str}.")
    connection.sql("SET memory_limit='" + duckdb_mem_str + "';")

    curr_db_result = connection.execute("SELECT current_database()")
    global database_name
    database_name = curr_db_result.fetchone()[0]

    _prepare_pond_tables()
    _load_extensions(config.get_config()["duck"]["extensions"])


def get_db_connection() -> duckdb.DuckDBPyConnection:
    # If you want to create a 2nd connection to an existing database,
    # you can use the cursor() method.
    # todo pool of cursors
    cursor = None
    try:
        cursor = connection.cursor()
        # its used as a fastapi dependency,
        # so fastapi will call second time to enter finally block
        yield cursor
    finally:
        if not cursor:
            duckdb.close(cursor)


def _prepare_pond_tables():
    logging.info("initializing duck db...")
    connection.execute("""
        CREATE OR replace TABLE pond
        (
            date_time datetime,
            duck_type text,
            total integer,
            PRIMARY KEY (date_time, duck_type)
        );
        """)
    connection.execute("""
        CREATE OR replace TABLE ducks
        (
            duck_type text,
            avg_height float,
            avg_weight float,
            can_fly boolean,
            date_of_discovery date,
            PRIMARY KEY (duck_type)
        );
        """)
    connection.execute("""
            CREATE or replace TABLE example_table (event_timestamp TIMESTAMP WITH TIME ZONE, event_name VARCHAR(255))
        """)  # noqa: E501,B950

    duck_data = [
        ("Mallard", 12.5, 2.3, True, date(1800, 1, 1)),
        ("Pekin", 10.0, 3.0, False, date(1850, 2, 1)),
        ("Wood", 11.0, 2.5, True, date(1750, 3, 1)),
        ("Muscovy", 9.0, 4.0, False, date(1823, 4, 1)),
        ("Runner", 8.0, 1.5, True, date(1822, 5, 1)),
    ]

    # Sample data for pond
    pond_data = [
        (datetime(2022, 1, 1, 12, 0), "Mallard", 5),
        (datetime(2022, 2, 1, 12, 0), "Pekin", 8),
        (datetime(2022, 3, 1, 12, 0), "Wood", 12),
        (datetime(2022, 4, 1, 12, 0), "Muscovy", 6),
        (datetime(2022, 5, 1, 12, 0), "Runner", 9),
        (datetime(2022, 6, 1, 12, 0), "Mallard", 7),
        (datetime(2022, 7, 1, 12, 0), "Pekin", 10),
        (datetime(2022, 8, 1, 12, 0), "Wood", 14),
        (datetime(2022, 9, 1, 12, 0), "Muscovy", 8),
        (datetime(2022, 10, 1, 12, 0), "Runner", 11),
    ]

    data_to_insert = [
        ("2023-11-22 12:30:00+00:00", "Event 1"),
    ]
    # Insert data into 'ducks' table
    connection.executemany(
        "INSERT INTO ducks VALUES (?, ?, ?, ?, ?)", duck_data
    )

    # Insert data into 'pond' table
    connection.executemany("INSERT INTO pond VALUES (?, ?, ?)", pond_data)

    connection.executemany(
        "INSERT INTO example_table VALUES (?, ?)", data_to_insert
    )


def _load_extensions(xtensions_str: str):
    # configure extensions
    if xtensions_str is None or xtensions_str == "":
        logging.info("no extensions configured to preload.")
        return
    xtensions = xtensions_str.split(",")
    logging.info(f"loading extensions.. {xtensions_str}.")
    for x in xtensions:
        connection.execute("install {} ; load {} ;".format(x, x))
        logging.info(f"loaded extension {x}.")
