# 專案結構說明

## 📁 目錄重組完成

```
CNN_Identify_emergencysound/
├── desktop/                    # 桌面版代碼 (原有功能)
│   ├── Toby/                  # 原 Toby 資料夾
│   ├── toby_test_RsPi/        # 樹莓派測試代碼
│   ├── *.py                   # 所有原始 Python 檔案
│   ├── *.npy, *.csv, *.wav    # 數據檔案
│   ├── test_audio/            # 測試音頻檔案
│   ├── data_npy/              # 訓練數據
│   └── req.txt                # 桌面版依賴
├── web/                       # 網頁版 (新增)
│   ├── backend/               # Flask 後端
│   │   ├── services/          # 業務邏輯服務
│   │   └── utils/             # 工具函數
│   └── frontend/              # Vue.js 前端
│       └── src/
│           ├── components/    # Vue 組件
│           ├── views/         # 頁面視圖
│           └── services/      # 前端服務
├── shared/                    # 共用資源
│   ├── models/               # AI 模型檔案 (從原 models/ 移動)
│   └── utils/                # 共用工具函數
└── README.md                 # 專案說明
```

## 🔄 重組完成的內容

### ✅ 已移動的檔案：
- **模型檔案**: `models/*` → `shared/models/`
- **桌面版代碼**: 所有 `.py` 檔案 → `desktop/`
- **Toby 資料夾**: `Toby/` → `desktop/Toby/`
- **樹莓派代碼**: `toby_test_RsPi/` → `desktop/toby_test_RsPi/`
- **數據檔案**: `*.npy`, `*.csv`, `*.wav` → `desktop/`
- **測試資料**: `test_audio/`, `data_npy/`, `wav_test/` → `desktop/`

### ✅ 已建立的新結構：
- **網頁版後端**: `web/backend/` (包含 services, utils)
- **網頁版前端**: `web/frontend/src/` (包含 components, views, services)
- **共用資源**: `shared/` (包含 models, utils)

## 🎯 下一步開發計劃

### 1. Flask 後端開發
- 建立 `web/backend/app.py` - 主要 Flask 應用
- 建立 `web/backend/services/model_service.py` - 模型服務
- 建立 `web/backend/services/mfcc_extractor.py` - MFCC 特徵提取
- 建立 `web/backend/services/audio_processor.py` - 音頻處理

### 2. Vue.js 前端開發
- 初始化 Vue 專案在 `web/frontend/`
- 建立音頻錄製組件
- 建立波形顯示組件
- 建立警報面板組件

### 3. Docker 配置
- 建立 `web/backend/Dockerfile`
- 建立 `web/frontend/Dockerfile`
- 建立 `web/docker-compose.yml`

## 💡 重用現有代碼的策略

可以直接重用的核心模組：
- `desktop/mfccs_value.py` → 轉換為 `web/backend/services/mfcc_extractor.py`
- `desktop/helpers.py` → 已複製到 `shared/utils/helpers.py`
- `desktop/model_prediction.py` → 轉換為 `web/backend/services/model_service.py`
- `shared/models/simple-train-nb30&25/` → 直接使用的 AI 模型