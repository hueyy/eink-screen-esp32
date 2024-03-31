# eink-screen-esp32

This is a monorepo containing some simple code for a tiny web app that controls my eink screen (with an ESP32 driver).

![photo of the screen](./assets/eink-screen.jpg)

## Software

There are 3 distinct codebases:

1. Web app (`/frontend`) - static site that is served by the backend
2. Backend (`/backend`) - backend server running on a Raspberry Pi Zero
2. MCU codebase (`/mcu`) - code that runs on the eink screen MCU

The general set-up is as follows:

- The Raspberry Pi hosts a local WiFi network which the ESP32 connects to
- The backend runs on the Raspberry Pi and serves up the frontend
- Whenever an instruction is given via the frontend, the backend receives it and forwards it to the ESP32

## Hardware

- [Waveshare 800×480, 7.5inch E-Ink raw display, red/white/black](https://www.waveshare.com/7.5inch-e-paper.htm)
- [Waveshare Universal e-Paper Raw Panel Driver Board, ESP32 WiFi / Bluetooth Wireless](https://www.waveshare.com/e-paper-esp32-driver-board.htm)
- Raspberry Pi Zero 2