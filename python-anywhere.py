from starlette.responses import PlainTextResponse

import server
from api import router

# entrypoint for pythonanywhere.com demo app
server.load_config(["/home/radioduck/radio-duck/pyanywhere.ini"])


@router.get(
    "/welcome_notice_disclaimer",
    tags=["welcome_notice"],
    response_class=PlainTextResponse,
)
def disclaimer():
    """
    You have arrived at the demo for radio-duck ( https://github.com/jaihind213/radio-duck ) .
    This api returns disclaimer for https://www.pythonanywhere.com/ demo website, kindly request to read it by trying out the api. # noqa: E501,B950
    """
    return "Disclaimer: if you are accessing radio-duck hosted on https://radioduck.pythonanywhere.com/ ,please not it is intended for demonstration purposes only. Do not store any sensitive information, passwords, or secrets on this server. The owner of this server is not liable for any data, including secrets, stored on the server that may be leaked. Use this service responsibly & at your own risk."  # noqa: E501,B950


server.congfigure_logging()
server.setup_duck()
server.configure_router()

# uvicorn python-anywhere:app --app-dir '.'
app = server.app
