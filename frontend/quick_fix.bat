@echo off
echo 🚀 快速修復前端
echo ================================

echo 📁 進入前端目錄...
cd /d "%~dp0"

echo 🔄 使用最小化配置...
copy package_minimal.json package.json

echo 🗑️  清理...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

echo 📦 安裝核心依賴...
npm install

echo ✅ 修復完成！

echo.
echo 🎯 現在嘗試啟動：
echo    npm start
echo.

pause
