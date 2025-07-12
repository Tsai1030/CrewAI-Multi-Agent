"""
測試向量資料庫搜索功能
"""

import chromadb
from src.rag.bge_embeddings import BGEM3Embeddings

def test_search(query: str, top_k: int = 3):
    """測試搜索功能"""
    print(f"🔍 搜索查詢: '{query}'")
    print("=" * 50)
    
    try:
        # 載入嵌入模型
        embeddings = BGEM3Embeddings(
            model_name="BAAI/bge-m3",
            device="cpu"
        )
        
        # 連接向量資料庫
        client = chromadb.PersistentClient(path="./vector_db_test1")
        collection = client.get_collection("ziwei_knowledge_test1")
        
        # 生成查詢嵌入
        query_embedding = embeddings.embed_query(query)
        
        # 搜索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # 顯示結果
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        print(f"找到 {len(documents)} 條相關結果:\n")
        
        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
            print(f"📄 結果 {i} (相似度: {1-dist:.4f})")
            print(f"類型: {meta.get('content_type', '未知')}")
            print(f"內容: {doc[:200]}...")
            print("-" * 40)
        
    except Exception as e:
        print(f"搜索失敗: {e}")

if __name__ == "__main__":
    # 測試不同類型的查詢
    test_queries = [
        "紫微星的特質",
        "命宮的意義", 
        "大限運勢",
        "格局分析",
        "排盤方法"
    ]
    
    for query in test_queries:
        test_search(query)
        print("\n" + "="*60 + "\n")
