"""
測試 Agent 討論功能
演示 Agent 之間的協作討論機制
"""

import asyncio
import logging
import json
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_discussion_mode():
    """測試討論模式"""
    print("=== 測試 Agent 討論模式 ===")
    
    try:
        from main import ZiweiAISystem
        from src.agents.coordinator import CoordinationStrategy
        
        # 創建系統
        system = ZiweiAISystem()
        await system.initialize()
        
        print("✅ 系統初始化完成")
        
        # 準備測試數據
        birth_data = {
            "gender": "女",
            "birth_year": 1992,
            "birth_month": 10,
            "birth_day": 8,
            "birth_hour": "酉"
        }
        
        print(f"📊 測試數據: {birth_data}")
        
        # 測試討論模式分析
        print("\n🗣️  開始 Agent 討論模式分析...")
        
        result = await system.analyze_ziwei_chart(
            birth_data=birth_data,
            domain_type="love"  # 專注於感情分析
        )
        
        if result['success']:
            print("✅ 討論模式分析成功")
            print(f"⏱️  處理時間: {result['metadata']['processing_time']:.2f} 秒")
            
            # 檢查是否有討論結果
            if 'discussion_result' in result['metadata']:
                discussion_info = result['metadata']['discussion_result']
                if discussion_info:
                    print(f"💬 討論輪次: {len(discussion_info.get('rounds', []))}")
                    print(f"🎯 最終共識: {discussion_info.get('final_consensus', 'N/A')[:100]}...")
                    
                    # 顯示關鍵洞察
                    insights = discussion_info.get('key_insights', [])
                    if insights:
                        print(f"💡 關鍵洞察 ({len(insights)} 條):")
                        for i, insight in enumerate(insights[:3], 1):
                            print(f"  {i}. {insight}")
                    
                    # 顯示分歧點
                    disagreements = discussion_info.get('disagreements', [])
                    if disagreements:
                        print(f"⚖️  分歧點 ({len(disagreements)} 條):")
                        for i, disagreement in enumerate(disagreements[:2], 1):
                            print(f"  {i}. {disagreement}")
            
            # 顯示最終分析結果
            formatted_result = result['result']
            if isinstance(formatted_result, dict):
                print(f"\n📋 最終分析結果:")
                print(f"🎯 分析類型: {formatted_result.get('analysis_type', 'N/A')}")
                
                analysis = formatted_result.get('detailed_analysis', '')
                if analysis:
                    print(f"📝 分析內容: {analysis[:300]}...")
            
            return True
        else:
            print(f"❌ 討論模式分析失敗: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_debate_mode():
    """測試辯論模式"""
    print("\n=== 測試 Agent 辯論模式 ===")
    
    try:
        from src.agents.coordinator import MultiAgentCoordinator, CoordinationStrategy
        from src.agents.claude_agent import ClaudeAgent
        from src.agents.gpt_agent import GPTAgent
        from src.agents.domain_agent import DomainAgent
        
        # 創建協調器
        coordinator = MultiAgentCoordinator()
        
        # 手動創建 Agent（簡化測試）
        claude_agent = ClaudeAgent("claude_logic")
        gpt_agent = GPTAgent("gpt_creative")
        love_agent = DomainAgent("love_expert", "love")
        
        # 添加到協調器
        coordinator.agents = {
            "claude_logic": claude_agent,
            "gpt_creative": gpt_agent,
            "love_expert": love_agent
        }
        
        print("✅ 協調器和 Agent 設置完成")
        
        # 準備測試數據
        test_input = {
            'chart_data': {
                'success': True,
                'data': {
                    'palace': {
                        '命宮': ['紫微星', '天府星'],
                        '夫妻宮': ['太陽星', '巨門星']
                    }
                }
            },
            'knowledge_context': '紫微星代表領導能力，太陽星代表熱情...',
            'birth_data': {
                "gender": "男",
                "birth_year": 1988,
                "birth_month": 6,
                "birth_day": 20,
                "birth_hour": "午"
            }
        }
        
        print("📊 開始辯論模式協調...")
        
        # 執行辯論模式
        result = await coordinator.coordinate_analysis(
            input_data=test_input,
            domain_type="love",
            strategy=CoordinationStrategy.DEBATE
        )
        
        if result.success:
            print("✅ 辯論模式協調成功")
            print(f"💬 參與 Agent: {len(result.responses)}")
            
            # 顯示辯論結果
            if result.discussion_result:
                discussion = result.discussion_result
                print(f"🗣️  辯論輪次: {len(discussion.rounds)}")
                
                for i, round_info in enumerate(discussion.rounds, 1):
                    print(f"\n第 {i} 輪 - {round_info.topic}:")
                    print(f"  參與者: {', '.join(round_info.participants)}")
                    print(f"  共識程度: {round_info.consensus_level:.2f}")
                    
                    for response in round_info.responses[:2]:  # 只顯示前2個回應
                        print(f"  {response.agent_id}: {response.content[:100]}...")
                
                print(f"\n🎯 最終綜合: {discussion.final_consensus[:200]}...")
            
            return True
        else:
            print("❌ 辯論模式協調失敗")
            return False
            
    except Exception as e:
        print(f"❌ 辯論測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_strategy_comparison():
    """測試不同協調策略的比較"""
    print("\n=== 測試協調策略比較 ===")
    
    try:
        from main import ZiweiAISystem
        from src.agents.coordinator import CoordinationStrategy
        
        # 創建系統
        system = ZiweiAISystem()
        await system.initialize()
        
        # 測試數據
        birth_data = {
            "gender": "男",
            "birth_year": 1985,
            "birth_month": 3,
            "birth_day": 15,
            "birth_hour": "子"
        }
        
        strategies = [
            ("並行模式", CoordinationStrategy.PARALLEL),
            ("討論模式", CoordinationStrategy.DISCUSSION),
            ("辯論模式", CoordinationStrategy.DEBATE)
        ]
        
        results = {}
        
        for strategy_name, strategy in strategies:
            print(f"\n🔄 測試 {strategy_name}...")
            
            try:
                # 直接調用協調器
                agent_input = {
                    'chart_data': {'success': True, 'data': {'palace': {'命宮': ['紫微星']}}},
                    'knowledge_context': '測試知識上下文',
                    'birth_data': birth_data
                }
                
                start_time = datetime.now()
                
                result = await system.coordinator.coordinate_analysis(
                    input_data=agent_input,
                    domain_type="comprehensive",
                    strategy=strategy
                )
                
                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()
                
                if result.success:
                    results[strategy_name] = {
                        'success': True,
                        'processing_time': processing_time,
                        'responses': len(result.responses),
                        'has_discussion': result.discussion_result is not None,
                        'discussion_rounds': len(result.discussion_result.rounds) if result.discussion_result else 0
                    }
                    print(f"  ✅ 成功 - 耗時: {processing_time:.2f}s, 回應: {len(result.responses)}")
                    
                    if result.discussion_result:
                        print(f"  💬 討論輪次: {len(result.discussion_result.rounds)}")
                else:
                    results[strategy_name] = {'success': False}
                    print(f"  ❌ 失敗")
                    
            except Exception as e:
                results[strategy_name] = {'success': False, 'error': str(e)}
                print(f"  ❌ 錯誤: {str(e)}")
        
        # 總結比較
        print(f"\n📊 策略比較總結:")
        for strategy_name, result in results.items():
            if result.get('success'):
                print(f"  {strategy_name}:")
                print(f"    - 處理時間: {result.get('processing_time', 0):.2f}s")
                print(f"    - Agent 回應: {result.get('responses', 0)}")
                print(f"    - 討論輪次: {result.get('discussion_rounds', 0)}")
            else:
                print(f"  {strategy_name}: 失敗")
        
        return True
        
    except Exception as e:
        print(f"❌ 策略比較測試失敗: {str(e)}")
        return False

async def main():
    """主測試函數"""
    print("🌟 Agent 討論功能測試")
    print(f"測試時間: {datetime.now()}")
    print("=" * 60)
    
    test_results = []
    
    # 1. 測試討論模式
    discussion_success = await test_discussion_mode()
    test_results.append(("討論模式", discussion_success))
    
    # 2. 測試辯論模式
    debate_success = await test_debate_mode()
    test_results.append(("辯論模式", debate_success))
    
    # 3. 測試策略比較
    comparison_success = await test_strategy_comparison()
    test_results.append(("策略比較", comparison_success))
    
    # 總結
    print("\n" + "=" * 60)
    print("🎉 測試完成！")
    
    print(f"\n📊 測試結果總結:")
    for test_name, success in test_results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"  {test_name}: {status}")
    
    successful_tests = sum(1 for _, success in test_results if success)
    total_tests = len(test_results)
    
    print(f"\n總計: {successful_tests}/{total_tests} 個測試通過")
    
    if successful_tests == total_tests:
        print("\n🎉 所有測試通過！Agent 討論功能正常運作。")
        print("\n💡 新功能特色:")
        print("  ✅ Agent 之間可以進行多輪討論")
        print("  ✅ 支援辯論式協作分析")
        print("  ✅ 自動評估共識程度")
        print("  ✅ 提取關鍵洞察和分歧點")
        print("  ✅ 生成綜合性結論")
    else:
        print("\n⚠️  部分測試失敗，請檢查配置和實現。")

if __name__ == "__main__":
    asyncio.run(main())
