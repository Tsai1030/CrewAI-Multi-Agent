# 紫微斗數 AI 系統安裝指南 - CrewAI + MCP 架構

## 📋 系統要求

- Python 3.11 或更高版本
- Conda 或 Miniconda
- 至少 8GB RAM
- 至少 10GB 可用磁盤空間

## 🚀 安裝步驟

### 1. 創建 Conda 環境

```bash
# 創建新的 conda 環境
conda create -n crewai python=3.11 -y

# 激活環境
conda activate crewai
```

### 2. 安裝依賴包

我們提供了多個版本的 requirements.txt，請根據您的需求選擇：

#### 選項 A: 完整版本（推薦）
```bash
pip install -r requirements_essential.txt
```

#### 選項 B: 核心版本
```bash
pip install -r requirements_core.txt
```

#### 選項 C: 最小版本
```bash
pip install -r requirements_minimal.txt
```

#### 選項 D: 清潔版本
```bash
pip install -r requirements_clean.txt
```

### 3. 環境配置

複製環境變數範本：
```bash
cp .env.example .env
```

編輯 `.env` 文件，填入您的 API 金鑰：
```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic API
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_BASE_URL=https://api.anthropic.com

# 其他配置
CREWAI_ENABLED=true
MCP_UNIFIED_SERVER_ENABLED=true
```

### 4. 測試安裝

運行測試腳本檢查安裝狀態：
```bash
python test_crewai_system.py
```

### 5. 啟動系統

#### 方法 A: 直接啟動 API 服務器
```bash
python api_server.py
```

#### 方法 B: 使用 uvicorn 啟動
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

#### 方法 C: 啟動 MCP 服務器（可選）
```bash
python mcp_server/server.py --standalone
```

## 🔧 故障排除

### 常見問題

#### 1. CrewAI 安裝失敗
```bash
# 如果 CrewAI 安裝失敗，嘗試單獨安裝
pip install crewai==0.28.8 --no-deps
pip install crewai-tools==0.1.6 --no-deps
```

#### 2. 依賴衝突
```bash
# 清理 pip 緩存
pip cache purge

# 重新安裝
pip install -r requirements_essential.txt --force-reinstall
```

#### 3. 內存不足
```bash
# 使用較小的批次大小安裝
pip install -r requirements_essential.txt --no-cache-dir
```

#### 4. 網絡問題
```bash
# 使用國內鏡像源
pip install -r requirements_essential.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 環境檢查

運行以下命令檢查環境：

```bash
# 檢查 Python 版本
python --version

# 檢查已安裝的包
pip list | grep -E "(crewai|fastapi|openai|anthropic)"

# 檢查環境變數
python -c "from src.config.settings import get_settings; print(get_settings().app.name)"
```

## 📁 文件結構說明

```
crewai/
├── 📋 requirements_*.txt     # 不同版本的依賴文件
├── 🧪 test_crewai_system.py # 系統測試腳本
├── 🚀 main.py               # 主程式（支援雙架構）
├── 🌐 api_server.py         # FastAPI 服務器
├── 🔧 mcp_server/           # 統一 MCP 服務器
├── 🤖 src/crew/             # CrewAI 多智能體系統
├── ⚙️ src/config/           # 配置管理
├── 🔍 src/rag/              # RAG 知識系統
├── 🌐 frontend/             # React 前端
└── 📚 docs/                 # 文檔
```

## 🎯 使用指南

### 1. 選擇架構

系統支援兩種架構：

- **CrewAI + MCP 架構**（推薦）：新的多智能體架構
- **Legacy Multi-Agent 架構**：原有的架構

### 2. API 端點

- `GET /` - 系統狀態
- `POST /analyze` - 紫微斗數分析
- `GET /status` - 詳細系統狀態
- `POST /switch-architecture` - 切換架構
- `GET /architecture` - 獲取當前架構

### 3. 前端訪問

啟動後訪問：
- API 文檔：http://localhost:8000/docs
- 前端界面：http://localhost:3000（需要單獨啟動）

## 🔄 架構切換

### 在運行時切換架構

```bash
# 切換到 CrewAI 架構
curl -X POST "http://localhost:8000/switch-architecture?use_crewai=true"

# 切換到 Legacy 架構
curl -X POST "http://localhost:8000/switch-architecture?use_crewai=false"

# 查看當前架構
curl -X GET "http://localhost:8000/architecture"
```

### 在代碼中切換架構

```python
from main import ZiweiAISystem

# 創建 CrewAI 系統
crewai_system = ZiweiAISystem(use_crewai=True)

# 創建 Legacy 系統
legacy_system = ZiweiAISystem(use_crewai=False)
```

## 📊 性能優化

### 1. 內存優化
```bash
# 設置環境變數
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
export TOKENIZERS_PARALLELISM=false
```

### 2. 並發設置
```bash
# 啟動時設置工作進程數
uvicorn api_server:app --workers 4 --host 0.0.0.0 --port 8000
```

### 3. 緩存配置
在 `.env` 文件中：
```env
CREWAI_CACHE_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

## 🆘 支援

如果遇到問題：

1. 檢查 `test_crewai_system.py` 的輸出
2. 查看日誌文件
3. 確認環境變數設置
4. 檢查網絡連接和 API 金鑰

## 📝 更新日誌

### v2.0.0 - CrewAI + MCP 架構
- ✅ 新增 CrewAI 多智能體框架
- ✅ 統一 MCP 服務器
- ✅ 雙架構支援
- ✅ 改進的工具管理
- ✅ 更好的錯誤處理

### v1.0.0 - Legacy Multi-Agent 架構
- ✅ 基礎多智能體系統
- ✅ RAG 知識檢索
- ✅ 紫微斗數分析
- ✅ Web API 接口
