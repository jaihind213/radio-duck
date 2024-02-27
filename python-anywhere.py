import server

# entrypoint for pythonanywhere.com demo app
server.load_config(["default.ini"])
server.congfigure_logging()
server.setup_duck()
server.configure_router()

# uvicorn python-anywhere:demo --app-dir '.'
demo = server.app
