@echo off
echo 🚀 啟動紫微斗數 AI 系統
echo ================================

echo 📡 啟動 FastAPI 後端服務器...
start "FastAPI Backend" cmd /k "python api_server.py"

echo ⏳ 等待後端啟動...
timeout /t 5 /nobreak > nul

echo 🌐 啟動 React 前端開發服務器...
cd frontend
start "React Frontend" cmd /k "npm start"

echo ✅ 系統啟動完成！
echo.
echo 📋 服務信息：
echo    後端 API: http://localhost:8000
echo    前端界面: http://localhost:3000
echo    API 文檔: http://localhost:8000/docs
echo.
echo 💡 提示：
echo    - 確保已安裝 Node.js 和 npm
echo    - 確保已安裝 Python 依賴包
echo    - 確保 .env 文件配置正確
echo.
pause
