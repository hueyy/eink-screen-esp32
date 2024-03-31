from flask import Flask, render_template
from flask_assets import Environment
from flask_htmx import HTMX

app = Flask(__name__)
assets = Environment(app)
htmx = HTMX(app)

@app.route("/")
def hello_world():
  return render_template("index.html")

if __name__ == "__main__":
  assets.init_app(app)