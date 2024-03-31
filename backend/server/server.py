from flask import Flask

app = Flask(__name__)
htmx = HTMX(app)

@app.route("/")
def hello_world():
  return "hi"