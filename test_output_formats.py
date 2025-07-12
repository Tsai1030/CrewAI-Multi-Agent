"""
測試不同輸出格式
"""

import asyncio
import json
from main import ZiweiAISystem

async def test_output_formats():
    """測試 JSON 和論述兩種輸出格式"""
    print("🌟 測試紫微斗數AI系統輸出格式")
    print("=" * 60)
    
    try:
        # 創建系統
        system = ZiweiAISystem()
        await system.initialize()
        
        print("✅ 系統初始化完成")
        
        # 示例分析數據
        sample_birth_data = {
            "gender": "男",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "birth_hour": "午"
        }
        
        # 測試 JSON 格式
        print("\n" + "="*60)
        print("📊 測試 JSON 格式輸出")
        print("="*60)
        
        json_result = await system.analyze_ziwei_chart(
            birth_data=sample_birth_data,
            domain_type="comprehensive",
            output_format="json"
        )
        
        if json_result['success']:
            print("✅ JSON 格式分析完成")
            print(f"⏱️  處理時間: {json_result['metadata']['processing_time']:.2f} 秒")
            print("\n📋 JSON 格式結果:")
            
            formatted_result = json_result['result']
            if isinstance(formatted_result, str):
                try:
                    parsed_result = json.loads(formatted_result)
                    print(json.dumps(parsed_result, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    print(formatted_result)
            else:
                print(json.dumps(formatted_result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ JSON 格式分析失敗: {json_result['error']}")
        
        # 測試論述格式
        print("\n" + "="*60)
        print("📝 測試論述格式輸出")
        print("="*60)
        
        narrative_result = await system.analyze_ziwei_chart(
            birth_data=sample_birth_data,
            domain_type="comprehensive",
            output_format="narrative"
        )
        
        if narrative_result['success']:
            print("✅ 論述格式分析完成")
            print(f"⏱️  處理時間: {narrative_result['metadata']['processing_time']:.2f} 秒")
            print("\n📖 論述格式結果:")
            print("-" * 60)
            
            formatted_result = narrative_result['result']
            if isinstance(formatted_result, str):
                print(formatted_result)
            else:
                print(json.dumps(formatted_result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 論述格式分析失敗: {narrative_result['error']}")
        
        # 清理系統資源
        await system.cleanup()
        print("\n✅ 系統清理完成")
        
    except Exception as e:
        print(f"❌ 系統運行錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_output_formats())
