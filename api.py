import logging
from typing import Any, List, Optional

import duckdb
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import PlainTextResponse

from config import get_config
from duck import get_db_connection

router = APIRouter()


class SqlRequest(BaseModel):
    sql: str
    timeout: int = 0
    parameters: Optional[List[Any]] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sql": "select * from pond where total > ?",
                    "parameters": [0],
                },
            ]
        }
    }


@router.get("/quack", tags=["health"], response_class=PlainTextResponse)
def ping(config=Depends(get_config), db_connection=Depends(get_db_connection)):
    """
    Ping api

    - return ping response if successful
    """
    result = db_connection.execute("select sum(total) from pond").fetchall()
    num_ducks = result[0]
    return f"quack quack. serving you on port {config['serve']['port']}, num_ducks in pond: {num_ducks}"


@router.post("/sql/", tags=["run_sql"], response_class=JSONResponse)
def run_sql(sql_req: SqlRequest, db_connection=Depends(get_db_connection)):
    """
    run sql

    - **sql**: the sql string
    - **timeout**: timeout in seconds
    - **parameters**: list of named parameters
    - return json with 3 keys 'schema','columns','rows'. each is an []. schema/columns are [] of string. rows is an [] of row. row is an [] of column values
    """
    if sql_req is None:
        raise HTTPException(status_code=400, detail="bad input: got NULL input request!")

    if sql_req.sql is None or "" == sql_req.sql.strip():
        raise HTTPException(status_code=400, detail="bad input: input request does not have any sql" )
    try:
        # todo: make async
        rows = db_connection.execute(sql_req.sql, sql_req.parameters).fetchall()
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
