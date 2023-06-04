# MicroDot does not support HTTPS and will throw a UnicodeError if
# accessed via HTTPS: https://github.com/miguelgrinberg/microdot/issues/62


def start_api_server():
    from microdot import Microdot, Request

    app = Microdot()

    Request.max_content_length = 2000 * 1024  # 2MB
    Request.max_body_length = 7 * 1024  # 7KB

    CORS_HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "86400",
    }

    CHUNK_SIZE = 1000  # 1KiB

    @app.route("/")
    def index(request):
        return {"status": "OK"}

    @app.route("/clear/", methods=["POST", "OPTIONS"])
    def api_clear(request):
        from lib.display import Display

        d = Display()
        d.init_epd()
        d.clear()

        return {"status": "OK"}

    @app.route("/receive_data/", methods=["POST", "OPTIONS"])
    def api_receive_data(request):
        if not request.stream:
            return {"error": "body missing"}, 400

        content_length = int(request.headers["Content-Length"])
        if not (content_length > 0):
            return {"error": "body empty"}, 400

        half_content_length = content_length // 2

        from lib.display import Display

        d = Display()

        d.init_epd()
        d.epd.begin_black_data_transmission()

        while content_length > 0:
            chunk = request.stream.read(min(content_length, CHUNK_SIZE))

            # end of black data and start of red data
            if content_length == half_content_length:
                d.epd.send_data(0x92)
                d.epd.begin_red_data_transmission()

            content_length -= len(chunk)
            d.epd.send_data(chunk)

        d.epd.turn_on_display()
        return {"status": "OK"}, CORS_HEADERS

    @app.route("/wifi/", methods=["GET", "OPTIONS"])
    def api_get_wifi_networks(request):
        from lib.wifi import get_wifi_status, get_wifi_networks

        status = get_wifi_status()
        networks = get_wifi_networks()
        return {
            "status": status,
            "networks": networks,
        }, CORS_HEADERS

    @app.route("/wifi/", methods=["POST"])
    def api_wifi(request):
        if not request.json or not request.json["ssid"] or not request.json["password"]:
            return {"error": "WiFi credentials not provided"}, 400
        return {"status": "OK"}, CORS_HEADERS

    @app.errorhandler(404)
    def not_found(request):
        return "Not found", 404

    @app.before_request
    def before_request(request):
        if request.method == "OPTIONS":
            res = Response(res)
            res.headers = res.headers | CORS_HEADERS
            return res

        import gc

        gc.collect()
        print("Memory free: ", gc.mem_free())

    print("Started HTTP server on port 80")
    app.run(port=80, debug=True)
