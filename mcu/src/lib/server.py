# MicroDot does not support HTTPS and will throw a UnicodeError if
# accessed via HTTPS: https://github.com/miguelgrinberg/microdot/issues/62


async def start_server():
    import gc

    gc.collect()

    from microdot_asyncio import Microdot, send_file

    app = Microdot()

    api_app = Microdot()

    @api_app.route("/")
    def api_index(request):
        return "Hello world!"

    @api_app.route("/test")
    def api_test(request):
        from lib.display import Display

        d = Display()
        d.init_buffer()
        d.clear(1)

        return "OK"

    @api_app.post("/receive_data")
    def api_receive_data(request):
        if "block_number" not in query_string:
            return {"error": "block_number missing"}, 400
        if "body" not in request:
            return {"error": "body missing"}, 400

        block_number = int(query_string["block_number"])
        buffer = request.body
        print(buffer)
        print(type(buffer))

        from lib.display import Display

        d = Display()

        if block_number == 0:
            d.epd.init()  # manually init since we're not using init_buffer
            d.epd.send_black_buffer(buffer)
            return {"status": "OK", "last_block": 0}
        elif block_number == 3:
            d.epd.send_black_buffer(buffer)
            d.turn_on_display()
            return {"status": "OK", "last_block": 2}
        else:
            d.epd.send_black_buffer(buffer)
            return {"status": "OK", "last_block": block_number - 1}

    app.mount(api_app, url_prefix="/api")

    @app.route("/")
    def index(request):
        return send_file("../frontend/index.html")

    @app.route("/<re:[(?!^api)(^.*$)]:path>")
    def static_assets(request, path):
        if ".." in path:
            # directory traversal is not allowed
            return "Not found", 404
        return send_file("../frontend/" + path)

    @app.errorhandler(404)
    def not_found(request):
        return send_file("../frontend/index.html", status_code=200)

    print("Started HTTP server on port 80")
    app.run(port=80)
