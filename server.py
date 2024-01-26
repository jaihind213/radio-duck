import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

import api
import config
import duck


# todo
@asynccontextmanager
async def shutdown_hook(app: FastAPI):
    yield
    duck.connection.close()
    print("shutdown hook called")


app = FastAPI(lifespan=shutdown_hook)

if __name__ == "__main__":
    arguments = sys.argv[0:]
    config_file = "/fubar.ini"
    if len(arguments) > 1:
        config_file = arguments[1]

    # config load
    default_config = os.getcwd() + "/default.ini"
    print("loading default config from", default_config)
    config.setup_app_config(default_config)
    if os.path.exists(config_file):
        print("loading user provided config from", config_file)
        config.setup_app_config(config_file)

    host = config.get_config()["serve"]["host"]
    port_str = config.get_config()["serve"]["port"]
    log_level = config.get_config()["logging"]["level"]
    # set default loglevel
    logging.basicConfig(level=logging._nameToLevel[log_level.upper()])

    # setup db
    duck.setup_duck()

    # configure secrets
    config.configure_sekrets(duck.connection)
    # start server
    import uvicorn

    app.include_router(
        api.router,
        prefix="/v1",
        dependencies=[
            Depends(config.get_config),
            Depends(duck.get_db_connection),
        ],
    )
    uvicorn.run(app, host=host, port=int(port_str), log_level=log_level)
