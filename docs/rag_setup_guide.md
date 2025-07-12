# RAG 向量庫設置指南

本指南將幫助您設置使用 Hugging Face BGE-M3 嵌入模型和 GPT-4o 輸出模型的 RAG 向量庫系統。

## 系統架構

```
RAG 系統架構:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   用戶查詢      │───▶│   BGE-M3 嵌入    │───▶│   向量搜索      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GPT-4o 回答   │◀───│   上下文整合     │◀───│   檢索結果      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 安裝依賴

### 1. 安裝 Python 包

```bash
# 安裝基礎依賴
pip install -r requirements.txt

# 或者手動安裝關鍵包
pip install transformers torch tokenizers chromadb openai langchain
```

### 2. 檢查 GPU 支持（可選）

```python
import torch
print(f"CUDA 可用: {torch.cuda.is_available()}")
print(f"CUDA 設備數量: {torch.cuda.device_count()}")
```

## 環境配置

### 1. 設置環境變數

在 `.env` 文件中配置以下變數：

```env
# OpenAI API 設定（用於 GPT-4o）
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_GPT4O=gpt-4o

# BGE-M3 嵌入模型設定
EMBEDDING_MODEL=BAAI/bge-m3
EMBEDDING_PROVIDER=huggingface
EMBEDDING_DEVICE=cpu
EMBEDDING_MAX_LENGTH=8192
EMBEDDING_BATCH_SIZE=32

# 向量資料庫設定
VECTOR_DB_TYPE=chromadb
VECTOR_DB_PATH=./data/vector_db
VECTOR_DB_COLLECTION=ziwei_knowledge

# RAG 系統設定
RAG_TOP_K=5
RAG_MIN_SCORE=0.7
```

### 2. 創建數據目錄

```bash
mkdir -p data/vector_db
mkdir -p logs
```

## 快速開始

### 1. 基本使用

```python
from src.rag.rag_system import create_rag_system

# 創建 RAG 系統
rag_system = create_rag_system()

# 檢查系統狀態
status = rag_system.get_system_status()
print(f"系統狀態: {status['system']}")
```

### 2. 添加知識

```python
# 添加單個文檔
knowledge = [
    {
        "content": "紫微星是紫微斗數中的帝王星...",
        "metadata": {
            "category": "主星解析",
            "star": "紫微星"
        }
    }
]

rag_system.add_knowledge(knowledge)
```

### 3. 搜索和問答

```python
# 搜索知識
results = rag_system.search_knowledge("紫微星的特質", top_k=3)

# 生成回答
response = rag_system.generate_answer("紫微星坐命的人有什麼特質？")
print(response['answer'])
```

## 高級配置

### 1. 自定義嵌入模型配置

```python
custom_config = {
    "vector_store": {
        "embedding_provider": "huggingface",
        "embedding_model": "BAAI/bge-m3",
        "embedding_config": {
            "device": "cuda",  # 使用 GPU
            "max_length": 8192,
            "batch_size": 64,
            "use_fp16": True,  # 使用半精度
            "openai_fallback": True  # 啟用 OpenAI 備用
        }
    }
}

rag_system = create_rag_system(custom_config)
```

### 2. 混合嵌入模型

系統支持 BGE-M3 和 OpenAI 嵌入模型的混合使用：

```python
# 主要使用 BGE-M3，OpenAI 作為備用
config = {
    "vector_store": {
        "embedding_provider": "huggingface",
        "embedding_config": {
            "openai_fallback": True,
            "openai_model": "text-embedding-ada-002"
        }
    }
}
```

### 3. GPT-4o 生成器配置

```python
generator_config = {
    "generator": {
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.9
    }
}
```

## 性能優化

### 1. 嵌入模型優化

- **使用 GPU**: 設置 `device="cuda"` 可顯著提升嵌入速度
- **批次處理**: 增加 `batch_size` 可提高吞吐量
- **半精度**: 啟用 `use_fp16=True` 可節省內存

### 2. 向量搜索優化

- **調整 top_k**: 根據需要調整檢索文檔數量
- **設置 min_score**: 過濾低相關性文檔
- **使用元數據過濾**: 縮小搜索範圍

### 3. 內存管理

```python
# 對於大量文檔，使用較小的批次大小
config = {
    "vector_store": {
        "embedding_config": {
            "batch_size": 16,  # 減少批次大小
            "max_length": 4096  # 減少最大長度
        }
    }
}
```

## 故障排除

### 1. 常見問題

**問題**: BGE-M3 模型下載失敗
```bash
# 解決方案：手動下載模型
huggingface-cli download BAAI/bge-m3
```

**問題**: CUDA 內存不足
```python
# 解決方案：使用 CPU 或減少批次大小
config = {
    "embedding_config": {
        "device": "cpu",
        "batch_size": 8
    }
}
```

**問題**: OpenAI API 調用失敗
```python
# 解決方案：檢查 API 密鑰和網絡連接
import openai
client = openai.OpenAI(api_key="your_key")
# 測試連接
```

### 2. 日誌調試

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 創建系統時會輸出詳細日誌
rag_system = create_rag_system()
```

### 3. 性能監控

```python
# 檢查系統狀態
status = rag_system.get_system_status()
print(f"向量庫文檔數量: {status['vector_store_stats']['total_documents']}")

# 檢查嵌入模型信息
if hasattr(rag_system.vector_store.embeddings, 'get_model_info'):
    model_info = rag_system.vector_store.embeddings.get_model_info()
    print(f"嵌入模型: {model_info}")
```

## 最佳實踐

### 1. 文檔預處理

- 清理文本格式
- 分割長文檔
- 添加有意義的元數據

### 2. 知識庫管理

- 定期更新知識庫
- 使用版本控制
- 備份向量數據

### 3. 查詢優化

- 使用具體的查詢詞
- 結合關鍵詞和語義搜索
- 根據結果調整參數

## 示例代碼

完整的示例代碼請參考 `examples/rag_demo.py`：

```bash
python examples/rag_demo.py
```

這個示例展示了：
- 系統初始化
- 知識添加
- 搜索和問答
- 紫微斗數分析
- 自定義配置

## 支持和反饋

如果您遇到問題或有改進建議，請：

1. 檢查日誌輸出
2. 參考故障排除部分
3. 查看示例代碼
4. 提交問題報告
