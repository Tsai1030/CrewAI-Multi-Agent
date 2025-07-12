@echo off
echo 🚀 開始 Git 推送到 GitHub
echo ================================

echo 📁 初始化 Git 倉庫...
git init

echo 📝 添加遠程倉庫...
git remote add origin https://github.com/Tsai1030/Multi-Agents.git

echo 📋 添加所有檔案...
git add .

echo 💬 提交變更...
git commit -m "Initial commit: Multi-Agent 紫微斗數 AI 系統"

echo 🌐 推送到 GitHub...
git push -u origin main

echo ✅ 推送完成！
pause
