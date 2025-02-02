from flask import Flask, request, redirect, url_for
from flask_htmx import HTMX  # type: ignore
from werkzeug.middleware.proxy_fix import ProxyFix
from jinjax import Catalog
from flask_apscheduler import APScheduler  # type: ignore
import os
from typing import Final
from datetime import datetime
from server.render import render_dashboard, image_buffer_to_bytes, bytes_to_image_buffer
from server.eink import dither_image_data, convert_image_data_to_mono_red_hlsb  # type: ignore
from server.utils import write_current_canvas, write_current_canvas_image
from server.bus import get_bus_data
from server.nea import get_weather_forecast
from server.db import db_get_mode, db_set_mode

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

DEFAULT_MODE: str = "dashboard"

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


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for(DEFAULT_MODE))


@app.route("/text", methods=["GET"])
def text():
    db_set_mode("static")
    return catalog.render("TextInputScreen")


@app.route("/image", methods=["GET"])
def image():
    db_set_mode("static")
    return catalog.render("ImageInputScreen")


@app.route("/current", methods=["HEAD", "PUT"])
def put_current():
    db_set_mode("static")

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
    db_set_mode("static")
    write_current_canvas("")
    write_current_canvas_image(bytes())
    return "OK"


@app.route("/current_dashboard", methods=["GET"])
def get_current_dashboard():
    now = datetime.now()
    time_dict = dict(
        current_date=now.strftime("%u %B"),
        current_day_of_week=now.strftime("%a"),
        current_year=now.strftime("%Y"),
        current_time=now.strftime("%I:%M %p"),
    )
    bus_data = get_bus_data()
    weather_data = get_weather_forecast()
    return catalog.render(
        "DashboardScreen",
        time_dict=time_dict,
        bus_data=bus_data,
        weather_data=weather_data,
    )


def re_render_dashboard() -> None:
    rendered_dashboard: bytes = render_dashboard()
    dithered_dashboard = dither_image_data(image_buffer_to_bytes(rendered_dashboard))

    write_current_canvas_image(bytes_to_image_buffer(dithered_dashboard))

    write_current_canvas(convert_image_data_to_mono_red_hlsb(dithered_dashboard))


@app.route("/dashboard", methods=["GET"])
def dashboard() -> str:
    db_set_mode("dynamic")
    return catalog.render("DashboardModeScreen")


# scheduled tasks
@scheduler.task("interval", id="check_for_updates", seconds=120)
def check_for_updates() -> str:
    mode = db_get_mode()
    print("Checking for updates: ", mode)
    if mode == "dynamic":
        re_render_dashboard()
    return "OK"


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()

    if os.environ.get("DEBUG") == "True":
        app.config["SCHEDULER_API_ENABLED"] = True
        app.run(debug=True, use_debugger=True, use_reloader=True)
    else:
        app.run()
