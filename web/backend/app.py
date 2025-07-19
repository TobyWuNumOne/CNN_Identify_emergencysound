"""
CNN Emergency Sound Detection - Web API
基於 FastAPI 的緊急聲音識別 Web 服務
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import json
import base64
import numpy as np
from datetime import datetime
from typing import Dict, List
import logging

# 導入自定義服務
from services.model_service import ModelService
from services.mfcc_extractor import MFCCExtractor
from services.audio_processor import AudioProcessor

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 創建 FastAPI 應用
app = FastAPI(
    title="CNN Emergency Sound Detection API",
    description="基於 CNN 的緊急聲音識別系統 Web API",
    version="1.0.0"
)

# CORS 設置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vue.js 開發服務器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服務
model_service = ModelService()
mfcc_extractor = MFCCExtractor()
audio_processor = AudioProcessor()

# WebSocket 連線管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

manager = ConnectionManager()

@app.get("/")
async def root():
    """根路徑 - API 資訊"""
    return {
        "message": "CNN Emergency Sound Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model_service.is_loaded(),
        "services": {
            "model_service": "ready",
            "mfcc_extractor": "ready",
            "audio_processor": "ready"
        }
    }

@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """音頻檔案上傳處理"""
    try:
        # 檢查檔案類型
        if not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="檔案必須是音頻格式")
        
        # 讀取音頻檔案
        audio_data = await file.read()
        
        # 處理音頻
        processed_audio = audio_processor.process_uploaded_audio(audio_data)
        
        # 提取 MFCC 特徵
        mfcc_features = mfcc_extractor.extract(processed_audio, sample_rate=8000)
        
        # 模型預測
        prediction = model_service.predict(mfcc_features)
        
        # 檢查是否為緊急情況
        alert = model_service.check_emergency(prediction)
        
        return {
            "prediction": prediction.tolist(),
            "labels": model_service.get_labels(),
            "alert": alert,
            "processing_time": 0.5,  # TODO: 實際計算處理時間
            "filename": file.filename
        }
        
    except Exception as e:
        logger.error(f"音頻處理錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音頻處理失敗: {str(e)}")

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 音頻串流處理"""
    await manager.connect(websocket)
    
    try:
        while True:
            # 接收客戶端數據
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "audio_data":
                try:
                    # 解碼音頻數據
                    audio_base64 = message["data"]["audio"]
                    audio_bytes = base64.b64decode(audio_base64)
                    audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
                    audio_float = audio_array.astype(np.float32) / 32767.0
                    
                    # 提取 MFCC 特徵
                    mfcc_features = mfcc_extractor.extract(
                        audio_float, 
                        sample_rate=message["data"]["sample_rate"]
                    )
                    
                    # 模型預測
                    prediction = model_service.predict(mfcc_features)
                    
                    # 檢查緊急情況
                    alert = model_service.check_emergency(prediction)
                    
                    # 回傳結果
                    response = {
                        "type": "prediction_result",
                        "data": {
                            "prediction": prediction.tolist(),
                            "labels": model_service.get_labels(),
                            "alert": alert,
                            "timestamp": message["data"]["timestamp"],
                            "sequence": message["data"]["sequence"],
                            "processing_time": 0.2  # TODO: 實際計算
                        }
                    }
                    
                    await manager.send_personal_message(response, websocket)
                    
                except Exception as e:
                    error_response = {
                        "type": "error",
                        "data": {
                            "code": "AUDIO_PROCESSING_ERROR",
                            "message": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                    await manager.send_personal_message(error_response, websocket)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket 錯誤: {str(e)}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )