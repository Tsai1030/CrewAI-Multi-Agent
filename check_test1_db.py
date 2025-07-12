"""
檢查 test1 向量資料庫的實際狀態
"""

import chromadb
from chromadb.config import Settings

def check_test1_database():
    """檢查 test1 資料庫狀態"""
    try:
        # 連接到 test1 資料庫
        client = chromadb.PersistentClient(
            path='./vector_db_test1',
            settings=Settings(anonymized_telemetry=False)
        )

        # 列出所有集合
        collections = client.list_collections()
        print(f'資料庫中的集合: {[c.name for c in collections]}')

        # 檢查 ziwei_knowledge_test1 集合
        try:
            collection = client.get_collection('ziwei_knowledge_test1')
            count = collection.count()
            print(f'ziwei_knowledge_test1 集合文檔數: {count}')
            
            if count > 0:
                # 獲取一些樣本
                results = collection.get(limit=3)
                docs = results.get('documents', [])
                print(f'樣本文檔數: {len(docs)}')
                for i, doc in enumerate(docs[:2]):
                    print(f'文檔 {i+1}: {doc[:100]}...')
            else:
                print('集合為空')
                
        except Exception as e:
            print(f'獲取集合失敗: {e}')
            
    except Exception as e:
        print(f'連接資料庫失敗: {e}')

if __name__ == "__main__":
    check_test1_database()
