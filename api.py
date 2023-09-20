import json
import logging

import duckdb
import numpy as np
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from config import get_config
from duck import get_db_connection

router = APIRouter()

class SqlRequest(BaseModel):
    sql: str
    timeout: int = None

@router.get("/quack")
def hi(config=Depends(get_config), db_connection = Depends(get_db_connection)):
    """
    ping api
    :param config:
    :param db_connection:
    :return: message from server if ping successfull
    """
    result = db_connection.execute("select sum(total) from pond").fetchall()
    num_ducks = result[0]
    return f"quack quack. serving you on port {config['serve']['port']}, num_ducks in pond: {num_ducks}"


@router.post("/sql/")
#def run_sql(sql: str, db_connection = Depends(get_db_connection)):
def run_sql(sql_req: SqlRequest, db_connection = Depends(get_db_connection)):
    """
    run sql
    :param sql_req: sql request to run
    :param db_connection:
    :return: json with 3 fields 'schema','columns','rows'. each is an []. schema/columns are [] of string. rows is an [] of row. row is an [] of column values
    """
    #todo: make async
    try:
        rows = db_connection.execute(sql_req.sql).fetchall()
        result = {
            "schema": [dtype[1] for dtype in db_connection.description],
            "columns": [name[0] for name in db_connection.description],
            "rows": list(rows)
        }
        return JSONResponse(content=result)
    except (duckdb.InvalidInputException, duckdb.BinderException, duckdb.CatalogException, duckdb.ParserException) as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="bad input:" + str(e))
    except duckdb.OutOfMemoryException as oom:
        logging.error(oom)
        raise HTTPException(status_code=500, detail="out of memory for query:" + str(oom))
    except:
        raise
