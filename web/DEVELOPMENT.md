# 開發進度記錄

## 📋 專案狀態

### ✅ 已完成
- [x] 專案目錄結構重組
- [x] 前後端技術選型
- [x] 流量優化方案設計
- [x] 開發環境配置

### 🔄 進行中
- [ ] FastAPI 後端開發
- [ ] Vue.js 前端開發
- [ ] Docker 容器化配置

### 📅 待完成
- [ ] WebSocket 即時通訊
- [ ] 音頻處理管道
- [ ] AI 模型整合
- [ ] 前端音頻視覺化
- [ ] 部署配置

## 🎯 技術決策記錄

### 後端選擇: FastAPI + Uvicorn
**原因**: 
- 高性能 ASGI 支援
- 原生 async/await
- 自動 API 文檔生成
- 優秀的 WebSocket 支援

### 前端選擇: Vue.js + PNPM
**原因**:
- 響應式數據綁定適合即時音頻
- 組件化開發
- PNPM 更快的安裝速度
- 更好的依賴管理

### 流量優化策略
- 前端降採樣: 22050Hz → 8000Hz
- 批次傳送: 每秒一次
- 數據壓縮: Int16Array 格式
- 預期流量: 16KB/秒/用戶

## 🔧 開發環境

### 後端依賴
- fastapi
- uvicorn[standard]
- websockets
- tensorflow
- librosa
- numpy

### 前端依賴
- vue@next
- socket.io-client
- @vueuse/core
- typescript (可選)

## 📝 重要檔案路徑

### 共用資源
- AI 模型: `../../shared/models/simple-train-nb30&25/`
- 工具函數: `../../shared/utils/helpers.py`

### 桌面版參考
- MFCC 提取: `../../desktop/mfccs_value.py`
- 模型預測: `../../desktop/model_prediction.py`
- 音頻處理: `../../desktop/Toby/threading_bata4.py`

## 🐛 已知問題
- [ ] 模型路徑需要調整
- [ ] CORS 設定需要配置
- [ ] WebSocket 連線穩定性待測試

## 📚 參考資料
- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [Vue.js 3 官方文檔](https://vuejs.org/)
- [Web Audio API MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)