from flask import Flask, request, redirect, url_for
from flask_assets import Environment
from flask_htmx import HTMX
from werkzeug.middleware.proxy_fix import ProxyFix
from jinjax import Catalog

app = Flask(__name__, static_folder=None)

assets = Environment(app)
assets.init_app(app)

htmx = HTMX(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

NAV_ITEMS = [
    {"title": "Image", "path": "/image"},
    {"title": "Text", "path": "/text"},
    {"title": "Toot", "path": "/toot"},
]

catalog = Catalog(
    globals={
        "current_path": lambda: request.path,
        "nav_items": NAV_ITEMS,
    }
)
catalog.add_folder("server/screens")
catalog.add_folder("server/components")

CURRENT_FILE_PATH = "server/static/current"

DEFAULT_MODE: str = "image"


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for(DEFAULT_MODE))


@app.route("/text", methods=["GET"])
def text():
    return catalog.render("TextInputScreen")


@app.route("/image", methods=["GET"])
def image():
    return catalog.render("ImageInputScreen")


@app.route("/current", methods=["HEAD", "PUT"])
def put_current():
    if not "image_data" in request.form:
        return {"message": "image_data field missing"}, 400
    if len(request.form["image_data"]) > 0:
        with open(CURRENT_FILE_PATH, "wb") as file:
            # convert from str to bytes
            file.write(bytes(int(n) for n in request.form["image_data"].split(",")))
    else:
        with open(CURRENT_FILE_PATH, "w") as file:
            file.write("")
    return "OK"


if __name__ == "__main__":
    pass
