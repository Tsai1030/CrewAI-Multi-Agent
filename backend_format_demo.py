"""
後端格式選擇演示
"""

import asyncio
from main import ZiweiAISystem

async def demo_backend_choices():
    """演示後端的各種選擇"""
    print("🌟 後端格式選擇演示")
    print("=" * 60)
    
    sample_birth_data = {
        "gender": "男",
        "birth_year": 1990,
        "birth_month": 5,
        "birth_day": 15,
        "birth_hour": "午"
    }
    
    try:
        system = ZiweiAISystem()
        await system.initialize()
        print("✅ 系統初始化完成\n")
        
        # 演示1：不同領域的選擇
        print("📊 演示1：不同領域 Prompt 的選擇")
        print("-" * 40)
        
        domains = {
            "love": "愛情感情分析",
            "wealth": "財富事業分析", 
            "future": "未來運勢分析",
            "comprehensive": "綜合命盤分析"
        }
        
        for domain_key, domain_name in domains.items():
            print(f"\n🎯 {domain_name} (domain_type='{domain_key}')")
            print("   使用的 Prompt：")
            if domain_key == "love":
                print("   - 專精於愛情感情分析的紫微斗數命理老師")
                print("   - 分析夫妻宮、桃花星、感情格局")
            elif domain_key == "wealth":
                print("   - 專精於財富事業分析的紫微斗數命理老師")
                print("   - 分析財帛宮、事業宮、財星組合")
            elif domain_key == "future":
                print("   - 專精於未來運勢預測的紫微斗數命理老師")
                print("   - 分析大限流年、人生轉折點")
            else:
                print("   - 綜合性的紫微斗數命理老師")
                print("   - 全面分析命盤格局")
        
        # 演示2：不同輸出格式的選擇
        print("\n\n📝 演示2：輸出格式的選擇")
        print("-" * 40)
        
        formats = {
            "json": "純 JSON 結構化格式",
            "narrative": "純論述格式",
            "json_to_narrative": "JSON Prompt + 論述輸出（推薦）"
        }
        
        for format_key, format_desc in formats.items():
            print(f"\n🎯 {format_desc} (output_format='{format_key}')")
            if format_key == "json":
                print("   - 使用結構化 JSON prompt")
                print("   - 輸出結構化 JSON 數據")
            elif format_key == "narrative":
                print("   - 使用論述型 prompt")
                print("   - 輸出自然語言論述")
            else:
                print("   - 使用結構化 JSON prompt（精確分析）")
                print("   - 輸出自然語言論述（易讀）")
                print("   - 🌟 最佳選擇：兼具精確性和可讀性")
        
        # 演示3：實際代碼示例
        print("\n\n💻 演示3：後端代碼選擇位置")
        print("-" * 40)
        
        print("""
在 main.py 中的選擇位置：

result = await system.analyze_ziwei_chart(
    birth_data=sample_birth_data,
    domain_type="love",              # 🎯 選擇領域
    output_format="json_to_narrative" # 🎯 選擇輸出格式
)

可選的 domain_type：
- "love"         → 愛情感情分析
- "wealth"       → 財富事業分析  
- "future"       → 未來運勢分析
- "comprehensive" → 綜合命盤分析

可選的 output_format：
- "json"              → 純 JSON 格式
- "narrative"         → 純論述格式
- "json_to_narrative" → JSON Prompt + 論述輸出（推薦）
        """)
        
        # 演示4：實際測試一個
        print("\n📋 演示4：實際測試 - 愛情領域 + JSON轉論述")
        print("-" * 40)
        
        result = await system.analyze_ziwei_chart(
            birth_data=sample_birth_data,
            domain_type="love",  # 使用愛情領域的 prompt
            output_format="json_to_narrative"  # JSON prompt 但論述輸出
        )
        
        if result['success']:
            print("✅ 分析完成")
            print(f"⏱️  處理時間: {result['metadata']['processing_time']:.2f} 秒")
            print("\n📖 愛情運勢分析結果（論述格式）:")
            print("-" * 50)
            print(result['result'])
        else:
            print(f"❌ 分析失敗: {result['error']}")
        
        await system.cleanup()
        print("\n✅ 演示完成")
        
    except Exception as e:
        print(f"❌ 演示失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_backend_choices())
