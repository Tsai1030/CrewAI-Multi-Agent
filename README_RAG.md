# 紫微斗數 RAG 向量庫系統

基於 Hugging Face BGE-M3 嵌入模型和 GPT-4o 輸出模型的檢索增強生成（RAG）系統，專為紫微斗數知識問答和命盤分析設計。

## 🌟 系統特色

- **🔥 先進的嵌入模型**: 使用 BGE-M3 多語言嵌入模型，支援中文語義理解
- **🤖 強大的生成能力**: 整合 GPT-4o 模型，提供專業的紫微斗數解析
- **📚 智能知識檢索**: ChromaDB 向量資料庫，快速精準的語義搜索
- **🔄 混合模型支持**: 支援 BGE-M3 和 OpenAI 嵌入模型的無縫切換
- **⚡ 高性能優化**: 支援 GPU 加速和批次處理
- **🛠️ 易於使用**: 簡潔的 API 設計，快速上手

## 🏗️ 系統架構

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   用戶查詢      │───▶│   BGE-M3 嵌入    │───▶│   向量搜索      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GPT-4o 回答   │◀───│   上下文整合     │◀───│   檢索結果      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📦 安裝依賴

```bash
# 安裝 Python 依賴
pip install -r requirements.txt

# 或手動安裝關鍵包
pip install transformers torch tokenizers chromadb openai langchain
```

## ⚙️ 環境配置

在 `.env` 文件中設置以下環境變數：

```env
# OpenAI API 設定
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_GPT4O=gpt-4o-mini

# BGE-M3 嵌入模型設定
EMBEDDING_MODEL=BAAI/bge-m3
EMBEDDING_PROVIDER=huggingface
EMBEDDING_DEVICE=cpu
EMBEDDING_MAX_LENGTH=8192
EMBEDDING_BATCH_SIZE=32

# 向量資料庫設定
VECTOR_DB_PATH=./data/vector_db
VECTOR_DB_COLLECTION=ziwei_knowledge
```

## 🚀 快速開始

### 1. 基本使用

```python
from src.rag import create_rag_system

# 創建 RAG 系統
rag_system = create_rag_system()

# 檢查系統狀態
status = rag_system.get_system_status()
print(f"系統狀態: {status['system']}")
```

### 2. 添加知識

```python
# 添加紫微斗數知識
knowledge = [
    {
        "content": "紫微星是紫微斗數中的帝王星，代表領導能力...",
        "metadata": {
            "category": "主星解析",
            "star": "紫微星"
        }
    }
]

rag_system.add_knowledge(knowledge)
```

### 3. 智能問答

```python
# 提問並獲得回答
response = rag_system.generate_answer("紫微星坐命的人有什麼特質？")
print(response['answer'])
```

### 4. 命盤分析

```python
# 分析紫微斗數命盤
chart_data = {
    "main_stars": ["紫微星", "天機星"],
    "palaces": ["命宮", "財帛宮"],
    # ... 更多命盤數據
}

analysis = rag_system.analyze_ziwei_chart(chart_data)
print(analysis['answer'])
```

## 📁 項目結構

```
src/rag/
├── __init__.py              # 模組導入
├── rag_system.py           # 主要 RAG 系統
├── vector_store.py         # 向量存儲實現
├── bge_embeddings.py       # BGE-M3 嵌入模型
├── gpt4o_generator.py      # GPT-4o 生成器
└── ...

examples/
├── rag_demo.py             # 完整演示腳本
└── ...

docs/
├── rag_setup_guide.md      # 詳細設置指南
└── ...

quick_start.py              # 快速開始示例
test_rag_system.py          # 系統測試腳本
```

## 🔧 高級配置

### 自定義嵌入模型

```python
custom_config = {
    "vector_store": {
        "embedding_provider": "huggingface",
        "embedding_model": "BAAI/bge-m3",
        "embedding_config": {
            "device": "cuda",        # 使用 GPU
            "max_length": 8192,
            "batch_size": 64,
            "use_fp16": True,        # 半精度加速
            "openai_fallback": True  # OpenAI 備用
        }
    }
}

rag_system = create_rag_system(custom_config)
```

### 混合嵌入模型

系統支援 BGE-M3 和 OpenAI 嵌入模型的混合使用，當主要模型失敗時自動切換到備用模型。

### 性能優化

- **GPU 加速**: 設置 `device="cuda"` 使用 GPU
- **批次處理**: 調整 `batch_size` 提高吞吐量
- **半精度**: 啟用 `use_fp16=True` 節省內存
- **並行處理**: 支援多線程文檔處理

## 🧪 測試系統

運行完整的系統測試：

```bash
python test_rag_system.py
```

運行快速開始示例：

```bash
python quick_start.py
```

運行完整演示：

```bash
python examples/rag_demo.py
```

## 📊 性能指標

| 組件 | 性能指標 |
|------|----------|
| BGE-M3 嵌入 | ~1024 維向量，支援 8192 token |
| 向量搜索 | 毫秒級響應，支援百萬級文檔 |
| GPT-4o 生成 | 高質量回答，支援長上下文 |
| 整體延遲 | 通常 2-5 秒（包含檢索和生成） |

## 🔍 故障排除

### 常見問題

1. **BGE-M3 模型下載失敗**
   ```bash
   huggingface-cli download BAAI/bge-m3
   ```

2. **CUDA 內存不足**
   ```python
   # 使用 CPU 或減少批次大小
   config = {"embedding_config": {"device": "cpu", "batch_size": 8}}
   ```

3. **OpenAI API 調用失敗**
   - 檢查 API 密鑰設置
   - 確認網絡連接
   - 檢查 API 配額

### 調試模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 創建系統時會輸出詳細日誌
rag_system = create_rag_system()
```

## 📚 文檔和示例

- [詳細設置指南](docs/rag_setup_guide.md)
- [完整演示腳本](examples/rag_demo.py)
- [快速開始示例](quick_start.py)
- [系統測試腳本](test_rag_system.py)

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 項目
2. 創建功能分支
3. 提交更改
4. 發起 Pull Request

## 📄 許可證

本項目採用 MIT 許可證。

## 🙏 致謝

- [BGE-M3](https://huggingface.co/BAAI/bge-m3) - 優秀的多語言嵌入模型
- [OpenAI GPT-4o](https://openai.com/) - 強大的語言生成模型
- [ChromaDB](https://www.trychroma.com/) - 高效的向量資料庫
- [LangChain](https://langchain.com/) - 便捷的 LLM 應用框架

---

**開始使用**: `python quick_start.py`

**完整測試**: `python test_rag_system.py`

**詳細演示**: `python examples/rag_demo.py`
