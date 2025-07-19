#!/bin/bash

# 開發環境啟動腳本

echo "🚀 啟動 CNN 緊急聲音識別系統 - 開發環境"
echo "========================================"

# 檢查是否安裝了必要的工具
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 未安裝，請先安裝 $1"
        exit 1
    fi
}

echo "📋 檢查系統需求..."
check_command "python3"
check_command "pnpm"
check_command "uvicorn"

# 設置環境變數
export PYTHONPATH="${PWD}/backend:${PYTHONPATH}"

# 啟動後端
echo ""
echo "🔧 啟動後端服務..."
cd backend

# 檢查虛擬環境
if [ ! -d "venv" ]; then
    echo "📦 創建虛擬環境..."
    python3 -m venv venv
fi

# 激活虛擬環境
source venv/bin/activate

# 安裝依賴
echo "📦 安裝後端依賴..."
pip install -r requirements.txt

# 啟動後端服務
echo "🚀 啟動 FastAPI 服務 (端口: 8000)..."
uvicorn app:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待後端啟動
sleep 3

# 啟動前端
echo ""
echo "🎨 啟動前端服務..."
cd ../frontend

# 安裝依賴
echo "📦 安裝前端依賴..."
pnpm install

# 啟動前端服務
echo "🚀 啟動 Vue.js 服務 (端口: 5173)..."
pnpm dev &
FRONTEND_PID=$!

# 等待服務啟動
sleep 5

echo ""
echo "✅ 服務啟動完成！"
echo "========================================"
echo "🌐 前端: http://localhost:5173"
echo "🔧 後端: http://localhost:8000"
echo "📚 API 文檔: http://localhost:8000/docs"
echo "❤️  健康檢查: http://localhost:8000/api/health"
echo ""
echo "按 Ctrl+C 停止所有服務"

# 等待用戶中斷
trap "echo ''; echo '🛑 正在停止服務...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

# 保持腳本運行
wait