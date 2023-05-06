# MicroDot does not support HTTPS and will throw a UnicodeError
# if accessed via HTTPS

from microdot import Microdot

app = Microdot()


@app.route("/")
def index(request):
    return "Hello, world!"


app.run()
