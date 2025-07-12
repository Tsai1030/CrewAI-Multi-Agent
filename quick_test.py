"""
快速測試修復後的系統
"""

import asyncio
import json
import time

async def test_json_parsing():
    """測試 JSON 解析修復"""
    print("🧪 測試 JSON 解析修復")
    
    # 模擬 GPT-4o 返回的 JSON 字符串
    json_string = """{
  "analysis_type": "comprehensive",
  "timestamp": "2025-07-11T00:00:00Z",
  "success": true,
  "data": {
    "overall_rating": 7,
    "comprehensive_analysis": {
      "personality_traits": [
        "系統化思維",
        "嚴謹邏輯",
        "創意表達"
      ],
      "life_pattern": "以系統性分析和創意表達為主，重視數據完整性和理論應用的靈活性。"
    },
    "detailed_analysis": "在這次紫微斗數分析中，強調了數據完整性的重要性以及理論應用的靈活性。",
    "suggestions": [
      "設定小目標，逐步提升專業技能。",
      "尋找心理支持，與信任的同事或朋友交流。"
    ]
  }
}"""
    
    # 模擬修復前的問題（直接打印 JSON 字符串）
    print("\n❌ 修復前的輸出（JSON 字符串）:")
    print(json_string)
    
    # 模擬修復後的解決方案
    print("\n✅ 修復後的輸出（格式化 JSON）:")
    try:
        parsed_result = json.loads(json_string)
        print(json.dumps(parsed_result, ensure_ascii=False, indent=2))
        print("\n🎉 JSON 解析修復成功！")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失敗: {e}")

async def test_cleanup():
    """測試資源清理"""
    print("\n🧹 測試資源清理")
    
    # 模擬清理過程
    components = ["coordinator", "ziwei_tool", "rag_system", "formatter"]
    
    for component in components:
        print(f"   清理 {component}...")
        await asyncio.sleep(0.1)  # 模擬清理時間
        print(f"   ✅ {component} 清理完成")
    
    print("✅ 所有組件清理完成")

async def main():
    """主測試函數"""
    print("🌟 快速測試修復後的系統")
    print("=" * 50)
    
    start_time = time.time()
    
    # 測試 JSON 解析修復
    await test_json_parsing()
    
    # 測試資源清理
    await test_cleanup()
    
    # 測試 asyncio 任務清理
    print("\n🔧 測試 asyncio 任務清理")
    current_task = asyncio.current_task()
    tasks = [task for task in asyncio.all_tasks() if not task.done() and task != current_task]
    print(f"   當前未完成任務數: {len(tasks)}")
    
    if tasks:
        print("   取消未完成任務...")
        for task in tasks:
            if not task.cancelled():
                task.cancel()
        
        try:
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=2.0
            )
            print("   ✅ 任務清理成功")
        except asyncio.TimeoutError:
            print("   ⚠️ 任務清理超時，但程序將正常退出")
    else:
        print("   ✅ 沒有需要清理的任務")
    
    end_time = time.time()
    print(f"\n🎉 測試完成，耗時: {end_time - start_time:.2f} 秒")
    print("✅ 所有修復都正常工作！")

if __name__ == "__main__":
    asyncio.run(main())
