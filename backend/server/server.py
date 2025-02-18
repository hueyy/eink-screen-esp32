from flask import Flask, request, redirect, url_for
from flask_htmx import HTMX  # type: ignore
from werkzeug.middleware.proxy_fix import ProxyFix
from jinjax import Catalog
from flask_apscheduler import APScheduler  # type: ignore
import os
from typing import Final, get_args
from datetime import datetime
from server.render import render_dashboard, image_buffer_to_bytes, bytes_to_image_buffer
from server.eink import dither_image_data, convert_image_data_to_mono_red_hlsb  # type: ignore
from server.utils import write_current_canvas, write_current_canvas_image
from server.bus import get_bus_data
from server.nea import get_weather_forecast
from server.db import (
    db_get_mode,
    db_set_mode,
    db_get_dashboard_type,
    db_set_dashboard_type,
    DashboardType,
)
from server.rss import parse_news_feeds_urls
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder=None)

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB limit
app.config["MAX_FORM_MEMORY_SIZE"] = 8 * 1024 * 1024  # 8 MB limit

htmx = HTMX(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)  # type: ignore

# constants
NAV_ITEMS: Final[tuple[dict[str, str], ...]] = (
    {"title": "Image", "path": "/image"},
    {"title": "Text", "path": "/text"},
    {"title": "Dashboard", "path": "/dashboard"},
)

DEFAULT_MODE: str = "dashboard"

# jinjax
catalog = Catalog(
    globals={
        "current_path": lambda: request.path,
        "nav_items": NAV_ITEMS,
        "dashboard_types": get_args(DashboardType),
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
async def get_current_dashboard():
    dashboard_type = db_get_dashboard_type()
    if dashboard_type == "Home":
        now = datetime.now()
        time_dict = dict(
            current_date=now.strftime("%-d %B"),
            current_day_of_week=now.strftime("%a"),
            current_year=now.strftime("%Y"),
            current_time=now.strftime("%I:%M %p"),
        )
        bus_data = get_bus_data()
        weather_data = get_weather_forecast()
        return catalog.render(
            "HomeDashboardScreen",
            time_dict=time_dict,
            bus_data=bus_data,
            weather_data=weather_data,
        )
    else:
        now = datetime.now()
        time_dict = dict(
            current_date=now.strftime("%-d %B"),
            current_day_of_week=now.strftime("%a"),
            current_year=now.strftime("%Y"),
            current_time=now.strftime("%I:%M %p"),
        )
        news_items = await parse_news_feeds_urls()
        return catalog.render(
            "NewsDashboardScreen", time_dict=time_dict, news_items=news_items[0:6]
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


@app.route("/dashboard", methods=["POST"])
def refresh_dashboard() -> str:
    dashboard_type = request.form.get("dashboard_type")
    if dashboard_type and dashboard_type in get_args(DashboardType):
        db_set_dashboard_type(dashboard_type)  # type: ignore
    db_set_mode("dynamic")

    from threading import Thread, Event

    done = Event()

    def wrapped_re_render():
        try:
            re_render_dashboard()
        except Exception as e:
            logging.error(e)
        finally:
            done.set()

    thread = Thread(target=wrapped_re_render)
    thread.daemon = True
    thread.start()

    done.wait(timeout=10)

    return "OK"


# scheduled tasks
@scheduler.task("interval", id="check_for_updates", seconds=120)
def check_for_updates() -> str:
    mode = db_get_mode()
    print("Checking for updates: ", mode)
    if mode == "dynamic":
        re_render_dashboard()
    return "OK"


# Scheduler should initialise when running via gunicorn
scheduler.init_app(app)
scheduler.start()

if __name__ == "__main__":
    if os.environ.get("DEBUG") == "True":
        app.config["SCHEDULER_API_ENABLED"] = True
        app.run(debug=True, use_debugger=True, use_reloader=True)
    else:
        app.run()
