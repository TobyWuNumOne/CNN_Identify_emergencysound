# API 設計文檔

## 🌐 API 概覽

Base URL: `http://localhost:8000`

## 📡 REST API 端點

### 健康檢查
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 音頻檔案上傳
```http
POST /api/upload-audio
Content-Type: multipart/form-data
```

**Request:**
```
file: audio.wav (音頻檔案)
```

**Response:**
```json
{
  "prediction": [0.1, 0.8, 0.1],
  "labels": ["ambulance", "environment", "police"],
  "alert": {
    "is_emergency": true,
    "type": "environment",
    "confidence": 0.8
  },
  "processing_time": 0.5
}
```

## 🔌 WebSocket API

### 音頻串流處理
```
WebSocket: ws://localhost:8000/ws/audio
```

#### 客戶端發送格式
```json
{
  "type": "audio_data",
  "data": {
    "audio": "base64_encoded_audio_data",
    "sample_rate": 8000,
    "timestamp": 1640995200000,
    "sequence": 1
  }
}
```

#### 服務端回應格式
```json
{
  "type": "prediction_result",
  "data": {
    "prediction": [0.1, 0.8, 0.1],
    "labels": ["ambulance", "environment", "police"],
    "alert": {
      "is_emergency": true,
      "type": "environment",
      "confidence": 0.8
    },
    "timestamp": 1640995200000,
    "sequence": 1,
    "processing_time": 0.2
  }
}
```

#### 錯誤回應格式
```json
{
  "type": "error",
  "data": {
    "code": "AUDIO_PROCESSING_ERROR",
    "message": "Failed to process audio data",
    "timestamp": 1640995200000
  }
}
```

## 🎵 音頻數據格式

### 輸入要求
- **採樣率**: 8000Hz (前端降採樣後)
- **聲道**: 單聲道 (Mono)
- **格式**: Int16Array → Base64 編碼
- **長度**: 1秒音頻數據 (8000 samples)

### MFCC 特徵
- **係數數量**: 13
- **時間幀**: 44 frames
- **輸入形狀**: (1, 13, 44, 1)

## 🚨 警報判斷邏輯

基於現有桌面版邏輯 (`desktop/mfccs_value.py`):

```python
def check_emergency(prediction, threshold=0.7):
    labels = ["ambulance", "environment", "police"]
    max_idx = np.argmax(prediction)
    confidence = prediction[max_idx]
    
    if labels[max_idx] in ["ambulance", "police"] and confidence > threshold:
        return {
            "is_emergency": True,
            "type": labels[max_idx],
            "confidence": float(confidence)
        }
    return {
        "is_emergency": False,
        "type": None,
        "confidence": float(confidence)
    }
```

## 📊 性能指標

### 目標延遲
- WebSocket 往返: < 100ms
- 音頻處理: < 200ms
- 總延遲: < 300ms

### 流量估算
- 每秒數據: 16KB (8000 samples × 2 bytes)
- 每分鐘: 960KB
- 10 並發用戶: 9.6MB/分鐘

## 🔒 錯誤處理

### HTTP 狀態碼
- `200` - 成功
- `400` - 請求格式錯誤
- `413` - 檔案過大
- `422` - 音頻格式不支援
- `500` - 服務器內部錯誤

### WebSocket 錯誤類型
- `INVALID_AUDIO_FORMAT` - 音頻格式錯誤
- `AUDIO_PROCESSING_ERROR` - 處理失敗
- `MODEL_PREDICTION_ERROR` - 模型預測失敗
- `RATE_LIMIT_EXCEEDED` - 請求頻率過高