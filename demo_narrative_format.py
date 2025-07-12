"""
演示論述格式輸出
"""

import asyncio
from src.output.gpt4o_formatter import GPT4oFormatter, FormattingTask

async def demo_narrative_format():
    """演示論述格式輸出"""
    print("🌟 演示論述格式輸出")
    print("=" * 50)
    
    try:
        # 創建格式化器
        formatter = GPT4oFormatter()
        
        # 模擬 Multi-Agent 分析結果
        mock_analysis = """
        根據命盤分析，此人命宮主星為紫微星，具有領導才能和高貴氣質。
        
        Claude Agent 分析：
        從邏輯推理角度來看，紫微星在命宮表示此人天生具備領導特質，
        性格嚴謹，做事有條理，善於分析問題。三方四正配置良好，
        顯示人生格局較高，適合從事管理或專業工作。
        
        GPT Agent 分析：
        這個命盤就像一顆明亮的北極星，指引著人生的方向。
        紫微星的能量讓您天生具備吸引他人的魅力，就像磁石一般。
        在人際關係中，您往往是眾人的焦點，具有很強的感召力。
        建議發揮您的領導天賦，在職場上積極表現。
        
        綜合建議：
        1. 發揮領導才能，承擔更多責任
        2. 保持謙遜態度，避免過於自負
        3. 注重團隊合作，發揮集體智慧
        """
        
        # 創建格式化任務
        task = FormattingTask(
            content=mock_analysis,
            domain_type="comprehensive", # 選擇領域 love, wealth, future, comprehensive
            output_format="narrative"  # 選擇論述模式、普通為json
        )
        
        print("📝 正在生成論述格式...")
        
        # 生成論述格式
        narrative_result = await formatter._format_to_narrative(task)
        
        print("✅ 論述格式生成完成")
        print("\n📖 論述格式結果:")
        print("-" * 50)
        print(narrative_result)
        print("-" * 50)
        
        # 清理資源
        await formatter.cleanup()
        print("\n✅ 演示完成")
        
    except Exception as e:
        print(f"❌ 演示失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_narrative_format())
