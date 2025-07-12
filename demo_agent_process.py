"""
演示 Agent 協作過程顯示功能
"""

import asyncio
from main import ZiweiAISystem

async def demo_agent_process_display():
    """演示 Agent 過程顯示的開關功能"""
    print("🌟 Agent 協作過程顯示演示")
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
        
        # 演示1：隱藏 Agent 過程（默認模式）
        print("📊 演示1：隱藏 Agent 協作過程")
        print("-" * 40)
        print("show_agent_process=False（默認）")
        print("只顯示最終結果，不顯示 Agent 溝通過程\n")
        
        result1 = await system.analyze_ziwei_chart(
            birth_data=sample_birth_data,
            domain_type="love",
            output_format="json_to_narrative",
            show_agent_process=False  # 🎯 隱藏過程
        )
        
        if result1['success']:
            print("✅ 分析完成（隱藏過程模式）")
            print(f"⏱️  處理時間: {result1['metadata']['processing_time']:.2f} 秒")
            print("📝 結果預覽:", result1['result'][:100] + "...")
        
        print("\n" + "="*60)
        
        # 演示2：顯示 Agent 過程（詳細模式）
        print("📊 演示2：顯示 Agent 協作過程")
        print("-" * 40)
        print("show_agent_process=True")
        print("顯示完整的 Agent 溝通和協作過程\n")
        
        result2 = await system.analyze_ziwei_chart(
            birth_data=sample_birth_data,
            domain_type="wealth",
            output_format="json_to_narrative",
            show_agent_process=True  # 🎯 顯示過程
        )
        
        if result2['success']:
            print("✅ 分析完成（顯示過程模式）")
            print(f"⏱️  處理時間: {result2['metadata']['processing_time']:.2f} 秒")
        
        # 演示3：後端 API 使用示例
        print("\n" + "="*60)
        print("💻 後端 API 使用示例")
        print("-" * 40)
        
        print("""
在後端 API 中的使用方式：

# 方式1：在主程序中設定
result = await system.analyze_ziwei_chart(
    birth_data=birth_data,
    domain_type="love",
    output_format="json_to_narrative",
    show_agent_process=True  # 🎯 開啟過程顯示
)

# 方式2：從環境變數控制
import os
show_process = os.getenv("SHOW_AGENT_PROCESS", "false").lower() == "true"

result = await system.analyze_ziwei_chart(
    birth_data=birth_data,
    domain_type="love", 
    output_format="json_to_narrative",
    show_agent_process=show_process
)

# 方式3：從 API 請求參數控制
@app.post("/analyze")
async def analyze_chart(request_data):
    show_process = request_data.get("show_agent_process", False)
    
    result = await system.analyze_ziwei_chart(
        birth_data=request_data["birth_data"],
        domain_type=request_data.get("domain_type", "comprehensive"),
        output_format=request_data.get("output_format", "json"),
        show_agent_process=show_process  # 🎯 從前端控制
    )
    return result
        """)
        
        await system.cleanup()
        print("\n✅ 演示完成")
        
    except Exception as e:
        print(f"❌ 演示失敗: {str(e)}")
        import traceback
        traceback.print_exc()

async def demo_backend_visibility():
    """演示後端可見性說明"""
    print("\n🔍 後端可見性說明")
    print("=" * 60)
    
    print("""
📋 Agent 過程顯示的可見性：

🖥️  後端（服務器端）：
   ✅ 可以看到完整的 Agent 協作過程
   ✅ 可以看到日誌和調試信息
   ✅ 可以控制是否顯示過程
   ✅ 適合開發和調試

📱 前端（用戶端）：
   ❌ 通常不會看到 Agent 內部過程
   ✅ 只接收最終的分析結果
   ✅ 可以通過 API 參數請求過程信息（如果後端支持）
   ✅ 適合用戶體驗

🎯 建議使用場景：

開發階段：
- show_agent_process=True
- 用於調試和優化 Agent 協作

生產環境：
- show_agent_process=False（默認）
- 只返回最終結果給用戶
- 過程信息記錄在後端日誌中

特殊需求：
- 可以提供 API 參數讓前端選擇是否查看過程
- 適合需要透明度的專業用戶
    """)

if __name__ == "__main__":
    asyncio.run(demo_agent_process_display())
    asyncio.run(demo_backend_visibility())
