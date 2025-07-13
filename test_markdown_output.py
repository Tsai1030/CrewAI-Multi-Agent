"""
測試 Markdown 格式輸出
"""

import asyncio
from src.output.gpt4o_formatter import GPT4oFormatter, FormattingTask

async def test_markdown_output():
    """測試 Markdown 格式輸出"""
    print("🧪 測試 Markdown 格式輸出")
    print("=" * 50)
    
    try:
        # 創建格式化器
        formatter = GPT4oFormatter()
        
        # 模擬分析結果
        mock_analysis = """
        根據您的紫微斗數命盤分析，您的財運和事業運勢整體來說相當不錯。
        
        命盤分析：
        - 財帛宮主星：武曲星，代表財富累積能力強
        - 事業宮配置：天機星，適合技術和創新領域
        - 整體評分：7分（滿分10分）
        
        詳細建議：
        1. 投資理財方面要謹慎保守
        2. 事業發展可朝向科技領域
        3. 人際關係需要多加經營
        """
        
        # 創建格式化任務
        task = FormattingTask(
            content=mock_analysis,
            domain_type="wealth",
            output_format="narrative"
        )
        
        print("📝 正在生成 Markdown 格式...")
        
        # 生成論述格式
        result = await formatter._format_to_narrative(task)
        
        print("✅ Markdown 格式生成完成")
        print("\n📖 Markdown 格式結果:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # 檢查是否包含 Markdown 語法
        markdown_indicators = ['##', '###', '**', '*']
        found_markdown = any(indicator in result for indicator in markdown_indicators)
        
        if found_markdown:
            print("✅ 檢測到 Markdown 格式語法")
        else:
            print("⚠️  未檢測到 Markdown 格式語法")
        
        # 清理資源
        await formatter.cleanup()
        print("\n✅ 測試完成")
        
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_markdown_output())
