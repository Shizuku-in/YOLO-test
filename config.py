import os
from dotenv import load_dotenv

load_dotenv()

# Server Config
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "1145"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Detector Config
DETECTOR_HOST = os.getenv("DETECTOR_HOST", "0.0.0.0")
DETECTOR_PORT = int(os.getenv("DETECTOR_PORT", "1919"))
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
CAMERA_WIDTH = int(os.getenv("CAMERA_WIDTH", "640"))
CAMERA_HEIGHT = int(os.getenv("CAMERA_HEIGHT", "480"))

# YOLO Model
MODEL_PATH = os.getenv("MODEL_PATH", "yolo11n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
TARGET_CLASSES = [int(x) for x in os.getenv("TARGET_CLASSES", "0,1").split(",")]

# Alarm Config
ALARM_COOLDOWN = int(os.getenv("ALARM_COOLDOWN", "10"))

# API URL
SERVER_URL = f"http://localhost:{SERVER_PORT}/api/report_alarm"
STREAM_URL = f"http://localhost:{DETECTOR_PORT}/stream"
WEBSOCKET_URL = f"ws://localhost:{SERVER_PORT}/ws"
