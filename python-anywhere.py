import server

# entrypoint for pythonanywhere.com demo app
server.load_config(["/home/radioduck/radio-duck/pyanywhere.ini"])
server.congfigure_logging()
server.setup_duck()
server.configure_router()

# uvicorn python-anywhere:app --app-dir '.'
app = server.app
