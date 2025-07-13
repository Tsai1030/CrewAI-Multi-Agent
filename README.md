# 🌟 Multi-Agent 紫微斗數 AI 系統 (Full-Stack)

一個基於多智能體協作的紫微斗數命理分析系統，結合了 RAG（檢索增強生成）技術和先進的 AI 模型。

**🆕 最新版本特色**:
- ✅ **完整前後端系統** - FastAPI + React 全棧應用
- ✅ **現代化 UI 界面** - Material-UI + Framer Motion 動畫
- ✅ **響應式設計** - 支援桌面和移動設備
- ✅ **實時 API 整合** - 前後端無縫連接

## 🌟 系統特色

### 🤖 Multi-Agent 協作架構
- **Claude Agent**: 專精邏輯推理和結構化分析
- **GPT Agent**: 擅長創意表達和故事化解釋
- **Domain Agents**: 專門領域分析（愛情、財富、未來運勢）
- **協調器**: 管理 Agent 間的討論和共識達成

### 📚 RAG 知識系統
- 使用 HuggingFace BGE-M3 嵌入模型
- 持久化向量資料庫（Chroma）
- 紫微斗數專業知識庫
- 智能檢索和上下文增強

### 🎯 多種輸出格式
- **JSON 格式**: 結構化數據輸出
- **論述格式**: 自然語言分析報告
- **JSON 轉論述**: 結合精確分析與易讀輸出

### 🔧 靈活配置
- 可選擇不同分析領域（愛情、財富、未來、綜合）
- 可控制 Agent 協作過程顯示
- 支援多種輸出格式切換

## 📁 項目結構

```
Multi-Agents/
├── main.py                    # 主程序入口
├── src/
│   ├── agents/                # Multi-Agent 系統
│   │   ├── coordinator.py     # 協調器
│   │   ├── claude_agent.py    # Claude Agent
│   │   ├── gpt_agent.py       # GPT Agent
│   │   └── domain_agent.py    # 領域專家 Agent
│   ├── rag/                   # RAG 系統
│   │   ├── embeddings.py      # 嵌入模型
│   │   ├── vector_store.py    # 向量資料庫
│   │   └── generator.py       # 生成器
│   ├── output/                # 輸出格式化
│   │   └── gpt4o_formatter.py # GPT-4o 格式化器
│   ├── prompts/               # Prompt 模板
│   │   └── system_prompts.py  # 系統 Prompt
│   └── tools/                 # 工具模組
│       └── ziwei_tool.py      # 紫微斗數工具
├── .env                       # 環境變數（不包含在 Git 中）
├── .gitignore                 # Git 忽略文件
└── requirements.txt           # Python 依賴
```

## 🚀 快速開始

### 1. 環境設置

```bash
# 克隆項目
git clone https://github.com/Tsai1030/Multi-Agents.git
cd Multi-Agents

# 安裝依賴
pip install -r requirements.txt
```

### 2. 配置環境變數

創建 `.env` 文件並添加以下配置：

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# RAG 設置
VECTOR_DB_NAME=test1
VECTOR_DB_PATH=./vector_db_test1

# 其他設置
DEFAULT_OUTPUT_FORMAT=json_to_narrative
SHOW_AGENT_PROCESS=false
```

### 3. 運行系統

```bash
python main.py
```

## 🎛️ 使用配置

### 選擇分析領域

在 `main.py` 中修改 `domain_type` 參數：

```python
result = await system.analyze_ziwei_chart(
    birth_data=sample_birth_data,
    domain_type="love",        # 選擇領域
    output_format="json_to_narrative",
    show_agent_process=True
)
```

**可選領域：**
- `"love"` - 愛情感情分析
- `"wealth"` - 財富事業分析
- `"future"` - 未來運勢分析
- `"comprehensive"` - 綜合命盤分析

### 選擇輸出格式

```python
# 可選格式：
output_format="json"              # 純 JSON 格式
output_format="narrative"         # 純論述格式
output_format="json_to_narrative" # JSON 分析 + 論述輸出（推薦）
```

### 控制 Agent 過程顯示

```python
show_agent_process=True   # 顯示 Agent 協作過程
show_agent_process=False  # 隱藏過程（適合生產環境）
```

## 🔧 技術架構

### Multi-Agent 協作流程

1. **初始分析階段**: 各 Agent 獨立分析
2. **討論階段**: Agent 間交叉討論和辯論
3. **共識達成**: 整合各方觀點形成最終結果
4. **格式化輸出**: 根據需求格式化最終結果

### RAG 系統架構

1. **文檔處理**: PDF 文檔分塊和預處理
2. **向量化**: 使用 BGE-M3 模型生成嵌入
3. **存儲**: Chroma 向量資料庫持久化存儲
4. **檢索**: 基於查詢的相似度檢索
5. **增強**: 將檢索結果注入到 Agent 分析中

## 📊 系統監控

系統提供詳細的運行監控信息：

- Agent 狀態追蹤
- 處理時間統計
- 協作過程記錄
- 信心度評估
- 共識程度測量

## 🛠️ 開發指南

### 添加新的 Agent

1. 繼承 `BaseAgent` 類
2. 實現必要的方法
3. 在協調器中註冊新 Agent

### 擴展輸出格式

1. 在 `GPT4oFormatter` 中添加新格式方法
2. 更新格式選擇邏輯
3. 添加相應的 Prompt 模板

### 自定義 Prompt

在 `src/prompts/system_prompts.py` 中修改或添加新的 Prompt 模板。

## 📝 更新日誌

### v1.0.0 (2025-07-12)
- ✅ 初始版本發布
- ✅ Multi-Agent 協作系統
- ✅ RAG 知識檢索系統
- ✅ 多種輸出格式支援
- ✅ Agent 過程可視化
- ✅ 完整的資源清理機制

## 📄 授權

本項目採用 MIT 授權條款。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📞 聯繫

如有問題或建議，請通過 GitHub Issues 聯繫。
