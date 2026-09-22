# 🪟 Automated Curtain Controller

A Raspberry Pi 5 project that automatically opens and closes curtains on a weekly schedule. Built with a Python/Flask backend and a dark mode web app you can install on your iPhone home screen.

## Demo
<table>
  <tr>
    <td align="center"><b>Opening</b></td>
    <td align="center"><b>Closing</b></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/brennansletten/automated-curtain-controller/main/demoOpen.gif" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/brennansletten/automated-curtain-controller/main/demoClose.gif" width="300"/></td>
  </tr>
</table>

## Web App
<img src="https://raw.githubusercontent.com/brennansletten/automated-curtain-controller/main/webapp.jpeg" width="300"/>

## Hardware
<table>
  <tr>
    <td><img src="https://raw.githubusercontent.com/brennansletten/automated-curtain-controller/main/hardware1.jpeg" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/brennansletten/automated-curtain-controller/main/hardware2.jpeg" width="300"/></td>
  </tr>
</table>

## Features
- Set different open and close times for each day of the week
- Enable or disable individual days with a toggle
- Manual open and close buttons from your phone
- Emergency stop that kills the motor mid-movement
- Remembers curtain position after a reboot
- Starts automatically on boot — no SSH needed day to day

## Tech Stack
- Python / Flask
- Raspberry Pi 5 running headless Linux
- GPIO motor control via gpiozero
- GT2 belt and pulley drive system
- Multithreaded motor control
- JSON for persistent storage
- Progressive Web App

## Hardware
- Raspberry Pi 5
- 28BYJ-48 stepper motor + ULN2003 driver board
- GT2 timing belt and pulleys
- 3D printed motor mount and idler bracket

## Wiring

| ULN2003 Pin | Raspberry Pi Pin |
|---|---|
| IN1 | GPIO17 (Pin 11) |
| IN2 | GPIO18 (Pin 12) |
| IN3 | GPIO27 (Pin 13) |
| IN4 | GPIO22 (Pin 15) |
| VCC | 5V (Pin 2) |
| GND | GND (Pin 6) |

## Setup
1. Flash Raspberry Pi OS Lite (64-bit) using Raspberry Pi Imager
2. Enable SSH and set WiFi credentials in the imager settings
3. SSH in and create the project folder
4. Set up a Python virtual environment
5. Install dependencies
6. Set up the systemd service so it runs on boot
7. Open http://[pi-ip]:5000 on your phone

## Dependencies
```bash
pip install flask gpiozero lgpio
```

## Project Structure
```
curtainproject/
├── app.py              # Flask backend, motor control, scheduler
├── schedule.json       # Weekly schedule
├── state.json          # Saved curtain position
└── templates/
    └── index.html      # Web app frontend
```

## How It Works
Flask runs as a systemd service and hosts the web interface on port 5000. A background thread checks the time every 60 seconds and triggers the motor if it matches the schedule. The motor runs on its own thread so the web app stays responsive while it's moving. After every open or close the curtain position gets saved to a file so it survives reboots.

## Credits
3D printed parts based on the Curtains Opener by daliudzius
https://www.printables.com/model/462278-curtains-opener

Adapted for a different window size and swapped the ESP8266 for a Raspberry Pi 5.
