<template>
  <div class="file-upload">
    <div class="upload-header">
      <h2>📁 音頻檔案上傳</h2>
      <p>上傳音頻檔案進行緊急聲音分析</p>
    </div>

    <!-- 檔案上傳區域 -->
    <div class="upload-section">
      <div 
        class="upload-dropzone"
        :class="{ 'dragover': isDragOver, 'uploading': isUploading }"
        @drop="handleDrop"
        @dragover.prevent="isDragOver = true"
        @dragleave="isDragOver = false"
        @click="triggerFileInput"
      >
        <input
          ref="fileInput"
          type="file"
          accept="audio/*"
          @change="handleFileSelect"
          style="display: none"
        />
        
        <div class="upload-content">
          <div class="upload-icon">
            <span v-if="isUploading">⏳</span>
            <span v-else>📁</span>
          </div>
          
          <div class="upload-text">
            <h3 v-if="isUploading">上傳中...</h3>
            <h3 v-else>點擊或拖拽檔案到此處</h3>
            <p>支援 WAV, MP3, M4A 等音頻格式</p>
            <p class="file-size-limit">檔案大小限制: 10MB</p>
          </div>
          
          <!-- 上傳進度 -->
          <div v-if="isUploading" class="upload-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: uploadProgress + '%' }"
              ></div>
            </div>
            <span class="progress-text">{{ uploadProgress }}%</span>
          </div>
        </div>
      </div>

      <!-- 選中的檔案資訊 -->
      <div v-if="selectedFile && !isUploading" class="file-info">
        <h4>選中的檔案</h4>
        <div class="file-details">
          <div class="file-item">
            <span class="file-icon">🎵</span>
            <div class="file-meta">
              <div class="file-name">{{ selectedFile.name }}</div>
              <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
            </div>
            <button @click="uploadFile" class="btn btn-primary">
              分析檔案
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分析結果 -->
    <div v-if="analysisResult" class="result-section">
      <h3>分析結果</h3>
      <div class="result-card">
        <!-- 主要結果 -->
        <div 
          :class="['alert', analysisResult.alert.is_emergency ? 'alert-emergency' : 'alert-safe']"
        >
          <div class="alert-content">
            <div class="alert-icon">
              {{ analysisResult.alert.is_emergency ? '🚨' : '✅' }}
            </div>
            <div class="alert-text">
              <strong v-if="analysisResult.alert.is_emergency">
                檢測到緊急聲音: {{ analysisResult.alert.type }}
              </strong>
              <strong v-else>未檢測到緊急聲音</strong>
              <div class="confidence">
                信心度: {{ (analysisResult.alert.confidence * 100).toFixed(1) }}%
              </div>
            </div>
          </div>
        </div>

        <!-- 詳細分析 -->
        <div class="analysis-details">
          <h4>詳細分析結果</h4>
          <div class="prediction-grid">
            <div 
              v-for="(value, index) in analysisResult.prediction" 
              :key="index"
              class="prediction-item"
            >
              <div class="prediction-label">
                {{ analysisResult.labels[index] }}
              </div>
              <div class="prediction-bar">
                <div 
                  class="prediction-fill" 
                  :style="{ 
                    width: (value * 100) + '%',
                    backgroundColor: getBarColor(value)
                  }"
                ></div>
              </div>
              <div class="prediction-value">
                {{ (value * 100).toFixed(1) }}%
              </div>
            </div>
          </div>
        </div>

        <!-- 檔案資訊 -->
        <div class="file-analysis-info">
          <h4>檔案資訊</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">檔案名稱:</span>
              <span class="info-value">{{ analysisResult.filename }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">處理時間:</span>
              <span class="info-value">{{ analysisResult.processing_time }}秒</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 錯誤訊息 -->
    <div v-if="errorMessage" class="error-section">
      <div class="alert alert-error">
        <strong>❌ 錯誤:</strong> {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { uploadAudioFile } from '../services/apiService'

export default {
  name: 'FileUpload',
  setup() {
    // 響應式數據
    const selectedFile = ref(null)
    const isUploading = ref(false)
    const uploadProgress = ref(0)
    const isDragOver = ref(false)
    const analysisResult = ref(null)
    const errorMessage = ref('')
    const fileInput = ref(null)

    // 觸發檔案選擇
    const triggerFileInput = () => {
      if (!isUploading.value) {
        fileInput.value?.click()
      }
    }

    // 處理檔案選擇
    const handleFileSelect = (event) => {
      const files = event.target.files
      if (files && files.length > 0) {
        selectFile(files[0])
      }
    }

    // 處理拖拽上傳
    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      
      const files = event.dataTransfer.files
      if (files && files.length > 0) {
        selectFile(files[0])
      }
    }

    // 選擇檔案
    const selectFile = (file) => {
      // 清除之前的結果
      analysisResult.value = null
      errorMessage.value = ''
      
      // 檢查檔案類型
      if (!file.type.startsWith('audio/')) {
        errorMessage.value = '請選擇音頻檔案 (WAV, MP3, M4A 等)'
        return
      }
      
      // 檢查檔案大小 (10MB)
      if (file.size > 10 * 1024 * 1024) {
        errorMessage.value = '檔案大小不能超過 10MB'
        return
      }
      
      selectedFile.value = file
    }

    // 上傳檔案
    const uploadFile = async () => {
      if (!selectedFile.value) return
      
      isUploading.value = true
      uploadProgress.value = 0
      errorMessage.value = ''
      
      try {
        const result = await uploadAudioFile(
          selectedFile.value,
          (progress) => {
            uploadProgress.value = progress
          }
        )
        
        analysisResult.value = result
        
        // 如果檢測到緊急情況，顯示通知
        if (result.alert.is_emergency) {
          if (Notification.permission === 'granted') {
            new Notification('檢測到緊急聲音!', {
              body: `檔案: ${result.filename}\n類型: ${result.alert.type}`,
              icon: '/emergency-icon.png'
            })
          }
        }
        
      } catch (error) {
        errorMessage.value = error.message
      } finally {
        isUploading.value = false
        uploadProgress.value = 0
      }
    }

    // 格式化檔案大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // 獲取進度條顏色
    const getBarColor = (value) => {
      if (value > 0.7) return '#ff6b6b'  // 紅色 - 高信心度
      if (value > 0.4) return '#ffa726'  // 橙色 - 中信心度
      return '#66bb6a'                   // 綠色 - 低信心度
    }

    return {
      selectedFile,
      isUploading,
      uploadProgress,
      isDragOver,
      analysisResult,
      errorMessage,
      fileInput,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      uploadFile,
      formatFileSize,
      getBarColor
    }
  }
}
</script>

<style scoped>
.file-upload {
  max-width: 800px;
  margin: 0 auto;
}

.upload-header {
  text-align: center;
  margin-bottom: 2rem;
}

.upload-dropzone {
  border: 3px dashed #ddd;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
}

.upload-dropzone:hover,
.upload-dropzone.dragover {
  border-color: #007bff;
  background: #f0f8ff;
}

.upload-dropzone.uploading {
  cursor: not-allowed;
  opacity: 0.7;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  font-size: 4rem;
}

.upload-text h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.upload-text p {
  margin: 0.25rem 0;
  color: #666;
}

.file-size-limit {
  font-size: 0.9rem;
  color: #999;
}

.upload-progress {
  width: 100%;
  max-width: 300px;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #007bff, #0056b3);
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: 600;
  color: #007bff;
}

.file-info {
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.file-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-icon {
  font-size: 2rem;
}

.file-meta {
  flex: 1;
}

.file-name {
  font-weight: 600;
  color: #333;
}

.file-size {
  color: #666;
  font-size: 0.9rem;
}

.result-section {
  margin-top: 2rem;
}

.result-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.alert-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.alert-icon {
  font-size: 2.5rem;
}

.alert-text {
  flex: 1;
}

.confidence {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 0.25rem;
}

.analysis-details {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.prediction-grid {
  display: grid;
  gap: 1rem;
}

.prediction-item {
  display: grid;
  grid-template-columns: 120px 1fr 80px;
  align-items: center;
  gap: 1rem;
}

.prediction-label {
  font-weight: 600;
  text-transform: capitalize;
}

.prediction-bar {
  height: 24px;
  background: #f0f0f0;
  border-radius: 12px;
  overflow: hidden;
}

.prediction-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 0.5s ease;
}

.prediction-value {
  text-align: right;
  font-weight: 600;
}

.file-analysis-info {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.info-grid {
  display: grid;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
}

.info-label {
  font-weight: 600;
  color: #666;
}

.info-value {
  color: #333;
}

.error-section {
  margin-top: 2rem;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>