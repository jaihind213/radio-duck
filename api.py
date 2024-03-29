import logging
from typing import Any, List, Optional

import duckdb
import fastapi
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field

import deser
from config import get_config
from duck import default_schema, get_db_connection

router = APIRouter()


class SqlRequest(BaseModel):
    sql: str
    timeout: int = 0
    parameters: Optional[List[Any]] = []
    schema_to_use: str = Field(alias="schema", default="")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sql": "select * from pond where total > ?",
                    "parameters": [0],
                    "schema": "main",
                },
            ]
        }
    }


@router.get("/quack", tags=["health"], response_class=PlainTextResponse)
def ping(
    config=fastapi.Depends(get_config),
    db_connection=fastapi.Depends(get_db_connection),
):
    """
    Ping api

    - return ping response if successful
    """
    result = db_connection.execute("select sum(total) from pond").fetchall()
    num_ducks = result[0]
    return (
        f"quack quack. serving you on port {config['serve']['port']},"
        f" num_ducks in pond: {num_ducks}"
    )


@router.post("/sql/", tags=["run_sql"], response_class=JSONResponse)
def run_sql(
    sql_req: SqlRequest, db_connection=fastapi.Depends(get_db_connection)
):
    """
    run sql

    - **sql**: the sql string
    - **timeout**: timeout in seconds
    - **parameters**: list of named parameters
    - **schema**: the database schema, defaults to 'main'
    - return json with 3 keys 'schema','columns','rows'. each is an [].
    schema/columns are [] of string.
    rows is an [] of row. row is an [] of column values
    """
    if sql_req is None:
        raise HTTPException(
            status_code=400, detail="bad input: got NULL input request!"
        )

    if sql_req.sql is None or "" == sql_req.sql.strip():
        raise HTTPException(
            status_code=400,
            detail="bad input: input request does not have any sql",
        )

    skema = default_schema
    if sql_req.schema_to_use is not None:
        schema_provided = sql_req.schema_to_use.strip()
        if "" != schema_provided:
            skema = schema_provided

    try:
        # todo: make async
        from duck import database_name

        db_connection.execute("use " + database_name + "." + skema)
        rows = db_connection.execute(
            sql_req.sql, sql_req.parameters
        ).fetchall()
        schema = [dtype[1] for dtype in db_connection.description]
        result = {
            "schema": schema,
            "columns": [name[0] for name in db_connection.description],
            "rows": list(_deserialize(schema, list(rows))),
        }
        return JSONResponse(content=result)
    except (
        duckdb.InvalidInputException,
        duckdb.BinderException,
        duckdb.CatalogException,
        duckdb.ParserException,
    ) as e:
        logging.error(e)
        raise HTTPException(
            status_code=400, detail="bad input:" + str(e)
        ) from e
    except duckdb.OutOfMemoryException as oom:
        logging.error(oom)
        raise HTTPException(
            status_code=500, detail="out of memory for query:" + str(oom)
        ) from oom


def _deserialize(schema, rows):
    return deser.jsonify_rows(tuple(schema), rows)
