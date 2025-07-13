"""
測試 GPT-4o Mini 模型配置
"""

import asyncio
import os
from src.config.settings import get_settings
from src.rag.gpt4o_generator import GPT4oGenerator
from src.output.gpt4o_formatter import GPT4oFormatter

async def test_gpt4o_mini_config():
    """測試 GPT-4o Mini 配置"""
    print("🧪 測試 GPT-4o Mini 模型配置")
    print("=" * 50)
    
    try:
        # 1. 檢查配置設定
        settings = get_settings()
        print(f"📋 配置檢查:")
        print(f"  - OpenAI API Key: {'已設置' if settings.openai.api_key else '未設置'}")
        print(f"  - 模型名稱: {settings.openai.model_gpt4o}")
        print(f"  - Base URL: {settings.openai.base_url}")
        
        # 2. 測試 GPT-4o 生成器
        print(f"\n🔧 測試 GPT-4o 生成器...")
        generator = GPT4oGenerator()
        print(f"  - 生成器模型: {generator.model}")
        
        # 3. 測試 GPT-4o 格式化器
        print(f"\n📝 測試 GPT-4o 格式化器...")
        formatter = GPT4oFormatter()
        print(f"  - 格式化器模型: {formatter.model}")
        
        # 4. 簡單的 API 測試
        print(f"\n🚀 執行簡單 API 測試...")
        
        test_response = await generator.client.chat.completions.create(
            model=generator.model,
            messages=[
                {"role": "system", "content": "你是一個測試助手。"},
                {"role": "user", "content": "請簡單回答：你使用的是什麼模型？"}
            ],
            max_tokens=100,
            temperature=0.1
        )
        
        response_text = test_response.choices[0].message.content
        print(f"  - API 回應: {response_text}")
        print(f"  - 使用模型: {test_response.model}")
        
        # 5. 檢查環境變數
        print(f"\n🌍 環境變數檢查:")
        print(f"  - OPENAI_MODEL_GPT4O: {os.getenv('OPENAI_MODEL_GPT4O', '未設置')}")
        print(f"  - OPENAI_API_KEY: {'已設置' if os.getenv('OPENAI_API_KEY') else '未設置'}")
        
        print(f"\n✅ 所有測試完成！")
        print(f"🎯 確認使用模型: {generator.model}")
        
        if "gpt-4o-mini" in generator.model.lower():
            print(f"🎉 成功切換到 GPT-4o Mini！")
        else:
            print(f"⚠️  模型可能未正確切換，當前: {generator.model}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_cost_comparison():
    """測試成本比較"""
    print(f"\n💰 GPT-4o vs GPT-4o Mini 成本比較:")
    print(f"=" * 40)
    
    # 假設的成本數據（實際數據請參考 OpenAI 官網）
    gpt4o_cost = {
        "input": 0.005,   # 每 1K tokens
        "output": 0.015   # 每 1K tokens
    }
    
    gpt4o_mini_cost = {
        "input": 0.00015,  # 每 1K tokens  
        "output": 0.0006   # 每 1K tokens
    }
    
    # 假設一次分析的 token 使用量
    typical_usage = {
        "input_tokens": 2000,
        "output_tokens": 1500
    }
    
    # 計算成本
    gpt4o_total = (typical_usage["input_tokens"] / 1000 * gpt4o_cost["input"] + 
                   typical_usage["output_tokens"] / 1000 * gpt4o_cost["output"])
    
    gpt4o_mini_total = (typical_usage["input_tokens"] / 1000 * gpt4o_mini_cost["input"] + 
                        typical_usage["output_tokens"] / 1000 * gpt4o_mini_cost["output"])
    
    savings = gpt4o_total - gpt4o_mini_total
    savings_percent = (savings / gpt4o_total) * 100
    
    print(f"📊 單次分析成本比較:")
    print(f"  - GPT-4o: ${gpt4o_total:.4f}")
    print(f"  - GPT-4o Mini: ${gpt4o_mini_total:.4f}")
    print(f"  - 節省: ${savings:.4f} ({savings_percent:.1f}%)")
    
    print(f"\n📈 100次分析成本:")
    print(f"  - GPT-4o: ${gpt4o_total * 100:.2f}")
    print(f"  - GPT-4o Mini: ${gpt4o_mini_total * 100:.2f}")
    print(f"  - 節省: ${savings * 100:.2f}")

if __name__ == "__main__":
    asyncio.run(test_gpt4o_mini_config())
    asyncio.run(test_cost_comparison())
