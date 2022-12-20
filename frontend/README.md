# eink-screen frontend

Simple web app to allow me to send images over to the eink screen via Bluetooth.

## Development

Firefox does not support and [is not planning to support Web Bluetooth](https://mozilla.github.io/standards-positions/#web-bluetooth). This web app therefore only supports Chromium / Google Chrome.

The API can only be called upon a user interaction event (e.g. a button click) and in a HTTPS context.

When running the web app on Linux, you must enable the `chrome://flags/#enable-experimental-web-platform-features` flag.

See [Web Bluetooth Implementation Status](https://github.com/WebBluetoothCG/web-bluetooth/blob/main/implementation-status.md)