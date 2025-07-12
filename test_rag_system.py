"""
RAG 系統測試腳本
測試 BGE-M3 + GPT-4o RAG 系統的各個組件
"""

import os
import sys
import logging
import traceback
from pathlib import Path

# 添加項目根目錄到路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_environment():
    """測試環境配置"""
    print("=== 環境配置測試 ===")
    
    # 檢查環境變數
    required_vars = [
        "OPENAI_API_KEY",
        "EMBEDDING_MODEL", 
        "EMBEDDING_PROVIDER"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {'*' * (len(value) - 10) + value[-10:] if len(value) > 10 else value}")
        else:
            print(f"✗ {var}: 未設置")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"警告: 缺少環境變數 {missing_vars}")
        return False
    
    return True


def test_dependencies():
    """測試依賴包"""
    print("\n=== 依賴包測試 ===")
    
    dependencies = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("tokenizers", "Tokenizers"),
        ("chromadb", "ChromaDB"),
        ("openai", "OpenAI"),
        ("langchain", "LangChain")
    ]
    
    all_available = True
    for package, name in dependencies:
        try:
            __import__(package)
            print(f"✓ {name}: 已安裝")
        except ImportError:
            print(f"✗ {name}: 未安裝")
            all_available = False
    
    return all_available


def test_bge_embeddings():
    """測試 BGE-M3 嵌入模型"""
    print("\n=== BGE-M3 嵌入模型測試 ===")
    
    try:
        from src.rag.bge_embeddings import BGEM3Embeddings
        
        # 創建嵌入模型（使用較小的配置進行測試）
        embeddings = BGEM3Embeddings(
            model_name="BAAI/bge-m3",
            device="cpu",
            max_length=512,  # 較小的長度用於測試
            batch_size=2
        )
        
        # 測試文本嵌入
        test_texts = [
            "紫微星是紫微斗數中的帝王星",
            "天機星代表智慧和變化"
        ]
        
        print("測試文檔嵌入...")
        doc_embeddings = embeddings.embed_documents(test_texts)
        print(f"✓ 文檔嵌入成功，維度: {len(doc_embeddings[0])}")
        
        print("測試查詢嵌入...")
        query_embedding = embeddings.embed_query("什麼是紫微星？")
        print(f"✓ 查詢嵌入成功，維度: {len(query_embedding)}")
        
        # 測試模型信息
        model_info = embeddings.get_model_info()
        print(f"✓ 模型信息: {model_info['model_name']}")
        
        return True
        
    except Exception as e:
        print(f"✗ BGE-M3 測試失敗: {str(e)}")
        traceback.print_exc()
        return False


def test_gpt4o_generator():
    """測試 GPT-4o 生成器"""
    print("\n=== GPT-4o 生成器測試 ===")
    
    try:
        from src.rag.gpt4o_generator import GPT4oGenerator
        
        # 創建生成器
        generator = GPT4oGenerator(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=100  # 較小的 token 數用於測試
        )
        
        # 測試簡單生成
        test_query = "什麼是紫微斗數？"
        test_context = ["紫微斗數是中國古代的一種命理學說"]
        
        print("測試回答生成...")
        response = generator.generate_response(
            query=test_query,
            context_documents=test_context
        )
        
        if "error" not in response:
            print(f"✓ 生成成功")
            print(f"  回答長度: {len(response['answer'])} 字符")
            print(f"  使用 Token: {response.get('usage', {}).get('total_tokens', 'N/A')}")
            return True
        else:
            print(f"✗ 生成失敗: {response['error']}")
            return False
            
    except Exception as e:
        print(f"✗ GPT-4o 測試失敗: {str(e)}")
        traceback.print_exc()
        return False


def test_vector_store():
    """測試向量存儲"""
    print("\n=== 向量存儲測試 ===")
    
    try:
        from src.rag.vector_store import ZiweiVectorStore
        from langchain.schema import Document
        
        # 創建向量存儲（使用測試配置）
        vector_store = ZiweiVectorStore(
            persist_directory="./data/test_vector_db",
            collection_name="test_collection",
            embedding_provider="huggingface",
            embedding_model="BAAI/bge-m3",
            embedding_config={
                "device": "cpu",
                "max_length": 512,
                "batch_size": 2
            }
        )
        
        # 測試文檔添加
        test_docs = [
            Document(
                page_content="紫微星是紫微斗數中最重要的主星之一",
                metadata={"category": "主星", "star": "紫微星"}
            ),
            Document(
                page_content="天機星代表智慧、變化和機敏",
                metadata={"category": "主星", "star": "天機星"}
            )
        ]
        
        print("測試文檔添加...")
        doc_ids = vector_store.add_documents(test_docs)
        print(f"✓ 添加文檔成功，ID: {doc_ids}")
        
        # 測試搜索
        print("測試向量搜索...")
        search_results = vector_store.search("紫微星的特質", top_k=2)
        print(f"✓ 搜索成功，找到 {len(search_results)} 個結果")
        
        # 測試統計信息
        stats = vector_store.get_collection_stats()
        print(f"✓ 統計信息: {stats}")
        
        return True
        
    except Exception as e:
        print(f"✗ 向量存儲測試失敗: {str(e)}")
        traceback.print_exc()
        return False


def test_rag_system():
    """測試完整 RAG 系統"""
    print("\n=== 完整 RAG 系統測試 ===")
    
    try:
        from src.rag.rag_system import create_rag_system
        
        # 創建測試配置
        test_config = {
            "vector_store": {
                "persist_directory": "./data/test_rag_db",
                "collection_name": "test_rag",
                "embedding_provider": "huggingface",
                "embedding_model": "BAAI/bge-m3",
                "embedding_config": {
                    "device": "cpu",
                    "max_length": 512,
                    "batch_size": 2,
                    "openai_fallback": True
                }
            },
            "generator": {
                "model": "gpt-4o",
                "temperature": 0.7,
                "max_tokens": 150
            },
            "rag": {
                "top_k": 3,
                "min_score": 0.5
            }
        }
        
        # 創建 RAG 系統
        print("創建 RAG 系統...")
        rag_system = create_rag_system(test_config)
        
        # 檢查系統狀態
        status = rag_system.get_system_status()
        print(f"✓ 系統狀態: {status['system']}")
        
        # 添加測試知識
        print("添加測試知識...")
        test_knowledge = [
            {
                "content": "紫微星是紫微斗數的主星，代表帝王之星，具有領導能力",
                "metadata": {"star": "紫微星", "type": "主星解析"}
            }
        ]
        
        success = rag_system.add_knowledge(test_knowledge)
        if success:
            print("✓ 知識添加成功")
        else:
            print("✗ 知識添加失敗")
            return False
        
        # 測試問答
        print("測試問答功能...")
        response = rag_system.generate_answer(
            query="紫微星有什麼特質？",
            context_type="auto"
        )
        
        if "error" not in response:
            print("✓ 問答測試成功")
            print(f"  回答: {response['answer'][:100]}...")
            return True
        else:
            print(f"✗ 問答測試失敗: {response['error']}")
            return False
            
    except Exception as e:
        print(f"✗ RAG 系統測試失敗: {str(e)}")
        traceback.print_exc()
        return False


def cleanup_test_data():
    """清理測試數據"""
    print("\n=== 清理測試數據 ===")
    
    import shutil
    test_dirs = [
        "./data/test_vector_db",
        "./data/test_rag_db"
    ]
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            try:
                shutil.rmtree(test_dir)
                print(f"✓ 清理 {test_dir}")
            except Exception as e:
                print(f"✗ 清理 {test_dir} 失敗: {str(e)}")


def main():
    """主測試函數"""
    print("RAG 系統測試")
    print("=" * 50)
    
    # 設置日誌
    logging.basicConfig(level=logging.WARNING)  # 減少日誌輸出
    
    test_results = []
    
    # 運行測試
    tests = [
        ("環境配置", test_environment),
        ("依賴包", test_dependencies),
        ("BGE-M3 嵌入", test_bge_embeddings),
        ("GPT-4o 生成器", test_gpt4o_generator),
        ("向量存儲", test_vector_store),
        ("完整 RAG 系統", test_rag_system)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} 測試異常: {str(e)}")
            test_results.append((test_name, False))
    
    # 清理測試數據
    cleanup_test_data()
    
    # 總結結果
    print("\n" + "=" * 50)
    print("測試結果總結:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n總計: {passed}/{total} 個測試通過")
    
    if passed == total:
        print("🎉 所有測試通過！RAG 系統配置正確。")
        return True
    else:
        print("⚠️  部分測試失敗，請檢查配置和依賴。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
