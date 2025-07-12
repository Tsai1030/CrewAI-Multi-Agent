"""
測試修復後的系統
"""

import asyncio
import json
from main import ZiweiAISystem

async def test_fixed_system():
    """測試修復後的系統"""
    print("🌟 測試修復後的紫微斗數AI系統")
    print("=" * 50)
    
    try:
        # 創建系統
        system = ZiweiAISystem()
        await system.initialize()
        
        print("✅ 系統初始化完成")
        
        # 示例分析
        print("\n📊 執行示例分析...")
        
        sample_birth_data = {
            "gender": "男",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "birth_hour": "午"
        }
        
        result = await system.analyze_ziwei_chart(
            birth_data=sample_birth_data,
            domain_type="comprehensive"
        )
        
        if result['success']:
            print("✅ 分析完成")
            print(f"⏱️  處理時間: {result['metadata']['processing_time']:.2f} 秒")
            print("\n📋 分析結果:")
            
            # 檢查 result['result'] 是否為 JSON 字符串
            formatted_result = result['result']
            if isinstance(formatted_result, str):
                try:
                    # 嘗試解析 JSON 字符串
                    parsed_result = json.loads(formatted_result)
                    print(json.dumps(parsed_result, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    # 如果不是有效的 JSON，直接顯示字符串
                    print(formatted_result)
            else:
                # 如果已經是字典或其他對象，直接序列化
                print(json.dumps(formatted_result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 分析失敗: {result['error']}")
        
        # 清理系統資源
        await system.cleanup()
        print("✅ 系統清理完成")
        
    except Exception as e:
        print(f"❌ 系統運行錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fixed_system())
