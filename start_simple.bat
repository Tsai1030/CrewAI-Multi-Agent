@echo off
echo 🌟 啟動紫微斗數 AI 系統（簡化版）
echo ================================

echo 📡 啟動 FastAPI 後端...
start "Backend" cmd /k "python api_server.py"

echo ⏳ 等待後端啟動...
timeout /t 3 /nobreak > nul

echo 🌐 啟動前端（如果有依賴問題會自動修復）...
cd frontend

echo 檢查依賴...
if not exist node_modules (
    echo 首次安裝依賴...
    npm install --legacy-peer-deps
)

echo 啟動開發服務器...
npm start

pause
