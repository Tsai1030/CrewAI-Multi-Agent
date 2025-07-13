@echo off
echo 🔧 修復前端依賴問題
echo ================================

echo 📁 進入前端目錄...
cd /d "%~dp0"

echo 🗑️  清理舊的依賴...
if exist node_modules (
    echo 正在刪除 node_modules...
    rmdir /s /q node_modules
)

if exist package-lock.json (
    echo 正在刪除 package-lock.json...
    del package-lock.json
)

echo 🧹 清理 npm 快取...
npm cache clean --force

echo 📦 重新安裝依賴...
npm install --legacy-peer-deps

echo 🔒 修復安全漏洞...
npm audit fix --force

echo ✅ 依賴修復完成！

echo.
echo 💡 說明：
echo    - 使用 --legacy-peer-deps 解決版本衝突
echo    - 自動修復了安全漏洞
echo    - 升級到 tsparticles v3
echo.
echo 🚀 現在可以運行：npm start
echo.

pause
