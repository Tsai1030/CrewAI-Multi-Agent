@echo off
echo 🔧 安裝前端依賴
echo ================================

echo 📁 當前目錄: %CD%

echo 🗑️  清理舊的安裝...
if exist node_modules (
    echo 刪除 node_modules...
    rmdir /s /q node_modules
)

if exist package-lock.json (
    echo 刪除 package-lock.json...
    del package-lock.json
)

echo 🧹 清理 npm 快取...
npm cache clean --force

echo 📋 檢查 Node.js 版本...
node --version
npm --version

echo.
echo 📦 安裝依賴（這可能需要幾分鐘）...
npm install --legacy-peer-deps --verbose

echo.
echo 🔍 檢查 react-scripts 是否安裝...
if exist "node_modules\.bin\react-scripts.cmd" (
    echo ✅ react-scripts 安裝成功
) else (
    echo ❌ react-scripts 安裝失敗，嘗試單獨安裝...
    npm install react-scripts --save --legacy-peer-deps
)

echo.
echo 📊 檢查安裝結果...
npm list react-scripts

echo.
echo ✅ 安裝完成！
echo 💡 現在可以運行: npm start

pause
