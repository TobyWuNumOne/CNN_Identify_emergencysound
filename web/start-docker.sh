#!/bin/bash

# Docker 環境啟動腳本

echo "🐳 啟動 CNN 緊急聲音識別系統 - Docker 環境"
echo "============================================="

# 檢查 Docker 和 Docker Compose
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 未安裝，請先安裝 $1"
        exit 1
    fi
}

echo "📋 檢查系統需求..."
check_command "docker"
check_command "docker-compose"

# 檢查 Docker 是否運行
if ! docker info &> /dev/null; then
    echo "❌ Docker 服務未運行，請啟動 Docker"
    exit 1
fi

# 停止現有容器
echo "🛑 停止現有容器..."
docker-compose down

# 構建並啟動服務
echo "🔨 構建並啟動服務..."
docker-compose up --build -d

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 10

# 檢查服務狀態
echo "📊 檢查服務狀態..."
docker-compose ps

# 等待後端健康檢查通過
echo "❤️  等待後端健康檢查..."
for i in {1..30}; do
    if curl -f http://localhost:8000/api/health &> /dev/null; then
        echo "✅ 後端服務健康"
        break
    fi
    echo "⏳ 等待後端啟動... ($i/30)"
    sleep 2
done

# 檢查前端
echo "🎨 檢查前端服務..."
if curl -f http://localhost/ &> /dev/null; then
    echo "✅ 前端服務正常"
else
    echo "⚠️  前端服務可能還在啟動中"
fi

echo ""
echo "✅ Docker 服務啟動完成！"
echo "============================================="
echo "🌐 應用: http://localhost"
echo "🔧 後端 API: http://localhost:8000"
echo "📚 API 文檔: http://localhost:8000/docs"
echo "❤️  健康檢查: http://localhost:8000/api/health"
echo ""
echo "📋 管理命令:"
echo "  查看日誌: docker-compose logs -f"
echo "  停止服務: docker-compose down"
echo "  重啟服務: docker-compose restart"
echo "  查看狀態: docker-compose ps"