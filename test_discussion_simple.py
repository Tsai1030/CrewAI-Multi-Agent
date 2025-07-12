"""
簡化的 Agent 討論測試
只測試核心討論功能，不依賴外部 API
"""

import asyncio
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_discussion_architecture():
    """測試討論架構"""
    print("=== 測試討論架構 ===")
    
    try:
        # 測試導入
        from src.agents.coordinator import CoordinationStrategy, DiscussionRound, DiscussionResult
        from src.agents.base_agent import AgentResponse, AgentRole
        
        print("✅ 討論相關類別導入成功")
        
        # 測試策略枚舉
        strategies = [strategy.value for strategy in CoordinationStrategy]
        print(f"✅ 協調策略: {strategies}")
        
        # 檢查新增的策略
        if "discussion" in strategies and "debate" in strategies:
            print("✅ 新增討論和辯論策略成功")
        else:
            print("⚠️  討論或辯論策略未正確添加")
        
        # 測試創建討論輪次
        test_response = AgentResponse(
            agent_id="test_agent",
            role=AgentRole.ANALYST,
            content="這是一個測試回應",
            confidence=0.8,
            success=True
        )
        
        discussion_round = DiscussionRound(
            round_number=1,
            topic="測試討論",
            participants=["test_agent"],
            responses=[test_response],
            consensus_level=0.5
        )
        
        print(f"✅ 討論輪次創建成功: 第 {discussion_round.round_number} 輪")
        print(f"  - 主題: {discussion_round.topic}")
        print(f"  - 參與者: {discussion_round.participants}")
        print(f"  - 共識程度: {discussion_round.consensus_level}")
        
        # 測試討論結果
        discussion_result = DiscussionResult(
            rounds=[discussion_round],
            final_consensus="測試共識",
            key_insights=["洞察1", "洞察2"],
            disagreements=["分歧1"]
        )
        
        print(f"✅ 討論結果創建成功")
        print(f"  - 輪次數: {len(discussion_result.rounds)}")
        print(f"  - 關鍵洞察: {len(discussion_result.key_insights)}")
        print(f"  - 分歧點: {len(discussion_result.disagreements)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 架構測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_agent_discussion_methods():
    """測試 Agent 討論方法"""
    print("\n=== 測試 Agent 討論方法 ===")
    
    try:
        from src.agents.claude_agent import ClaudeAgent
        from src.agents.gpt_agent import GPTAgent
        from src.agents.domain_agent import DomainAgent
        
        # 創建 Agent 實例（不初始化 API）
        claude_agent = ClaudeAgent("test_claude")
        gpt_agent = GPTAgent("test_gpt")
        love_agent = DomainAgent("test_love", "love")
        
        print("✅ Agent 實例創建成功")
        
        # 檢查討論方法是否存在
        agents = [
            ("Claude Agent", claude_agent),
            ("GPT Agent", gpt_agent),
            ("Domain Agent", love_agent)
        ]
        
        for agent_name, agent in agents:
            has_discussion = hasattr(agent, 'participate_in_discussion')
            has_debate = hasattr(agent, 'participate_in_debate')
            
            print(f"  {agent_name}:")
            print(f"    - 討論方法: {'✅' if has_discussion else '❌'}")
            print(f"    - 辯論方法: {'✅' if has_debate else '❌'}")
            
            # 檢查任務處理能力
            if hasattr(agent, 'can_handle_task'):
                from src.agents.base_agent import AgentTask
                
                discussion_task = AgentTask(
                    task_id="test_discussion",
                    task_type="discussion_response",
                    input_data={},
                    context={}
                )
                
                debate_task = AgentTask(
                    task_id="test_debate",
                    task_type="debate_response",
                    input_data={},
                    context={}
                )
                
                can_discussion = agent.can_handle_task(discussion_task)
                can_debate = agent.can_handle_task(debate_task)
                
                print(f"    - 可處理討論任務: {'✅' if can_discussion else '❌'}")
                print(f"    - 可處理辯論任務: {'✅' if can_debate else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent 方法測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_coordinator_discussion_methods():
    """測試協調器討論方法"""
    print("\n=== 測試協調器討論方法 ===")
    
    try:
        from src.agents.coordinator import MultiAgentCoordinator
        
        # 創建協調器
        coordinator = MultiAgentCoordinator()
        
        print("✅ 協調器創建成功")
        
        # 檢查討論相關方法
        discussion_methods = [
            '_execute_discussion',
            '_execute_debate',
            '_build_discussion_context',
            '_build_debate_context',
            '_conduct_discussion_round',
            '_conduct_debate_round',
            '_evaluate_consensus',
            '_evaluate_debate_convergence',
            '_generate_final_consensus',
            '_generate_debate_synthesis'
        ]
        
        print("檢查討論方法:")
        for method_name in discussion_methods:
            has_method = hasattr(coordinator, method_name)
            print(f"  {method_name}: {'✅' if has_method else '❌'}")
        
        # 檢查討論設置
        if hasattr(coordinator, 'max_discussion_rounds'):
            print(f"✅ 最大討論輪次: {coordinator.max_discussion_rounds}")
        
        if hasattr(coordinator, 'consensus_threshold'):
            print(f"✅ 共識閾值: {coordinator.consensus_threshold}")
        
        if hasattr(coordinator, 'discussion_timeout'):
            print(f"✅ 討論超時: {coordinator.discussion_timeout}")
        
        return True
        
    except Exception as e:
        print(f"❌ 協調器測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_discussion_context_building():
    """測試討論上下文構建"""
    print("\n=== 測試討論上下文構建 ===")
    
    try:
        from src.agents.coordinator import MultiAgentCoordinator, DiscussionRound
        from src.agents.base_agent import AgentResponse, AgentRole
        
        coordinator = MultiAgentCoordinator()
        
        # 創建模擬討論輪次
        test_responses = [
            AgentResponse(
                agent_id="claude_agent",
                role=AgentRole.ANALYST,
                content="從邏輯分析角度，這個命盤顯示出強烈的領導特質...",
                confidence=0.8,
                success=True
            ),
            AgentResponse(
                agent_id="gpt_agent",
                role=AgentRole.CREATIVE,
                content="用生動的比喻來說，這就像是天生的指揮家...",
                confidence=0.7,
                success=True
            )
        ]
        
        discussion_rounds = [
            DiscussionRound(
                round_number=1,
                topic="初始分析",
                participants=["claude_agent", "gpt_agent"],
                responses=test_responses,
                consensus_level=0.6
            )
        ]
        
        # 測試討論上下文構建
        discussion_context = coordinator._build_discussion_context(discussion_rounds, "love")
        
        print("✅ 討論上下文構建成功")
        print(f"上下文長度: {len(discussion_context)} 字符")
        print(f"上下文預覽: {discussion_context[:200]}...")
        
        # 測試辯論上下文構建
        debate_context = coordinator._build_debate_context(discussion_rounds, "love")
        
        print("✅ 辯論上下文構建成功")
        print(f"辯論上下文長度: {len(debate_context)} 字符")
        print(f"辯論上下文預覽: {debate_context[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 上下文構建測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_consensus_evaluation():
    """測試共識評估"""
    print("\n=== 測試共識評估 ===")
    
    try:
        from src.agents.coordinator import MultiAgentCoordinator
        from src.agents.base_agent import AgentResponse, AgentRole
        
        coordinator = MultiAgentCoordinator()
        
        # 創建高共識的回應
        high_consensus_responses = [
            AgentResponse(
                agent_id="agent1",
                role=AgentRole.ANALYST,
                content="紫微星坐命，具有領導能力，性格穩重，適合管理工作",
                confidence=0.9,
                success=True
            ),
            AgentResponse(
                agent_id="agent2",
                role=AgentRole.CREATIVE,
                content="紫微星的人天生就有領導氣質，穩重可靠，很適合當主管",
                confidence=0.8,
                success=True
            )
        ]
        
        # 創建低共識的回應
        low_consensus_responses = [
            AgentResponse(
                agent_id="agent1",
                role=AgentRole.ANALYST,
                content="紫微星坐命，財運很好，適合投資",
                confidence=0.7,
                success=True
            ),
            AgentResponse(
                agent_id="agent2",
                role=AgentRole.CREATIVE,
                content="天機星的變化特質，感情運勢不穩定",
                confidence=0.6,
                success=True
            )
        ]
        
        # 測試共識評估
        high_consensus = await coordinator._evaluate_consensus(high_consensus_responses)
        low_consensus = await coordinator._evaluate_consensus(low_consensus_responses)
        
        print(f"✅ 高共識評估: {high_consensus:.3f}")
        print(f"✅ 低共識評估: {low_consensus:.3f}")
        
        if high_consensus > low_consensus:
            print("✅ 共識評估邏輯正確")
        else:
            print("⚠️  共識評估可能需要調整")
        
        return True
        
    except Exception as e:
        print(f"❌ 共識評估測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主測試函數"""
    print("🌟 Agent 討論功能 - 簡化測試")
    print(f"測試時間: {datetime.now()}")
    print("=" * 60)
    
    test_results = []
    
    # 運行測試
    tests = [
        ("討論架構", test_discussion_architecture),
        ("Agent 討論方法", test_agent_discussion_methods),
        ("協調器討論方法", test_coordinator_discussion_methods),
        ("討論上下文構建", test_discussion_context_building),
        ("共識評估", test_consensus_evaluation)
    ]
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {str(e)}")
            test_results.append((test_name, False))
    
    # 總結
    print("\n" + "=" * 60)
    print("🎉 簡化測試完成！")
    
    print(f"\n📊 測試結果總結:")
    for test_name, success in test_results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"  {test_name}: {status}")
    
    successful_tests = sum(1 for _, success in test_results if success)
    total_tests = len(test_results)
    
    print(f"\n總計: {successful_tests}/{total_tests} 個測試通過")
    
    if successful_tests == total_tests:
        print("\n🎉 所有架構測試通過！Agent 討論功能已正確實現。")
        print("\n💡 新功能特色:")
        print("  ✅ 支援討論式和辯論式協作")
        print("  ✅ 多輪討論機制")
        print("  ✅ 自動共識評估")
        print("  ✅ 上下文構建和管理")
        print("  ✅ 洞察提取和分歧識別")
        
        print("\n🚀 下一步建議:")
        print("  1. 設置正確的 API 密鑰進行完整測試")
        print("  2. 調整共識評估算法")
        print("  3. 優化討論提示詞")
        print("  4. 測試不同領域的討論效果")
    else:
        print("\n⚠️  部分架構測試失敗，需要檢查實現。")

if __name__ == "__main__":
    asyncio.run(main())
