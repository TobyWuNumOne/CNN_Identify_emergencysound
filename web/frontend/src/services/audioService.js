/**
 * 音頻服務 - 處理前端音頻錄製和處理
 */

/**
 * 音頻錄製器類別
 */
export class AudioRecorder {
  constructor() {
    this.mediaStream = null
    this.audioContext = null
    this.processor = null
    this.isRecording = false
    this.onAudioData = null
    this.sampleRate = 22050
  }

  /**
   * 初始化音頻錄製
   */
  async initialize() {
    try {
      // 請求麥克風權限
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: this.sampleRate,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        }
      })

      // 創建音頻上下文
      this.audioContext = new AudioContext({ sampleRate: this.sampleRate })
      
      console.log(`音頻上下文初始化成功，採樣率: ${this.audioContext.sampleRate}Hz`)
      
      return true
    } catch (error) {
      console.error('音頻初始化失敗:', error)
      throw new Error(`無法存取麥克風: ${error.message}`)
    }
  }

  /**
   * 開始錄音
   */
  async startRecording(onAudioData) {
    if (!this.audioContext || !this.mediaStream) {
      throw new Error('音頻系統未初始化')
    }

    this.onAudioData = onAudioData
    
    try {
      // 創建音頻源
      const source = this.audioContext.createMediaStreamSource(this.mediaStream)
      
      // 創建音頻處理器 (使用較小的 buffer size 以減少延遲)
      this.processor = this.audioContext.createScriptProcessor(1024, 1, 1)
      
      // 音頻處理回調
      this.processor.onaudioprocess = (event) => {
        if (this.isRecording && this.onAudioData) {
          const audioData = event.inputBuffer.getChannelData(0)
          
          // 降採樣到 8000Hz (減少流量)
          const downsampledData = this.downsample(audioData, this.audioContext.sampleRate, 8000)
          
          // 轉換為 Int16Array 以減少傳輸量
          const int16Data = this.floatToInt16(downsampledData)
          
          this.onAudioData(int16Data, 8000)
        }
      }
      
      // 連接音頻節點
      source.connect(this.processor)
      this.processor.connect(this.audioContext.destination)
      
      this.isRecording = true
      console.log('開始錄音')
      
    } catch (error) {
      console.error('開始錄音失敗:', error)
      throw new Error(`錄音啟動失敗: ${error.message}`)
    }
  }

  /**
   * 停止錄音
   */
  stopRecording() {
    this.isRecording = false
    
    if (this.processor) {
      this.processor.disconnect()
      this.processor = null
    }
    
    console.log('停止錄音')
  }

  /**
   * 清理資源
   */
  cleanup() {
    this.stopRecording()
    
    if (this.audioContext) {
      this.audioContext.close()
      this.audioContext = null
    }
    
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop())
      this.mediaStream = null
    }
    
    console.log('音頻資源已清理')
  }

  /**
   * 降採樣音頻數據
   */
  downsample(audioData, originalSampleRate, targetSampleRate) {
    if (originalSampleRate === targetSampleRate) {
      return audioData
    }
    
    const ratio = originalSampleRate / targetSampleRate
    const newLength = Math.round(audioData.length / ratio)
    const result = new Float32Array(newLength)
    
    for (let i = 0; i < newLength; i++) {
      const index = Math.round(i * ratio)
      result[i] = audioData[index] || 0
    }
    
    return result
  }

  /**
   * 將 Float32 轉換為 Int16
   */
  floatToInt16(floatArray) {
    const int16Array = new Int16Array(floatArray.length)
    for (let i = 0; i < floatArray.length; i++) {
      // 限制在 [-1, 1] 範圍內，然後轉換為 16-bit
      const clampedValue = Math.max(-1, Math.min(1, floatArray[i]))
      int16Array[i] = Math.round(clampedValue * 32767)
    }
    return int16Array
  }

  /**
   * 檢查瀏覽器支援
   */
  static isSupported() {
    return !!(
      navigator.mediaDevices &&
      navigator.mediaDevices.getUserMedia &&
      window.AudioContext
    )
  }
}

/**
 * 音頻視覺化器
 */
export class AudioVisualizer {
  constructor(canvas) {
    this.canvas = canvas
    this.ctx = canvas.getContext('2d')
    this.animationId = null
    this.audioData = new Float32Array(1024)
  }

  /**
   * 更新音頻數據
   */
  updateAudioData(audioData) {
    // 將 Int16 轉換回 Float32 用於視覺化
    this.audioData = new Float32Array(audioData.length)
    for (let i = 0; i < audioData.length; i++) {
      this.audioData[i] = audioData[i] / 32767.0
    }
  }

  /**
   * 開始繪製波形
   */
  startVisualization() {
    const draw = () => {
      this.drawWaveform()
      this.animationId = requestAnimationFrame(draw)
    }
    draw()
  }

  /**
   * 停止視覺化
   */
  stopVisualization() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId)
      this.animationId = null
    }
  }

  /**
   * 繪製波形
   */
  drawWaveform() {
    const { width, height } = this.canvas
    
    // 清除畫布
    this.ctx.fillStyle = '#1a1a1a'
    this.ctx.fillRect(0, 0, width, height)
    
    // 繪製波形
    this.ctx.strokeStyle = '#00ff88'
    this.ctx.lineWidth = 2
    this.ctx.beginPath()
    
    const sliceWidth = width / this.audioData.length
    let x = 0
    
    for (let i = 0; i < this.audioData.length; i++) {
      const v = this.audioData[i]
      const y = (v + 1) * height / 2
      
      if (i === 0) {
        this.ctx.moveTo(x, y)
      } else {
        this.ctx.lineTo(x, y)
      }
      
      x += sliceWidth
    }
    
    this.ctx.stroke()
    
    // 繪製中心線
    this.ctx.strokeStyle = '#333'
    this.ctx.lineWidth = 1
    this.ctx.beginPath()
    this.ctx.moveTo(0, height / 2)
    this.ctx.lineTo(width, height / 2)
    this.ctx.stroke()
  }
}