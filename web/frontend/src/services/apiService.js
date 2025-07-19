/**
 * API 服務 - 處理與後端的 HTTP 通訊
 */

import axios from 'axios'

// 創建 axios 實例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    console.log(`API 請求: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API 請求錯誤:', error)
    return Promise.reject(error)
  }
)

// 回應攔截器
api.interceptors.response.use(
  (response) => {
    console.log(`API 回應: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API 回應錯誤:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

/**
 * 檢查後端健康狀態
 */
export const checkBackendHealth = async () => {
  try {
    const response = await api.get('/api/health')
    return response.data
  } catch (error) {
    throw new Error(`健康檢查失敗: ${error.message}`)
  }
}

/**
 * 上傳音頻檔案進行分析
 */
export const uploadAudioFile = async (file, onProgress = null) => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    
    // 如果提供了進度回調
    if (onProgress) {
      config.onUploadProgress = (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        onProgress(percentCompleted)
      }
    }
    
    const response = await api.post('/api/upload-audio', formData, config)
    return response.data
  } catch (error) {
    if (error.response?.status === 413) {
      throw new Error('檔案過大，請選擇較小的音頻檔案')
    } else if (error.response?.status === 422) {
      throw new Error('不支援的音頻格式，請使用 WAV、MP3 或 M4A 格式')
    }
    throw new Error(`檔案上傳失敗: ${error.response?.data?.detail || error.message}`)
  }
}

/**
 * 獲取模型資訊
 */
export const getModelInfo = async () => {
  try {
    const response = await api.get('/api/model-info')
    return response.data
  } catch (error) {
    throw new Error(`獲取模型資訊失敗: ${error.message}`)
  }
}

export default api