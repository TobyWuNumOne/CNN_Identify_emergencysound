<template>
  <div class="audio-recorder">
    <div class="recorder-header">
      <h2>🎤 即時錄音識別</h2>
      <p>點擊開始錄音，系統將即時分析環境聲音並識別緊急警報</p>
    </div>

    <!-- 錄音控制 -->
    <div class="recorder-controls">
      <button 
        @click="toggleRecording" 
        :class="['btn', recordingClass]"
        :disabled="!isSupported || isInitializing"
      >
        <span v-if="isInitializing">初始化中...</span>
        <span v-else-if="isRecording">🛑 停止錄音</span>
        <span v-else>🎤 開始錄音</span>
      </button>
      
      <div v-if="!isSupported" class="error-message">
        ❌ 您的瀏覽器不支援音頻錄製功能
      </div>
    </div>

    <!-- 連線狀態 -->
    <div class="connection-status">
      <div class="status-item">
        <span class="status-label">WebSocket:</span>
        <span :class="['status-value', wsConnected ? 'status-online' : 'status-offline']">
          {{ wsConnected ? '已連線' : '未連線' }}
        </span>
      </div>
      <div class="status-item">
        <span class="status-label">音頻:</span>
        <span :class="['status-value', audioInitialized ? 'status-online' : 'status-offline']">
          {{ audioInitialized ? '就緒' : '未就緒' }}
        </span>
      </div>
    </div>

    <!-- 波形顯示 -->
    <div class="waveform-section">
      <h3>音頻波形</h3>
      <div class="waveform-container">
        <canvas 
          ref="waveformCanvas" 
          class="waveform-canvas"
          width="800" 
          height="200"
        ></canvas>
      </div>
    </div>

    <!-- 預測結果 -->
    <div class="prediction-section">
      <h3>識別結果</h3>
      
      <!-- 警報狀態 -->
      <div v-if="currentAlert" :class="['alert', currentAlert.is_emergency ? 'alert-emergency' : 'alert-safe']">
        <div v-if="currentAlert.is_emergency" class="emergency-alert">
          🚨 檢測到緊急聲音: {{ currentAlert.type }}
          <div class="confidence">信心度: {{ (currentAlert.confidence * 100).toFixed(1) }}%</div>
        </div>
        <div v-else class="safe-alert">
          ✅ 環境聲音正常
          <div class="confidence">信心度: {{ (currentAlert.confidence * 100).toFixed(1) }}%</div>
        </div>
      </div>

      <!-- 詳細預測結果 -->
      <div v-if="currentPrediction" class="prediction-details">
        <h4>詳細分析</h4>
        <div class="prediction-bars">
          <div 
            v-for="(value, index) in currentPrediction" 
            :key="index"
            class="prediction-bar"
          >
            <div class="bar-label">{{ labels[index] }}</div>
            <div class="bar-container">
              <div 
                class="bar-fill" 
                :style="{ width: (value * 100) + '%' }"
                :class="getBarClass(labels[index], value)"
              ></div>
            </div>
            <div class="bar-value">{{ (value * 100).toFixed(1) }}%</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 錯誤訊息 -->
    <div v-if="errorMessage" class="error-section">
      <div class="alert alert-error">
        ❌ {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { AudioRecorder, AudioVisualizer } from '../services/audioService'
import { WebSocketService } from '../services/websocketService'

export default {
  name: 'AudioRecorder',
  setup() {
    // 響應式數據
    const isRecording = ref(false)
    const isInitializing = ref(false)
    const isSupported = ref(false)
    const audioInitialized = ref(false)
    const wsConnected = ref(false)
    const currentAlert = ref(null)
    const currentPrediction = ref(null)
    const errorMessage = ref('')
    const waveformCanvas = ref(null)
    
    // 服務實例
    let audioRecorder = null
    let audioVisualizer = null
    let wsService = null
    let sequenceNumber = 0

    // 標籤
    const labels = ['ambulance', 'environment', 'police']

    // 計算屬性
    const recordingClass = computed(() => ({
      'btn-record': !isRecording.value,
      'btn-stop': isRecording.value,
      'recording': isRecording.value
    }))

    // 初始化
    const initialize = async () => {
      try {
        isInitializing.value = true
        errorMessage.value = ''

        // 檢查瀏覽器支援
        isSupported.value = AudioRecorder.isSupported()
        if (!isSupported.value) {
          throw new Error('瀏覽器不支援音頻錄製功能')
        }

        // 初始化音頻錄製器
        audioRecorder = new AudioRecorder()
        await audioRecorder.initialize()
        audioInitialized.value = true

        // 初始化音頻視覺化
        if (waveformCanvas.value) {
          audioVisualizer = new AudioVisualizer(waveformCanvas.value)
        }

        // 初始化 WebSocket
        wsService = new WebSocketService()
        wsService.setEventCallbacks({
          onConnect: () => {
            wsConnected.value = true
            console.log('WebSocket 連線成功')
          },
          onDisconnect: () => {
            wsConnected.value = false
            console.log('WebSocket 連線斷開')
          },
          onPredictionResult: (data) => {
            handlePredictionResult(data)
          },
          onError: (error) => {
            errorMessage.value = `WebSocket 錯誤: ${error.message}`
          }
        })
        
        wsService.connect()

      } catch (error) {
        console.error('初始化失敗:', error)
        errorMessage.value = error.message
      } finally {
        isInitializing.value = false
      }
    }

    // 處理預測結果
    const handlePredictionResult = (data) => {
      currentPrediction.value = data.prediction
      currentAlert.value = data.alert
      
      console.log('收到預測結果:', data)
      
      // 如果是緊急情況，可以觸發額外的警報
      if (data.alert.is_emergency) {
        // 可以在這裡添加聲音警報、震動等
        console.log('🚨 緊急警報:', data.alert.type)
      }
    }

    // 處理音頻數據
    const handleAudioData = (audioData, sampleRate) => {
      // 更新波形視覺化
      if (audioVisualizer) {
        audioVisualizer.updateAudioData(audioData)
      }

      // 發送到後端進行分析
      if (wsService && wsConnected.value) {
        wsService.sendAudioData(audioData, sampleRate, sequenceNumber++)
      }
    }

    // 切換錄音狀態
    const toggleRecording = async () => {
      if (!audioRecorder || !audioInitialized.value) {
        errorMessage.value = '音頻系統未就緒'
        return
      }

      try {
        if (isRecording.value) {
          // 停止錄音
          audioRecorder.stopRecording()
          if (audioVisualizer) {
            audioVisualizer.stopVisualization()
          }
          isRecording.value = false
          console.log('錄音已停止')
        } else {
          // 開始錄音
          await audioRecorder.startRecording(handleAudioData)
          if (audioVisualizer) {
            audioVisualizer.startVisualization()
          }
          isRecording.value = true
          sequenceNumber = 0
          console.log('錄音已開始')
        }
      } catch (error) {
        console.error('錄音操作失敗:', error)
        errorMessage.value = error.message
      }
    }

    // 獲取預測條的樣式
    const getBarClass = (label, value) => {
      if (label === 'ambulance' || label === 'police') {
        return value > 0.7 ? 'bar-emergency' : 'bar-normal'
      }
      return 'bar-normal'
    }

    // 生命週期
    onMounted(() => {
      initialize()
    })

    onUnmounted(() => {
      // 清理資源
      if (audioRecorder) {
        audioRecorder.cleanup()
      }
      if (audioVisualizer) {
        audioVisualizer.stopVisualization()
      }
      if (wsService) {
        wsService.disconnect()
      }
    })

    return {
      // 響應式數據
      isRecording,
      isInitializing,
      isSupported,
      audioInitialized,
      wsConnected,
      currentAlert,
      currentPrediction,
      errorMessage,
      waveformCanvas,
      
      // 計算屬性
      recordingClass,
      
      // 方法
      toggleRecording,
      getBarClass,
      
      // 常量
      labels
    }
  }
}
</script>

<style scoped>
.audio-recorder {
  max-width: 1000px;
  margin: 0 auto;
}

.recorder-header {
  text-align: center;
  margin-bottom: 2rem;
}

.recorder-header h2 {
  color: #333;
  margin-bottom: 0.5rem;
}

.recorder-controls {
  text-align: center;
  margin-bottom: 2rem;
}

.connection-status {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-label {
  font-weight: 600;
  color: #333;
}

.waveform-section,
.prediction-section {
  margin-bottom: 2rem;
}

.waveform-section h3,
.prediction-section h3 {
  color: #333;
  margin-bottom: 1rem;
}

.prediction-details {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.prediction-bars {
  display: grid;
  gap: 1rem;
}

.prediction-bar {
  display: grid;
  grid-template-columns: 100px 1fr 60px;
  align-items: center;
  gap: 1rem;
}

.bar-label {
  font-weight: 600;
  text-transform: capitalize;
}

.bar-container {
  background: #e9ecef;
  height: 20px;
  border-radius: 10px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 10px;
}

.bar-normal {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.bar-emergency {
  background: linear-gradient(90deg, #dc3545, #c82333);
  animation: emergency-pulse 1s infinite alternate;
}

@keyframes emergency-pulse {
  0% { opacity: 1; }
  100% { opacity: 0.7; }
}

.bar-value {
  text-align: right;
  font-weight: 600;
  font-size: 0.9rem;
}

.emergency-alert {
  font-size: 1.2rem;
  font-weight: bold;
}

.safe-alert {
  font-size: 1.1rem;
}

.confidence {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 0.5rem;
}

.alert-error {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
}

.error-message {
  color: #dc3545;
  margin-top: 1rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .connection-status {
    flex-direction: column;
    gap: 1rem;
  }
  
  .prediction-bar {
    grid-template-columns: 80px 1fr 50px;
    gap: 0.5rem;
  }
}
</style>