import os
from flask import Flask, stream_template
from flask_assets import Environment
from flask_htmx import HTMX
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# app.config.from_prefixed_env()

assets = Environment(app)
assets.init_app(app)

htmx = HTMX(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


@app.route("/")
def home():
    return stream_template("index.jinja")


@app.route("/text")
def text():
    return stream_template("text_input.jinja")


if __name__ == "__main__":
    pass
