# CNN Emergency Sound Web Version

基於 CNN 的緊急聲音識別系統 - 網頁版

## 🛠️ 技術棧

### 後端
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **WebSocket**: 即時音頻串流
- **AI**: TensorFlow/Keras + LibRosa

### 前端
- **Framework**: Vue.js 3
- **Package Manager**: PNPM
- **Audio**: Web Audio API
- **WebSocket**: Socket.IO Client

## 🚀 快速開始

### 後端啟動
```bash
cd web/backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 前端啟動
```bash
cd web/frontend
pnpm install
pnpm dev
```

## 📡 API 端點

- `GET /api/health` - 健康檢查
- `WebSocket /ws/audio` - 音頻串流處理
- `POST /api/upload-audio` - 音頻檔案上傳

## 🔧 開發工具

- 後端熱重載: `uvicorn app:app --reload`
- 前端熱重載: `pnpm dev`
- API 文檔: `http://localhost:8000/docs`