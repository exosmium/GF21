# 🕵️‍♂️ GF21 Livman Telegram Interface

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Unofficial Python API wrapper and Telegram bot for GF21 GPS trackers using the 365GPS platform. Reverse engineered from the web interface.

## 🎯 About GF21 Tracker

The GF21 is a compact (2.6×1.3×4.3cm) 2G GSM GPS tracker with:
- Built-in 350mAh battery
- Supports 850/900/1800/1900MHz bands
- WIFI+LBS+GPS positioning
- Operating temp: -20°C to 85°C 
- Real-time tracking via 365GPS platform
- Two-way voice calls
- Remote audio monitoring
- Vibration alerts

## ⚡ Features

- Async Python implementation for 365GPS API
- Clean Telegram bot interface with inline buttons
- Real-time location tracking and status monitoring
- Journey time estimation via Google Maps API
- Location visualization with static maps
- Battery and movement status tracking

## 🔧 Installation

```bash
git clone https://github.com/exosmium/GF21
cd GF21
pip install -r requirements.txt
```

Add your credentials to `config.txt`:
```ini
[GPS]
IMEI=your_device_imei
PASSWORD=device_password
```

## 📱 Usage 

```bash
python main.py
```

Then interact via Telegram bot commands:
- `/start` - Launch bot
- Use inline buttons for status/location updates

## 🔍 Technical Details

- Pure Python async/await implementation
- Session management for 365GPS platform
- Google Maps API integration for routing
- Telegram Bot API via Telethon

## 🤝 Contributing

Pull requests welcome! Areas for improvement:
- Support for other 365GPS devices
- Additional tracking features
- UI/UX enhancements
- Documentation improvements

## ⚠️ Disclaimer

For personal vehicle tracking only. Use responsibly and legally.

## 📝 License

MIT

---

Keywords: gps-tracker, 365gps, gf21-tracker, liveman-gf21, vehicle-tracking, telegram-bot, python-async, reverse-engineering, gps-monitoring, fleet-tracking, anti-theft, gsm-tracker
