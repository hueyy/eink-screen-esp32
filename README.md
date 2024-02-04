# eink-screen-esp32

This is a monorepo containing some simple code for a tiny web app that controls my eink screen (with an ESP32 driver). I have since switched to using a Raspberry Pi to drive the eink screen so I am no longer maintaining this repository and therefore have archived it.

![photo of the screen](./assets/eink-screen.jpg)

## Software

There are 2 distinct codebases:

1. Web app (`/frontend`) - static site
2. MCU codebase (`/mcu`) - code that runs on the eink screen MCU

## Hardware

- [Waveshare 800×480, 7.5inch E-Ink raw display, red/white/black](https://www.waveshare.com/7.5inch-e-paper.htm)
- [Waveshare Universal e-Paper Raw Panel Driver Board, ESP32 WiFi / Bluetooth Wireless](https://www.waveshare.com/e-paper-esp32-driver-board.htm)
