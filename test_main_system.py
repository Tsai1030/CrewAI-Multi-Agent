"""
測試主程式系統
驗證 main.py 的完整功能
"""

import asyncio
import logging
import json
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO)

async def test_system_initialization():
    """測試系統初始化"""
    print("=== 測試系統初始化 ===")
    
    try:
        from main import ZiweiAISystem
        
        # 創建系統實例
        system = ZiweiAISystem()
        
        # 測試初始化
        await system.initialize()
        
        # 檢查狀態
        status = system.get_system_status()
        
        print(f"✅ 系統初始化成功")
        print(f"⏱️  初始化時間: {status['initialization_time']:.2f} 秒")
        print(f"📊 組件狀態:")
        for component, status_val in status['components'].items():
            print(f"  - {component}: {'✅' if status_val else '❌'}")
        
        return system
        
    except Exception as e:
        print(f"❌ 系統初始化失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_individual_components(system):
    """測試各個組件"""
    print("\n=== 測試各個組件 ===")
    
    # 測試紫微斗數工具
    print("\n1. 測試紫微斗數工具...")
    try:
        test_birth_data = {
            "gender": "男",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "birth_hour": "午"
        }
        
        chart_result = system.ziwei_tool.get_ziwei_chart(test_birth_data)
        if chart_result.get('success'):
            print("✅ 紫微斗數工具正常")
        else:
            print(f"⚠️  紫微斗數工具警告: {chart_result.get('error', '未知錯誤')}")
    except Exception as e:
        print(f"❌ 紫微斗數工具錯誤: {str(e)}")
    
    # 測試 RAG 系統
    print("\n2. 測試 RAG 系統...")
    try:
        rag_status = system.rag_system.get_system_status()
        print(f"✅ RAG 系統狀態: {rag_status['system']}")
        
        # 測試知識搜索
        search_results = system.rag_system.search_knowledge("紫微星", top_k=2)
        print(f"✅ 知識搜索結果: {len(search_results)} 條")
        
    except Exception as e:
        print(f"❌ RAG 系統錯誤: {str(e)}")
    
    # 測試 Multi-Agent 協調器
    print("\n3. 測試 Multi-Agent 協調器...")
    try:
        if system.coordinator and system.coordinator.agents:
            print(f"✅ 協調器已初始化，包含 {len(system.coordinator.agents)} 個 Agent")
            for agent_id in system.coordinator.agents.keys():
                print(f"  - {agent_id}")
        else:
            print("⚠️  協調器未正確初始化")
    except Exception as e:
        print(f"❌ 協調器錯誤: {str(e)}")

async def test_simple_analysis(system):
    """測試簡單分析流程"""
    print("\n=== 測試簡單分析流程 ===")
    
    try:
        # 準備測試數據
        birth_data = {
            "gender": "女",
            "birth_year": 1995,
            "birth_month": 8,
            "birth_day": 20,
            "birth_hour": "申"
        }
        
        print(f"測試數據: {birth_data}")
        
        # 執行分析
        print("開始執行分析...")
        result = await system.analyze_ziwei_chart(
            birth_data=birth_data,
            domain_type="comprehensive"
        )
        
        if result['success']:
            print("✅ 分析成功完成")
            print(f"⏱️  處理時間: {result['metadata']['processing_time']:.2f} 秒")
            
            # 顯示結果摘要
            formatted_result = result['result']
            if isinstance(formatted_result, dict):
                print(f"📊 分析類型: {formatted_result.get('analysis_type', 'N/A')}")
                print(f"🎯 整體評分: {formatted_result.get('overall_rating', 'N/A')}")
                
                # 顯示部分分析內容
                analysis = formatted_result.get('detailed_analysis', '')
                if analysis:
                    print(f"📝 分析摘要: {analysis[:200]}...")
            
            return True
        else:
            print(f"❌ 分析失敗: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ 分析過程錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_different_domains(system):
    """測試不同領域分析"""
    print("\n=== 測試不同領域分析 ===")
    
    birth_data = {
        "gender": "男",
        "birth_year": 1988,
        "birth_month": 12,
        "birth_day": 25,
        "birth_hour": "子"
    }
    
    domains = ["love", "wealth", "future"]
    
    for domain in domains:
        print(f"\n測試 {domain} 領域分析...")
        try:
            result = await system.analyze_ziwei_chart(
                birth_data=birth_data,
                domain_type=domain
            )
            
            if result['success']:
                processing_time = result['metadata']['processing_time']
                print(f"✅ {domain} 分析成功 (耗時: {processing_time:.2f}s)")
            else:
                print(f"❌ {domain} 分析失敗: {result['error']}")
                
        except Exception as e:
            print(f"❌ {domain} 分析錯誤: {str(e)}")

async def test_knowledge_retrieval(system):
    """測試知識檢索功能"""
    print("\n=== 測試知識檢索功能 ===")
    
    test_queries = [
        "紫微星的特質",
        "天機星代表什麼",
        "太陽星的性格",
        "命宮主星分析",
        "財帛宮的意義"
    ]
    
    for query in test_queries:
        try:
            results = system.rag_system.search_knowledge(query, top_k=2, min_score=0.5)
            print(f"查詢 '{query}': 找到 {len(results)} 條結果")
            
            for i, result in enumerate(results, 1):
                score = result.get('score', 0)
                content = result.get('content', '')[:100]
                print(f"  {i}. (相似度: {score:.3f}) {content}...")
                
        except Exception as e:
            print(f"❌ 查詢 '{query}' 失敗: {str(e)}")

async def test_error_handling(system):
    """測試錯誤處理"""
    print("\n=== 測試錯誤處理 ===")
    
    # 測試無效輸入
    print("1. 測試無效出生數據...")
    try:
        invalid_data = {
            "gender": "無效",
            "birth_year": 1800,  # 過早的年份
            "birth_month": 13,   # 無效月份
            "birth_day": 32,     # 無效日期
            "birth_hour": "無效時辰"
        }
        
        result = await system.analyze_ziwei_chart(invalid_data)
        if not result['success']:
            print("✅ 正確處理了無效輸入")
        else:
            print("⚠️  系統未正確驗證輸入")
            
    except Exception as e:
        print(f"✅ 正確拋出異常: {str(e)}")

async def main():
    """主測試函數"""
    print("🌟 紫微斗數AI系統 - 主程式測試")
    print(f"測試時間: {datetime.now()}")
    print("=" * 60)
    
    # 1. 測試系統初始化
    system = await test_system_initialization()
    
    if not system:
        print("❌ 系統初始化失敗，終止測試")
        return
    
    # 2. 測試各個組件
    await test_individual_components(system)
    
    # 3. 測試簡單分析
    analysis_success = await test_simple_analysis(system)
    
    if analysis_success:
        # 4. 測試不同領域
        await test_different_domains(system)
        
        # 5. 測試知識檢索
        await test_knowledge_retrieval(system)
    
    # 6. 測試錯誤處理
    await test_error_handling(system)
    
    # 總結
    print("\n" + "=" * 60)
    print("🎉 測試完成！")
    
    final_status = system.get_system_status()
    print(f"📊 最終系統狀態:")
    print(f"  - 初始化: {'✅' if final_status['initialized'] else '❌'}")
    print(f"  - 組件數量: {sum(1 for v in final_status['components'].values() if v)}/4")
    
    if final_status['rag_stats']:
        rag_stats = final_status['rag_stats']
        if 'vector_store_stats' in rag_stats:
            doc_count = rag_stats['vector_store_stats'].get('total_documents', 0)
            print(f"  - 知識庫文檔: {doc_count} 條")
    
    print("\n📋 測試建議:")
    if analysis_success:
        print("✅ 系統基本功能正常，可以進行生產環境部署")
        print("🔧 建議下一步:")
        print("  1. 添加更多紫微斗數知識到 RAG 系統")
        print("  2. 優化 Agent 協作策略")
        print("  3. 開發 Web 前端界面")
        print("  4. 設置監控和日誌系統")
    else:
        print("⚠️  系統存在問題，需要進一步調試")
        print("🔧 建議檢查:")
        print("  1. API 密鑰配置")
        print("  2. 網絡連接")
        print("  3. 依賴包版本")
        print("  4. 環境變數設置")

if __name__ == "__main__":
    asyncio.run(main())
