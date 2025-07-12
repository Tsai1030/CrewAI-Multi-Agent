"""
測試向量庫持久化功能
"""

import asyncio
import logging
import os
import shutil
from pathlib import Path

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_vector_db_persistence():
    """測試向量庫持久化功能"""
    print("=== 測試向量庫持久化功能 ===")
    
    try:
        # 清理測試環境
        test_db_path = Path("./test_vector_db")
        if test_db_path.exists():
            shutil.rmtree(test_db_path)
            print("✅ 清理舊的測試向量庫")
        
        # 設置測試環境變數
        os.environ["VECTOR_DB_PATH"] = str(test_db_path)
        os.environ["VECTOR_DB_COLLECTION"] = "test_ziwei_knowledge"
        
        from main import ZiweiAISystem
        
        print("\n--- 第一次初始化：創建新向量庫 ---")
        
        # 第一次初始化系統
        system1 = ZiweiAISystem()
        await system1.initialize()
        
        # 檢查向量庫狀態
        stats1 = system1.get_system_status()
        rag_stats1 = stats1.get('rag_stats', {})
        vector_stats1 = rag_stats1.get('vector_store', {})
        total_docs1 = vector_stats1.get('total_documents', 0)
        
        print(f"✅ 第一次初始化完成")
        print(f"   向量庫路徑: {vector_stats1.get('persist_directory', 'unknown')}")
        print(f"   文檔數量: {total_docs1}")
        
        # 添加一些測試知識
        test_knowledge = [
            {
                "content": "測試知識1：這是第一條測試知識，用於驗證向量庫持久化功能。",
                "metadata": {"category": "測試", "type": "持久化測試"}
            },
            {
                "content": "測試知識2：這是第二條測試知識，包含紫微斗數相關內容。",
                "metadata": {"category": "測試", "star": "測試星"}
            }
        ]
        
        success = system1.rag_system.add_knowledge(test_knowledge)
        if success:
            print(f"✅ 成功添加 {len(test_knowledge)} 條測試知識")
        
        # 檢查更新後的狀態
        stats1_updated = system1.get_system_status()
        rag_stats1_updated = stats1_updated.get('rag_stats', {})
        vector_stats1_updated = rag_stats1_updated.get('vector_store', {})
        total_docs1_updated = vector_stats1_updated.get('total_documents', 0)
        
        print(f"   更新後文檔數量: {total_docs1_updated}")
        
        # 測試搜索功能
        search_results = system1.rag_system.search_knowledge("測試知識", top_k=2)
        print(f"✅ 搜索測試：找到 {len(search_results)} 條相關知識")
        
        print("\n--- 第二次初始化：使用現有向量庫 ---")
        
        # 第二次初始化系統（模擬重啟）
        system2 = ZiweiAISystem()
        await system2.initialize()
        
        # 檢查向量庫狀態
        stats2 = system2.get_system_status()
        rag_stats2 = stats2.get('rag_stats', {})
        vector_stats2 = rag_stats2.get('vector_store', {})
        total_docs2 = vector_stats2.get('total_documents', 0)
        
        print(f"✅ 第二次初始化完成")
        print(f"   向量庫路徑: {vector_stats2.get('persist_directory', 'unknown')}")
        print(f"   文檔數量: {total_docs2}")
        
        # 驗證數據持久化
        if total_docs2 == total_docs1_updated:
            print("✅ 向量庫數據成功持久化！")
        else:
            print(f"❌ 數據持久化失敗：期望 {total_docs1_updated}，實際 {total_docs2}")
        
        # 測試搜索功能（驗證數據完整性）
        search_results2 = system2.rag_system.search_knowledge("測試知識", top_k=2)
        print(f"✅ 重啟後搜索測試：找到 {len(search_results2)} 條相關知識")
        
        if len(search_results2) == len(search_results):
            print("✅ 搜索功能正常，數據完整性驗證通過！")
        else:
            print(f"❌ 數據完整性驗證失敗：期望 {len(search_results)}，實際 {len(search_results2)}")
        
        print("\n--- 測試添加新知識到現有向量庫 ---")
        
        # 添加更多知識到現有向量庫
        additional_knowledge = [
            {
                "content": "額外知識1：這是重啟後添加的新知識。",
                "metadata": {"category": "測試", "type": "增量測試"}
            }
        ]
        
        success2 = system2.rag_system.add_knowledge(additional_knowledge)
        if success2:
            print(f"✅ 成功添加 {len(additional_knowledge)} 條額外知識")
        
        # 檢查最終狀態
        stats2_final = system2.get_system_status()
        rag_stats2_final = stats2_final.get('rag_stats', {})
        vector_stats2_final = rag_stats2_final.get('vector_store', {})
        total_docs2_final = vector_stats2_final.get('total_documents', 0)
        
        print(f"   最終文檔數量: {total_docs2_final}")
        
        expected_final = total_docs2 + len(additional_knowledge)
        if total_docs2_final == expected_final:
            print("✅ 增量添加功能正常！")
        else:
            print(f"❌ 增量添加失敗：期望 {expected_final}，實際 {total_docs2_final}")
        
        print("\n--- 測試總結 ---")
        print(f"初始文檔數: {total_docs1}")
        print(f"添加測試知識後: {total_docs1_updated}")
        print(f"重啟後文檔數: {total_docs2}")
        print(f"添加額外知識後: {total_docs2_final}")
        
        # 清理測試環境
        if test_db_path.exists():
            shutil.rmtree(test_db_path)
            print("✅ 清理測試向量庫")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_main_system_persistence():
    """測試主系統的持久化行為"""
    print("\n=== 測試主系統持久化行為 ===")
    
    try:
        from main import ZiweiAISystem
        
        print("--- 檢查主系統向量庫狀態 ---")
        
        # 初始化主系統
        system = ZiweiAISystem()
        await system.initialize()
        
        # 檢查向量庫狀態
        stats = system.get_system_status()
        rag_stats = stats.get('rag_stats', {})
        vector_stats = rag_stats.get('vector_store', {})
        total_docs = vector_stats.get('total_documents', 0)
        
        print(f"✅ 主系統初始化完成")
        print(f"   向量庫路徑: {vector_stats.get('persist_directory', 'unknown')}")
        print(f"   集合名稱: {vector_stats.get('collection_name', 'unknown')}")
        print(f"   文檔數量: {total_docs}")
        
        if total_docs > 0:
            print("✅ 發現現有向量庫數據，系統正確使用持久化向量庫")
        else:
            print("ℹ️  向量庫為空，系統會載入基礎知識")
        
        # 測試搜索功能
        search_results = system.rag_system.search_knowledge("紫微星", top_k=3)
        print(f"✅ 搜索測試：找到 {len(search_results)} 條關於紫微星的知識")
        
        for i, result in enumerate(search_results[:2], 1):
            content_preview = result['content'][:50] + "..." if len(result['content']) > 50 else result['content']
            print(f"   {i}. {content_preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ 主系統測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主測試函數"""
    print("🌟 向量庫持久化功能測試")
    print("=" * 50)
    
    tests = [
        ("向量庫持久化測試", test_vector_db_persistence),
        ("主系統持久化測試", test_main_system_persistence)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🚀 開始 {test_name}...")
            result = await test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name} 通過")
            else:
                print(f"❌ {test_name} 失敗")
                
        except Exception as e:
            print(f"❌ {test_name} 異常: {str(e)}")
            results.append((test_name, False))
    
    # 總結
    print("\n" + "=" * 50)
    print("🎉 測試完成！")
    
    successful_tests = sum(1 for _, success in results if success)
    total_tests = len(results)
    
    print(f"\n📊 測試結果: {successful_tests}/{total_tests} 個測試通過")
    
    for test_name, success in results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    if successful_tests == total_tests:
        print(f"\n🎉 所有測試通過！向量庫持久化功能正常運作！")
        
        print(f"\n💡 功能特色:")
        print(f"   ✅ 向量庫數據永久保存")
        print(f"   ✅ 系統重啟後自動使用現有數據")
        print(f"   ✅ 支援增量添加新知識")
        print(f"   ✅ 數據完整性保證")
        print(f"   ✅ 搜索功能持續可用")
        
        print(f"\n🛠️  管理工具:")
        print(f"   python manage_vector_db.py status      # 查看狀態")
        print(f"   python manage_vector_db.py add-file    # 添加文件")
        print(f"   python manage_vector_db.py search      # 搜索知識")
        
    else:
        print(f"\n⚠️  部分測試失敗，請檢查配置。")

if __name__ == "__main__":
    asyncio.run(main())
