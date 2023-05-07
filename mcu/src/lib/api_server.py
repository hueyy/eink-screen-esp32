# MicroDot does not support HTTPS and will throw a UnicodeError if
# accessed via HTTPS: https://github.com/miguelgrinberg/microdot/issues/62


async def start_api_server():
    import gc

    gc.collect()

    from microdot_asyncio import Microdot, Request

    app = Microdot()

    Request.max_content_length = 400 * 1024  # 400KB
    Request.max_body_length = 400 * 1024

    @app.route("/")
    def index(request):
        return {"status": "OK"}

    @app.post("/clear")
    def api_clear(request):
        from lib.display import Display

        d = Display()
        d.init_epd()
        d.clear()

        return {"status": "OK"}

    @app.route("/receive_data", methods=["POST", "OPTIONS"])
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

        parts = 100

        if block_number == 0:
            d.epd.init()  # manually init since we're not using init_buffer
            d.epd.send_black_buffer(buffer)
            return {"status": "OK", "last_block": 0}
        elif block_number == (parts - 1):
            d.epd.send_black_buffer(buffer)
            d.turn_on_display()
            return {"status": "OK", "last_block": (parts - 2)}
        else:
            d.epd.send_black_buffer(buffer)
            return {"status": "OK", "last_block": block_number - 1}

    @app.errorhandler(404)
    def not_found(request):
        return "Not found", 404

    @app.before_request
    def before_request(request):
        if request.method == "OPTIONS":
            res = Response(res)
            res.headers["Access-Control-Allow-Origin"] = "*"
            res.headers["Access-Control-Allow-Methods"] = "*"
            res.headers["Access-Control-Allow-Headers"] = "*"
            res.headers["Access-Control-Allow-Credentials"] = "true"
            res.headers["Access-Control-Max-Age"] = "86400"
            return res
        gc.collect()
        print("Memory free: ", gc.mem_free())

    print("Started HTTP server on port 80")
    app.run(port=80, debug=True)
