# Counter-UAS Sensor Fusion Command Center

A Windows desktop command center for real-time UAV detection, tracking, classification, and multi-sensor fusion.

The application combines data from radar, Remote ID, RF monitoring, acoustic sensors, computer vision, RTSP cameras, and MAVLink/JSON telemetry into a unified operational picture.

## Features

- Multi-sensor UAV track fusion
- Radar target ingest via MAVLink 2 over UART or UDP
- JSON telemetry ingest over UART, UDP, or TCP
- Remote ID correlation and whitelist support
- 2.4 GHz and 5.8 GHz RF detection flags
- Acoustic and computer-vision confirmations
- RTSP RGB camera monitoring
- Pan/Tilt tracker connectivity status
- OpenStreetMap/Leaflet operational map
- Target table with coordinates, altitude, speed, heading, range, and confidence
- Event log and connection diagnostics
- Russian / English interface
- External response-station track reports over UDP
- Persistent settings in `config.json`

## Sensor Fusion

Messages sharing the same target ID are merged into a single track. If no confidence value is supplied, the application calculates confidence from available confirmations:

- Radar: 30
- Computer vision: 30
- Acoustic: 15
- 5.8 GHz RF: 10
- Remote ID: 10
- 2.4 GHz RF: 5

Speed and heading can also be estimated from target displacement when they are not provided by the source.

## Input JSON Format

One JSON object per line for serial/TCP, or one object/datagram for UDP. Arrays are also accepted.

```json
{
  "id": "T1",
  "lat": 47.01,
  "lon": 28.86,
  "alt": 120,
  "speed": 18,
  "heading": 45,
  "radar": true,
  "remote_id": "ABC123",
  "rf24": true,
  "rf58": true,
  "acoustic": true,
  "cv": true,
  "class": "UAV",
  "confidence": 85
}
```

Only `id` is mandatory.

## Requirements

- Windows 10/11
- Python 3
- PySide6
- Internet connection for OpenStreetMap tiles

## Installation

Run once:

```bat
install.bat
```

Then start the application with:

```bat
start.bat
```

Or install manually:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python CounterUAS_CommandCenter.py
```

## Screenshots

The `screenshots/` directory contains views of the map, camera page, connection settings, target table, event log, and external response-station interface.

## Notes

- Targets are shown only when received from connected real or test data sources.
- Configuration is stored in `config.json` next to the application.
- RTSP availability depends on the configured camera stream and local network.

## Disclaimer

This repository is intended for lawful research, monitoring, integration, and situational-awareness applications. Users are responsible for compliance with applicable laws and regulations.
