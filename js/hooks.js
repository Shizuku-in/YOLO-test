import { ElNotification } from 'element-plus';

export function useWebSocket(alarms, isCloudConnected) {
    const connectWebSocket = () => {
        const ws = new WebSocket("ws://localhost:1145/ws"); // 模拟 WS 地址
        
        ws.onopen = () => { 
            console.log("WebSocket Connected");
            isCloudConnected.value = true;
        };
        
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                alarms.value.unshift(data);
                
                ElNotification({
                    title: '安全警报',
                    message: `${data.location} - ${data.type}`,
                    type: 'error',
                    position: 'bottom-right',
                });
            } catch (e) {
                console.error("数据解析错误", e);
            }
        };

        ws.onclose = () => { 
            console.log("WebSocket Disconnected");
            isCloudConnected.value = false;
            setTimeout(connectWebSocket, 3000); // 断线重连
        };

        ws.onerror = () => {
            isCloudConnected.value = false;
        };
    };

    return { connectWebSocket };
}

export function useVideoStream(isCameraConnected) {
    const handleVideoLoad = () => {
        isCameraConnected.value = true;
    };
    
    const handleVideoError = () => {
        isCameraConnected.value = false;
    };

    return { handleVideoLoad, handleVideoError };
}