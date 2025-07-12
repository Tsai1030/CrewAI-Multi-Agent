"""
RAG 系統演示腳本
展示如何使用 BGE-M3 + GPT-4o 的 RAG 系統
"""

import os
import sys
import json
import logging
from pathlib import Path

# 添加項目根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.rag.rag_system import ZiweiRAGSystem, create_rag_system


def setup_logging():
    """設置日誌"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def demo_basic_usage():
    """演示基本用法"""
    print("=== RAG 系統基本用法演示 ===")
    
    # 創建 RAG 系統
    rag_system = create_rag_system()
    
    # 檢查系統狀態
    status = rag_system.get_system_status()
    print(f"系統狀態: {status['system']}")
    print(f"向量存儲: {status['components']['vector_store']}")
    print(f"生成器: {status['components']['generator']}")
    
    return rag_system


def demo_add_knowledge(rag_system):
    """演示添加知識"""
    print("\n=== 添加知識演示 ===")
    
    # 示例紫微斗數知識
    sample_knowledge = [
        {
            "content": """紫微星是紫微斗數中的帝王星，代表領導能力和權威。
            紫微星坐命的人通常具有以下特質：
            1. 天生的領導才能
            2. 喜歡掌控全局
            3. 有責任感和使命感
            4. 容易得到他人的尊重
            5. 適合從事管理或領導工作""",
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
            3. 喜歡學習新知識
            4. 適應能力強
            5. 容易心思不定""",
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
            3. 具有正義感
            4. 適合公職或服務業
            5. 容易操勞過度""",
            "metadata": {
                "category": "主星解析",
                "star": "太陽星",
                "palace": "命宮"
            }
        }
    ]
    
    # 添加知識
    success = rag_system.add_knowledge(sample_knowledge)
    if success:
        print(f"成功添加 {len(sample_knowledge)} 條知識")
    else:
        print("添加知識失敗")
    
    # 檢查向量存儲統計
    stats = rag_system.vector_store.get_collection_stats()
    print(f"向量庫統計: {stats}")


def demo_search_knowledge(rag_system):
    """演示知識搜索"""
    print("\n=== 知識搜索演示 ===")
    
    # 搜索查詢
    queries = [
        "紫微星的特質",
        "領導能力",
        "智慧星曜",
        "太陽星性格"
    ]
    
    for query in queries:
        print(f"\n查詢: {query}")
        results = rag_system.search_knowledge(query, top_k=3, min_score=0.5)
        
        for i, result in enumerate(results, 1):
            print(f"  結果 {i} (相似度: {result['score']:.3f}):")
            print(f"    {result['content'][:100]}...")
            if result['metadata']:
                print(f"    元數據: {result['metadata']}")


def demo_generate_answers(rag_system):
    """演示回答生成"""
    print("\n=== 回答生成演示 ===")
    
    # 測試問題
    questions = [
        "紫微星坐命的人有什麼特質？",
        "天機星代表什麼意思？",
        "太陽星的人適合什麼工作？",
        "如何判斷一個人的領導能力？"
    ]
    
    for question in questions:
        print(f"\n問題: {question}")
        print("-" * 50)
        
        # 生成回答
        response = rag_system.generate_answer(
            query=question,
            context_type="auto",
            temperature=0.7
        )
        
        print(f"回答: {response['answer']}")
        
        if 'retrieval_info' in response:
            retrieval = response['retrieval_info']
            print(f"檢索信息: 找到 {retrieval['relevant_docs']} 條相關文檔")
        
        if 'usage' in response:
            usage = response['usage']
            print(f"Token 使用: {usage['total_tokens']} (輸入: {usage['prompt_tokens']}, 輸出: {usage['completion_tokens']})")


def demo_ziwei_analysis(rag_system):
    """演示紫微斗數分析"""
    print("\n=== 紫微斗數分析演示 ===")
    
    # 示例命盤數據
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
                "secondary_stars": ["左輔", "右弼"],
                "four_modernizations": []
            },
            "財帛宮": {
                "main_star": "天機星",
                "secondary_stars": ["文昌", "文曲"],
                "four_modernizations": []
            }
        }
    }
    
    print("分析命盤數據:")
    print(json.dumps(chart_data, ensure_ascii=False, indent=2))
    
    # 生成分析
    analysis = rag_system.analyze_ziwei_chart(
        chart_data=chart_data,
        analysis_type="comprehensive"
    )
    
    print("\n分析結果:")
    print("-" * 50)
    print(analysis['answer'])
    
    if 'usage' in analysis:
        usage = analysis['usage']
        print(f"\nToken 使用: {usage['total_tokens']}")


def demo_system_configuration():
    """演示系統配置"""
    print("\n=== 系統配置演示 ===")
    
    # 自定義配置
    custom_config = {
        "vector_store": {
            "persist_directory": "./data/custom_vector_db",
            "collection_name": "custom_ziwei",
            "embedding_provider": "huggingface",
            "embedding_model": "BAAI/bge-m3",
            "embedding_config": {
                "device": "cpu",
                "max_length": 4096,
                "batch_size": 16,
                "use_fp16": False,
                "openai_fallback": True
            }
        },
        "generator": {
            "model": "gpt-4o",
            "temperature": 0.8,
            "max_tokens": 1500
        },
        "rag": {
            "top_k": 3,
            "min_score": 0.8
        }
    }
    
    print("自定義配置:")
    print(json.dumps(custom_config, ensure_ascii=False, indent=2))
    
    # 使用自定義配置創建系統
    custom_rag = create_rag_system(custom_config)
    
    # 檢查狀態
    status = custom_rag.get_system_status()
    print(f"\n自定義系統狀態: {status['system']}")
    print(f"配置: {status['config']['rag']}")


def main():
    """主函數"""
    setup_logging()
    
    print("紫微斗數 RAG 系統演示")
    print("使用 BGE-M3 嵌入模型 + GPT-4o 輸出模型")
    print("=" * 60)
    
    try:
        # 基本用法演示
        rag_system = demo_basic_usage()
        
        # 添加知識演示
        demo_add_knowledge(rag_system)
        
        # 搜索知識演示
        demo_search_knowledge(rag_system)
        
        # 生成回答演示
        demo_generate_answers(rag_system)
        
        # 紫微斗數分析演示
        demo_ziwei_analysis(rag_system)
        
        # 系統配置演示
        demo_system_configuration()
        
        print("\n演示完成！")
        
    except Exception as e:
        print(f"演示過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
