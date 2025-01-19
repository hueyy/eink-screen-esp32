from flask import Flask, request
from flask_assets import Environment
from flask_htmx import HTMX
from werkzeug.middleware.proxy_fix import ProxyFix
from jinjax import Catalog

app = Flask(__name__)

assets = Environment(app)
assets.init_app(app)

htmx = HTMX(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

catalog = Catalog()
catalog.add_folder("server/screens")
catalog.add_folder("server/components")


@app.route("/", methods=["GET"])
def home():
    return catalog.render("HomeScreen")


@app.route("/text")
def text():
    return catalog.render("TextInputScreen")


@app.route("/current")
def current():
    return


if __name__ == "__main__":
    pass
