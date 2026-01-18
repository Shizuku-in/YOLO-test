import { ref, onMounted } from 'vue';
import { ALARM_CONFIG_MAP } from './config.js';
import { useWebSocket, useVideoStream } from './hooks.js';
import { CONFIG } from './env.config.js';

export default {
    setup() {
        const alarms = ref([]);
        const isCloudConnected = ref(false);
        const isCameraConnected = ref(false);
        const videoSrc = ref(CONFIG.STREAM_URL);

        const { connectWebSocket } = useWebSocket(alarms, isCloudConnected);
        const { handleVideoLoad, handleVideoError } = useVideoStream(isCameraConnected);

        const getAlarmConfig = (type) => {
            return ALARM_CONFIG_MAP[type] || ALARM_CONFIG_MAP['?'];
        };

        onMounted(() => {
            connectWebSocket();
        });

        return { 
            alarms, 
            isCloudConnected, 
            isCameraConnected,
            videoSrc,
            handleVideoLoad,
            handleVideoError,
            getAlarmConfig 
        };
    }
};