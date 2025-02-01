from flask import Flask, request, redirect, url_for
from flask_htmx import HTMX  # type: ignore
from werkzeug.middleware.proxy_fix import ProxyFix
from jinjax import Catalog
from flask_apscheduler import APScheduler  # type: ignore
import os
from typing import Final, Literal
from datetime import datetime
from server.render import render_dashboard_as_rgb, image_buffer_to_bytes  # type: ignore
from server.eink import dither_image_data, convert_image_data_to_mono_red_hlsb  # type: ignore

app = Flask(__name__, static_folder=None)

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB limit
app.config["MAX_FORM_MEMORY_SIZE"] = 8 * 1024 * 1024  # 8 MB limit

htmx = HTMX(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)  # type: ignore

# constants
NAV_ITEMS: Final[list[dict[str, str]]] = [
    {"title": "Image", "path": "/image"},
    {"title": "Text", "path": "/text"},
    {"title": "Dashboard", "path": "/dashboard"},
    # {"title": "Headlines", "path": "/headlines"},
]

HEADLINE_OPTIONS: Final[list[tuple[str, str]]] = [
    ("news.ycombinator.com", "https://news.ycombinator.com/rss"),
    ("bbc.com", "https://feeds.bbci.co.uk/news/rss.xml"),
]

CURRENT_FILE_PATH = "server/static/current"
CURRENT_FILE_IMAGE_PATH = "server/static/current.png"

DEFAULT_MODE: str = "image"

# jinjax
catalog = Catalog(
    globals={
        "current_path": lambda: request.path,
        "nav_items": NAV_ITEMS,
    }
)
catalog.add_folder("server/screens")
catalog.add_folder("server/components")

# scheduler
scheduler = APScheduler()

mode: Literal["input", "dashboard"] = "input"


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for(DEFAULT_MODE))


@app.route("/text", methods=["GET"])
def text():
    mode = "input"
    return catalog.render("TextInputScreen")


@app.route("/image", methods=["GET"])
def image():
    mode = "input"
    return catalog.render("ImageInputScreen")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    mode = "dashboard"
    rendered_dashboard: bytes = render_dashboard_as_rgb()
    write_current_canvas(
        convert_image_data_to_mono_red_hlsb(dither_image_data(rendered_dashboard))
    )
    return catalog.render("DashboardModeScreen")


def write_to_file(file_path: str, value: bytes | str):
    open_mode = "w" if type(value) is str else "wb"
    with open(file_path, open_mode) as file:
        file.write(value)


def write_current_canvas(value: bytes | str):
    return write_to_file(CURRENT_FILE_PATH, value)


def write_current_canvas_image(value: bytes):
    return write_to_file(CURRENT_FILE_IMAGE_PATH, value)


@app.route("/current", methods=["HEAD", "PUT"])
def put_current():
    if not "image_data" in request.files:
        return {"message": "image_data field missing"}, 400

    image_data = request.files["image_data"].read()

    write_current_canvas_image(image_data)
    mono_red_hlsb = convert_image_data_to_mono_red_hlsb(
        image_buffer_to_bytes(image_data)
    )
    write_current_canvas(mono_red_hlsb)

    return "OK"


@app.route("/clear", methods=["HEAD", "POST"])
def clear_current():
    write_current_canvas("")
    write_current_canvas_image(bytes())
    return "OK"


@app.route("/current_dashboard", methods=["GET"])
def get_current_dashboard():
    now = datetime.now()
    current_date = now.strftime("%I:%M %p")
    current_time = now.strftime("%A, %B %d, %Y")
    return catalog.render(
        "DashboardScreen", current_date=current_date, current_time=current_time
    )


# scheduled tasks
# @scheduler.task("interval", id="check_for_updates", seconds=5)
# def check_for_updates():
#     print("Checking for updates: ", mode)
#     if mode == "dashboard" or True:
#         rendered_dashboard: bytes = render_dashboard_as_rgb()
#         write_current_canvas(
#             convert_image_data_to_mono_red_hlsb(dither_image_data(rendered_dashboard))
#         )
#     return "OK"


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()

    if os.environ.get("DEBUG") == "True":
        app.config["SCHEDULER_API_ENABLED"] = True
        app.run(debug=True, use_debugger=True, use_reloader=True)
    else:
        app.run()
