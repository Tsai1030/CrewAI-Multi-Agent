# GitHub 上傳指南

## 🎯 上傳到 GitHub 倉庫

### 📋 準備工作

1. **確認 Git 已安裝**
```bash
git --version
```

2. **設置 Git 用戶信息**（如果尚未設置）
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 🚀 上傳步驟

#### 1. 初始化本地 Git 倉庫
```bash
# 在項目根目錄執行
git init
```

#### 2. 添加遠程倉庫
```bash
git remote add origin https://github.com/Tsai1030/CrewAI-Multi-Agent.git
```

#### 3. 檢查要上傳的文件
```bash
# 查看將要添加的文件
git status

# 查看被忽略的文件
git status --ignored
```

#### 4. 添加文件到暫存區
```bash
# 添加所有文件（會自動排除 .gitignore 中的文件）
git add .

# 或者選擇性添加重要文件
git add README.md
git add main.py
git add api_server.py
git add requirements_essential.txt
git add src/
git add frontend/
git add .env.example
git add .gitignore
```

#### 5. 提交更改
```bash
git commit -m "🎉 Initial commit: CrewAI + MCP 紫微斗數 AI 分析系統

✨ 功能特色:
- 🤖 CrewAI 多智能體協作架構
- 🔧 MCP 工具統一管理
- 🧠 RAG 知識增強系統
- 📱 React 前端 + FastAPI 後端
- 🎨 雙架構支援 (CrewAI + Legacy)

🛠️ 技術棧:
- Python 3.11+ / CrewAI / FastAPI
- React 18+ / Material-UI
- OpenAI GPT-4o / Anthropic Claude
- ChromaDB / BGE-M3 嵌入模型"
```

#### 6. 推送到 GitHub
```bash
# 首次推送
git push -u origin main

# 如果遇到分支問題，可能需要：
git branch -M main
git push -u origin main
```

### 📁 確認上傳的核心文件

#### ✅ 必須上傳的文件：
- `README.md` - 項目說明文檔
- `main.py` - 主程式入口
- `api_server.py` - FastAPI 服務器
- `performance_config.py` - 性能配置
- `requirements_essential.txt` - 核心依賴
- `.env.example` - 環境變數範例
- `.gitignore` - Git 忽略規則

#### ✅ 核心目錄：
- `src/` - 源代碼目錄
  - `crew/` - CrewAI 系統
  - `config/` - 配置管理
  - `rag/` - RAG 知識系統
  - `agents/` - Legacy Agents
  - `prompts/` - Prompt 模板
  - `output/` - 輸出格式化
  - `utils/` - 工具函數

- `frontend/` - React 前端
  - `src/` - 前端源碼
  - `public/` - 靜態資源
  - `package.json` - 前端依賴

- `mcp_server/` - MCP 服務器
- `data/knowledge/` - 知識庫文件
- `docs/` - 文檔目錄
- `wizard_icon/` - 圖標資源
- `前後端呈現畫面/` - 展示截圖

#### ❌ 不會上傳的文件（已在 .gitignore 中）：
- 所有 `test_*.py` 測試文件
- 所有 `debug_*.py` 調試文件
- 所有 `demo_*.py` 演示文件
- `__pycache__/` 緩存目錄
- `cache/` 緩存文件
- `logs/` 日誌文件
- `vector_db_test*/` 測試數據庫
- `*.log` 日誌文件
- `.env` 環境變數文件（包含敏感信息）
- `node_modules/` Node.js 依賴

### 🔧 故障排除

#### 問題 1：推送被拒絕
```bash
# 如果遠程倉庫有內容，先拉取
git pull origin main --allow-unrelated-histories
git push origin main
```

#### 問題 2：文件太大
```bash
# 檢查大文件
git ls-files | xargs ls -la | sort -k5 -rn | head

# 移除大文件並重新提交
git rm --cached large_file.pdf
git commit --amend -m "Remove large files"
```

#### 問題 3：敏感信息洩露
```bash
# 如果意外提交了 .env 文件
git rm --cached .env
git commit -m "Remove sensitive .env file"
```

### 📊 上傳後檢查

1. **訪問 GitHub 倉庫**：https://github.com/Tsai1030/CrewAI-Multi-Agent
2. **檢查 README.md 顯示**：確認 Markdown 格式正確
3. **檢查文件結構**：確認所有必要文件都已上傳
4. **檢查 .gitignore**：確認敏感文件未被上傳

### 🎉 完成！

您的 CrewAI + MCP 紫微斗數 AI 分析系統現在已經成功上傳到 GitHub！

其他用戶可以通過以下方式克隆和使用：

```bash
git clone https://github.com/Tsai1030/CrewAI-Multi-Agent.git
cd CrewAI-Multi-Agent
cp .env.example .env
# 編輯 .env 文件添加 API 密鑰
pip install -r requirements_essential.txt
python api_server.py
```
