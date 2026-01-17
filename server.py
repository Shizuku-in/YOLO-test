import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json

C_GREEN = "\033[92m"
C_RED   = "\033[91m"
C_RESET = "\033[0m"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlarmData(BaseModel):
    camera_id: str
    risk_type: str
    confidence: float
    timestamp: str

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/report_alarm")
async def report_alarm(data: AlarmData):
    print(f"{C_RED}[ALARMED]{C_RESET} {data.risk_type} - {data.timestamp}")
    
    message = json.dumps({
        "time": datetime.now().strftime("%H:%M:%S"),
        "location": f"{data.camera_id}",
        "type": data.risk_type,
        "desc": f"{data.confidence:.2f}"
    })
    
    await manager.broadcast(message)
    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1145)