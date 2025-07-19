/**
 * WebSocket 服務 - 處理即時音頻串流通訊
 */

import { io } from 'socket.io-client'

export class WebSocketService {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    
    // 事件回調
    this.onPredictionResult = null
    this.onError = null
    this.onConnect = null
    this.onDisconnect = null
  }

  /**
   * 連接 WebSocket
   */
  connect() {
    try {
      const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
      
      this.socket = io(wsUrl, {
        transports: ['websocket'],
        upgrade: false,
        rememberUpgrade: false
      })

      this.setupEventListeners()
      
      console.log('正在連接 WebSocket...')
      
    } catch (error) {
      console.error('WebSocket 連接失敗:', error)
      if (this.onError) {
        this.onError(error)
      }
    }
  }

  /**
   * 設置事件監聽器
   */
  setupEventListeners() {
    if (!this.socket) return

    // 連接成功
    this.socket.on('connect', () => {
      this.isConnected = true
      this.reconnectAttempts = 0
      console.log('WebSocket 連接成功')
      
      if (this.onConnect) {
        this.onConnect()
      }
    })

    // 連接斷開
    this.socket.on('disconnect', (reason) => {
      this.isConnected = false
      console.log('WebSocket 連接斷開:', reason)
      
      if (this.onDisconnect) {
        this.onDisconnect(reason)
      }
      
      // 自動重連
      this.handleReconnect()
    })

    // 預測結果
    this.socket.on('prediction_result', (data) => {
      console.log('收到預測結果:', data)
      
      if (this.onPredictionResult) {
        this.onPredictionResult(data)
      }
    })

    // 錯誤處理
    this.socket.on('error', (error) => {
      console.error('WebSocket 錯誤:', error)
      
      if (this.onError) {
        this.onError(error)
      }
    })

    // 連接錯誤
    this.socket.on('connect_error', (error) => {
      console.error('WebSocket 連接錯誤:', error)
      this.handleReconnect()
    })
  }

  /**
   * 處理重連邏輯
   */
  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)
      
      console.log(`${delay}ms 後嘗試重連 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      
      setTimeout(() => {
        if (!this.isConnected) {
          this.connect()
        }
      }, delay)
    } else {
      console.error('WebSocket 重連次數已達上限')
      if (this.onError) {
        this.onError(new Error('無法連接到服務器，請檢查網路連接'))
      }
    }
  }

  /**
   * 發送音頻數據
   */
  sendAudioData(audioData, sampleRate, sequence = 0) {
    if (!this.isConnected || !this.socket) {
      console.warn('WebSocket 未連接，無法發送音頻數據')
      return false
    }

    try {
      // 將 Int16Array 轉換為 Base64
      const audioBuffer = new Uint8Array(audioData.buffer)
      const base64Audio = btoa(String.fromCharCode(...audioBuffer))
      
      const message = {
        type: 'audio_data',
        data: {
          audio: base64Audio,
          sample_rate: sampleRate,
          timestamp: Date.now(),
          sequence: sequence
        }
      }

      this.socket.emit('audio_stream', message)
      return true
      
    } catch (error) {
      console.error('發送音頻數據失敗:', error)
      if (this.onError) {
        this.onError(error)
      }
      return false
    }
  }

  /**
   * 斷開連接
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
    this.isConnected = false
    this.reconnectAttempts = 0
    console.log('WebSocket 已斷開')
  }

  /**
   * 設置事件回調
   */
  setEventCallbacks({
    onPredictionResult,
    onError,
    onConnect,
    onDisconnect
  }) {
    this.onPredictionResult = onPredictionResult
    this.onError = onError
    this.onConnect = onConnect
    this.onDisconnect = onDisconnect
  }

  /**
   * 獲取連接狀態
   */
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      maxReconnectAttempts: this.maxReconnectAttempts
    }
  }
}