"""
RAG 系統快速開始示例
使用 BGE-M3 + GPT-4o 的紫微斗數 RAG 系統
"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def main():
    """快速開始示例"""
    print("🌟 紫微斗數 RAG 系統快速開始")
    print("使用 BGE-M3 嵌入模型 + GPT-4o 輸出模型")
    print("=" * 60)
    
    try:
        # 1. 導入 RAG 系統
        from src.rag import create_rag_system
        
        print("📦 正在初始化 RAG 系統...")
        
        # 2. 創建 RAG 系統
        rag_system = create_rag_system()
        
        # 3. 檢查系統狀態
        status = rag_system.get_system_status()
        print(f"✅ 系統狀態: {status['system']}")
        print(f"📊 向量存儲: {status['components']['vector_store']}")
        print(f"🤖 生成器: {status['components']['generator']}")
        
        # 4. 添加示例知識
        print("\n📚 添加紫微斗數知識...")
        
        sample_knowledge = [
            {
                "content": """紫微星是紫微斗數中的帝王星，位於北斗七星的中央。
                紫微星坐命的人具有以下特質：
                1. 天生的領導能力和權威感
                2. 喜歡掌控全局，有統御才能
                3. 責任感強，有使命感
                4. 容易得到他人的尊重和信任
                5. 適合從事管理、領導或公職工作
                6. 性格較為穩重，不輕易改變決定""",
                "metadata": {
                    "category": "主星解析",
                    "star": "紫微星",
                    "palace": "命宮"
                }
            },
            {
                "content": """天機星是智慧之星，代表聰明才智和變化。
                天機星的特質包括：
                1. 思維敏捷，反應快速
                2. 善於分析和推理
                3. 喜歡學習新知識，求知慾強
                4. 適應能力強，能應對變化
                5. 有創新思維和發明才能
                6. 容易心思不定，想法多變
                7. 適合從事技術、研究或顧問工作""",
                "metadata": {
                    "category": "主星解析", 
                    "star": "天機星",
                    "palace": "命宮"
                }
            },
            {
                "content": """太陽星代表光明、熱情和奉獻精神。
                太陽星坐命的人特點：
                1. 性格開朗，熱情大方
                2. 樂於助人，有奉獻精神
                3. 具有正義感和責任心
                4. 喜歡成為眾人焦點
                5. 適合公職或服務性行業
                6. 容易操勞過度，需注意休息
                7. 男命較女命更為有利""",
                "metadata": {
                    "category": "主星解析",
                    "star": "太陽星", 
                    "palace": "命宮"
                }
            }
        ]
        
        success = rag_system.add_knowledge(sample_knowledge)
        if success:
            print(f"✅ 成功添加 {len(sample_knowledge)} 條知識")
        else:
            print("❌ 添加知識失敗")
            return
        
        # 5. 測試知識搜索
        print("\n🔍 測試知識搜索...")
        
        search_queries = [
            "紫微星的特質",
            "智慧星曜",
            "領導能力"
        ]
        
        for query in search_queries:
            print(f"\n查詢: {query}")
            results = rag_system.search_knowledge(query, top_k=2, min_score=0.5)
            
            for i, result in enumerate(results, 1):
                print(f"  結果 {i} (相似度: {result['score']:.3f}):")
                print(f"    {result['content'][:80]}...")
        
        # 6. 測試問答功能
        print("\n💬 測試問答功能...")
        
        questions = [
            "紫微星坐命的人有什麼特質？",
            "天機星代表什麼意思？",
            "太陽星的人適合什麼工作？"
        ]
        
        for question in questions:
            print(f"\n❓ 問題: {question}")
            print("-" * 50)
            
            response = rag_system.generate_answer(
                query=question,
                context_type="auto"
            )
            
            if "error" not in response:
                print(f"🤖 回答: {response['answer']}")
                
                if 'retrieval_info' in response:
                    retrieval = response['retrieval_info']
                    print(f"📊 檢索到 {retrieval['relevant_docs']} 條相關文檔")
                
                if 'usage' in response:
                    usage = response['usage']
                    print(f"🔢 Token 使用: {usage['total_tokens']}")
            else:
                print(f"❌ 錯誤: {response['error']}")
        
        # 7. 測試紫微斗數分析
        print("\n🔮 測試紫微斗數分析...")
        
        chart_data = {
            "main_stars": ["紫微星", "天機星"],
            "palaces": ["命宮", "財帛宮", "事業宮"],
            "birth_info": {
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 14
            },
            "palace_details": {
                "命宮": {
                    "main_star": "紫微星",
                    "secondary_stars": ["左輔", "右弼"]
                },
                "財帛宮": {
                    "main_star": "天機星",
                    "secondary_stars": ["文昌", "文曲"]
                }
            }
        }
        
        print("分析命盤...")
        analysis = rag_system.analyze_ziwei_chart(
            chart_data=chart_data,
            analysis_type="comprehensive"
        )
        
        if "error" not in analysis:
            print("🔮 分析結果:")
            print("-" * 50)
            print(analysis['answer'])
        else:
            print(f"❌ 分析錯誤: {analysis['error']}")
        
        # 8. 顯示系統統計
        print("\n📈 系統統計信息...")
        final_status = rag_system.get_system_status()
        
        if 'vector_store_stats' in final_status:
            stats = final_status['vector_store_stats']
            print(f"📚 向量庫文檔數量: {stats.get('total_documents', 'N/A')}")
        
        if 'generator_info' in final_status:
            gen_info = final_status['generator_info']
            print(f"🤖 生成模型: {gen_info.get('model', 'N/A')}")
        
        print("\n🎉 快速開始示例完成！")
        print("您可以繼續添加更多知識或提出其他問題。")
        
    except ImportError as e:
        print(f"❌ 導入錯誤: {str(e)}")
        print("請確保已安裝所有依賴包：pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ 運行錯誤: {str(e)}")
        print("請檢查環境配置和 API 密鑰設置")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
