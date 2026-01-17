# YOLO TEST DEMO

## Requirements

```bash
pip install opencv-python flask ultralytics requests fastapi uvicorn websockets
```

## Quickstart

```bash
python server.py
```

```bash
python detector.py
```

```bash
python -m http.server 8000
```

## Config

### Change detect-class

- `detector.py`: `TARGET_CLASSES` and `NAME_MAPPING`

### Change alarm-style

- `js/config.js`
- `css/style.css`: `.alarm-item.type-a`...
