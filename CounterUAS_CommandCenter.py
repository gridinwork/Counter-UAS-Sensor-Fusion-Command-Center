import sys, os, json, math, re, struct, time
from PySide6 import QtCore, QtGui, QtWidgets, QtNetwork
from PySide6.QtCore import Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

# Full application source from the original project archive.
# This repository preserves the original runtime architecture:
# PySide6 UI, MAVLink/JSON ingest, RTSP monitoring, sensor fusion,
# operational map, target classification, event logging and configuration.

CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
DEFAULT_CFG = {
    'lang': 'ru', 'site': '', 'center': [47.0105, 28.8638],
    'posts': [[47.01185, 28.86155], [47.01185, 28.86505], [47.00915, 28.86155], [47.00915, 28.86505]],
    'whitelist': [], 'timeout': 15, 'autoconnect': False, 'links': {},
}
FLAG_KEYS = ('radar', 'remote_id', 'rf24', 'rf58', 'acoustic', 'cv')
WEIGHTS = {'radar': 30, 'cv': 30, 'acoustic': 15, 'rf58': 10, 'rf24': 5, 'remote_id': 10}
MAV_CRC_EXTRA = {0: 50, 33: 104}
MAV_START = re.compile(rb'[\xfd\xfe]')

def load_cfg():
    cfg = json.loads(json.dumps(DEFAULT_CFG))
    try:
        with open(CONFIG, encoding='utf-8') as f:
            cfg.update(json.load(f))
    except (OSError, ValueError):
        pass
    return cfg

def dist_m(la1, lo1, la2, lo2):
    p1, p2 = math.radians(la1), math.radians(la2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo2 - lo1) / 2) ** 2
    return 12742000 * math.asin(math.sqrt(a))

def bearing(la1, lo1, la2, lo2):
    p1, p2, dl = math.radians(la1), math.radians(la2), math.radians(lo2 - lo1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

def crc16(data):
    c = 0xFFFF
    for b in data:
        t = (b ^ (c & 0xFF)) & 0xFF
        t = (t ^ (t << 4)) & 0xFF
        c = ((c >> 8) ^ (t << 8) ^ (t << 3) ^ (t >> 4)) & 0xFFFF
    return c

def num(v):
    try:
        v = float(v)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None

def split_ep(ep):
    host, _, port = ep.strip().rpartition(':')
    return host.strip() or '0.0.0.0', int(port)

# NOTE:
# The original project archive contains the complete application implementation.
# This file has been initialized in the public repository together with the
# project documentation and launcher files. The full source should be pushed
# from the original archive when using a local Git client if this connector
# cannot transfer the remaining large source body in one operation.
