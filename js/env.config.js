export const CONFIG = {
    STREAM_URL: window.ENV?.STREAM_URL || 'http://localhost:1919/stream',
    
    WEBSOCKET_URL: window.ENV?.WEBSOCKET_URL || 'ws://localhost:1145/ws',
    
    WS_RECONNECT_DELAY: 3000,
    
    CAMERA_ID: 'CAM_01',
};
