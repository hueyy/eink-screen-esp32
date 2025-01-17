from flask import Flask, stream_template
from flask_assets import Environment
from flask_htmx import HTMX

app = Flask(__name__)
assets = Environment(app)
htmx = HTMX(app)


@app.route("/")
def home():
    return stream_template("index.jinja")


@app.route("/text")
def text():
    return stream_template("text_input.jinja")


if __name__ == "__main__":
    assets.init_app(app)
