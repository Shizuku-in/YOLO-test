import cv2
import time
import requests
import threading
from flask import Flask, Response
from ultralytics import YOLO
from datetime import datetime

C_GREEN = "\033[92m"
C_RED   = "\033[91m"
C_RESET = "\033[0m"

app = Flask(__name__)

# 模型
model = YOLO("yolo11n.pt") 

# 接口
SERVER_URL = "http://localhost:1145/api/report_alarm"

# 摄像头
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# 冷却
last_time = 0
ALARM_COOLDOWN = 10 # 秒

# 类别映射
# 例 0: person; 1: bicycle
TARGET_CLASSES = [0, 1] 
NAME_MAPPING = {
    "person": "Person detected!",
    "bicycle": "Bicycle detected!"
}

def send_alarm_async(risk_type, conf, location="Location_01"):
    def _send():
        try:
            payload = {
                "camera_id": location,
                "risk_type": risk_type,
                "confidence": float(conf),
                "timestamp": datetime.now().isoformat()
            }
            requests.post(SERVER_URL, json=payload, timeout=1)
            print(f"{C_GREEN}[ALARMED]{C_RESET} {risk_type}")
        except Exception as e:
            print(f"{C_RESET}[ERROR]{C_RESET} {e}")
    
    threading.Thread(target=_send).start()

def generate_frames():
    global last_time
    
    while True:
        success, frame = camera.read()
        if not success:
            break

        # 推理
        results = model(frame, stream=True, classes=TARGET_CLASSES, conf=0.5, verbose=False)

        detected_risk = False
        max_conf = 0.0
        risk_name = ""

        for result in results:
            note_frame = result.plot() # 返回 numpy 数组图片
            
            if len(result.boxes) > 0:
                detected_risk = True
                max_conf = result.boxes.conf[0].item()
                cls_id = int(result.boxes.cls[0].item())
                risk_name = result.names[cls_id]

        
        final_frame = note_frame if 'note_frame' in locals() else frame # 若无目标则使用原图

        current_time = time.time()
        if detected_risk and (current_time - last_time > ALARM_COOLDOWN):
            display_name = NAME_MAPPING.get(risk_name, risk_name) # 映射名称
            send_alarm_async(display_name, max_conf)
            last_time = current_time

        # cv2.imshow("Debug", final_frame)
        # cv2.waitKey(1)

        ret, buffer = cv2.imencode('.jpg', final_frame)
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            print(f"{C_RED}[ERROR]{C_RESET} Skipped frame")
            pass



@app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') # 前端通过这个路由获取视频流

if __name__ == '__main__':
    print(f"{C_GREEN}[Streaming started]{C_RESET} http://localhost:1919/stream")
    app.run(host='0.0.0.0', port=1919, debug=False)