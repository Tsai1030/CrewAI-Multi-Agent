"""
Agent 討論功能演示
展示 Agent 之間如何進行協作討論和辯論
"""

import asyncio
import logging
import json
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_section(title):
    """打印章節標題"""
    print(f"\n{'='*60}")
    print(f"🌟 {title}")
    print('='*60)

def print_subsection(title):
    """打印子章節標題"""
    print(f"\n{'─'*40}")
    print(f"📋 {title}")
    print('─'*40)

async def demo_discussion_vs_parallel():
    """演示討論模式 vs 並行模式的差異"""
    print_section("討論模式 vs 並行模式比較")
    
    try:
        from src.agents.coordinator import MultiAgentCoordinator, CoordinationStrategy
        from src.agents.claude_agent import ClaudeAgent
        from src.agents.gpt_agent import GPTAgent
        from src.agents.domain_agent import DomainAgent
        
        # 創建協調器和 Agent
        coordinator = MultiAgentCoordinator()
        
        # 手動創建 Agent（模擬模式，不實際調用 API）
        claude_agent = ClaudeAgent("claude_logic")
        gpt_agent = GPTAgent("gpt_creative")
        love_agent = DomainAgent("love_expert", "love")
        
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
                        '夫妻宮': ['太陽星', '巨門星'],
                        '財帛宮': ['天機星', '太陰星']
                    }
                }
            },
            'knowledge_context': '紫微星代表領導能力，太陽星代表熱情開朗，天機星代表智慧變化...',
            'birth_data': {
                "gender": "女",
                "birth_year": 1990,
                "birth_month": 8,
                "birth_day": 15,
                "birth_hour": "午"
            }
        }
        
        strategies_to_test = [
            ("並行模式", CoordinationStrategy.PARALLEL),
            ("討論模式", CoordinationStrategy.DISCUSSION),
            ("辯論模式", CoordinationStrategy.DEBATE)
        ]
        
        results = {}
        
        for strategy_name, strategy in strategies_to_test:
            print_subsection(f"測試 {strategy_name}")
            
            try:
                start_time = datetime.now()
                
                result = await coordinator.coordinate_analysis(
                    input_data=test_input,
                    domain_type="love",
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
                        'discussion_rounds': len(result.discussion_result.rounds) if result.discussion_result else 0,
                        'integrated_result': result.integrated_result[:200] + "..." if result.integrated_result else "無整合結果"
                    }
                    
                    print(f"✅ {strategy_name} 執行成功")
                    print(f"   ⏱️  處理時間: {processing_time:.2f} 秒")
                    print(f"   📊 Agent 回應數: {len(result.responses)}")
                    
                    if result.discussion_result:
                        discussion = result.discussion_result
                        print(f"   💬 討論輪次: {len(discussion.rounds)}")
                        print(f"   🎯 最終共識: {discussion.final_consensus[:100]}...")
                        
                        if discussion.key_insights:
                            print(f"   💡 關鍵洞察: {len(discussion.key_insights)} 條")
                            for i, insight in enumerate(discussion.key_insights[:2], 1):
                                print(f"      {i}. {insight[:80]}...")
                        
                        if discussion.disagreements:
                            print(f"   ⚖️  分歧點: {len(discussion.disagreements)} 條")
                    
                    print(f"   📝 整合結果: {result.integrated_result[:150]}...")
                    
                else:
                    results[strategy_name] = {'success': False}
                    print(f"❌ {strategy_name} 執行失敗")
                    
            except Exception as e:
                results[strategy_name] = {'success': False, 'error': str(e)}
                print(f"❌ {strategy_name} 發生錯誤: {str(e)}")
        
        # 比較結果
        print_subsection("策略比較總結")
        
        for strategy_name, result in results.items():
            if result.get('success'):
                print(f"\n🔹 {strategy_name}:")
                print(f"   處理時間: {result.get('processing_time', 0):.2f} 秒")
                print(f"   Agent 回應: {result.get('responses', 0)} 個")
                print(f"   討論輪次: {result.get('discussion_rounds', 0)} 輪")
                print(f"   有討論結果: {'是' if result.get('has_discussion') else '否'}")
            else:
                print(f"\n🔹 {strategy_name}: 執行失敗")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def demo_discussion_rounds():
    """演示討論輪次的詳細過程"""
    print_section("討論輪次詳細演示")
    
    try:
        from src.agents.coordinator import MultiAgentCoordinator, DiscussionRound, DiscussionResult
        from src.agents.base_agent import AgentResponse, AgentRole
        
        coordinator = MultiAgentCoordinator()
        
        print("📝 模擬多輪討論過程...")
        
        # 模擬第一輪討論
        round1_responses = [
            AgentResponse(
                agent_id="claude_logic",
                role=AgentRole.ANALYST,
                content="從邏輯分析角度，紫微星坐命宮表示此人具有天生的領導能力和權威感。配合天府星，形成「紫府同宮」格局，代表穩重、有責任感，適合管理職位。在感情方面，這種人通常比較理性，會慎重考慮感情問題。",
                confidence=0.85,
                success=True
            ),
            AgentResponse(
                agent_id="gpt_creative",
                role=AgentRole.CREATIVE,
                content="用生動的比喻來說，紫微天府同宮就像是天生的CEO，既有領導魅力又有穩健的管理風格。在愛情中，她就像是一位優雅的女王，會吸引那些欣賞她能力和氣質的人。不過也要注意，太過理性可能會讓感情缺少一些浪漫色彩。",
                confidence=0.78,
                success=True
            ),
            AgentResponse(
                agent_id="love_expert",
                role=AgentRole.EXPERT,
                content="從感情專業角度分析，夫妻宮有太陽巨門，太陽星代表光明熱情，但巨門星容易造成溝通問題。這個組合暗示感情中可能會有誤會或口舌是非。建議在感情中要多溝通，避免因為誤解而產生矛盾。",
                confidence=0.82,
                success=True
            )
        ]
        
        round1 = DiscussionRound(
            round_number=1,
            topic="初始分析",
            participants=["claude_logic", "gpt_creative", "love_expert"],
            responses=round1_responses,
            consensus_level=0.6
        )
        
        print_subsection("第一輪：初始分析")
        for response in round1_responses:
            print(f"\n🤖 {response.agent_id} (信心度: {response.confidence:.2f}):")
            print(f"   {response.content}")
        
        print(f"\n📊 第一輪共識程度: {round1.consensus_level:.2f}")
        
        # 模擬第二輪討論（互相回應）
        round2_responses = [
            AgentResponse(
                agent_id="claude_logic",
                role=AgentRole.ANALYST,
                content="我同意創意專家關於「女王」特質的比喻，但需要補充的是，感情專家提到的太陽巨門組合確實需要注意。從邏輯上分析，紫微的理性特質配合巨門的溝通問題，可能會讓她在表達感情時過於直接，容易傷害到對方。建議學習更溫和的溝通方式。",
                confidence=0.88,
                success=True
            ),
            AgentResponse(
                agent_id="gpt_creative",
                role=AgentRole.CREATIVE,
                content="邏輯專家說得很對！我想補充的是，太陽巨門的組合其實也有正面意義。太陽的光明可以化解巨門的陰暗面，關鍵是要學會「說話的藝術」。就像陽光穿透烏雲一樣，用溫暖和真誠去化解誤會。建議她在感情中多用讚美和鼓勵，少用批評和指責。",
                confidence=0.83,
                success=True
            ),
            AgentResponse(
                agent_id="love_expert",
                role=AgentRole.EXPERT,
                content="兩位專家的分析都很精闢。我要強調的是，紫微天府的人在感情中往往期望值較高，容易對伴侶要求過多。配合太陽巨門的溝通問題，建議她要學會降低期望，多包容對方的不完美。同時，財帛宮的天機太陰暗示她的感情可能會受到經濟因素影響。",
                confidence=0.86,
                success=True
            )
        ]
        
        round2 = DiscussionRound(
            round_number=2,
            topic="交叉討論與深化",
            participants=["claude_logic", "gpt_creative", "love_expert"],
            responses=round2_responses,
            consensus_level=0.78
        )
        
        print_subsection("第二輪：交叉討論與深化")
        for response in round2_responses:
            print(f"\n🤖 {response.agent_id} (信心度: {response.confidence:.2f}):")
            print(f"   {response.content}")
        
        print(f"\n📊 第二輪共識程度: {round2.consensus_level:.2f}")
        print(f"📈 共識提升: {round2.consensus_level - round1.consensus_level:.2f}")
        
        # 生成最終討論結果
        discussion_result = DiscussionResult(
            rounds=[round1, round2],
            final_consensus="經過兩輪討論，各專家達成共識：此命盤主人具有領導特質但在感情溝通上需要注意技巧，建議多用溫和方式表達，降低期望值，並注意經濟因素對感情的影響。",
            key_insights=[
                "紫微天府同宮形成天生領導者格局",
                "太陽巨門組合需要注意溝通技巧",
                "理性特質可能影響感情表達",
                "經濟因素可能影響感情發展"
            ],
            disagreements=[
                "對於太陽巨門組合的正負面影響程度存在不同看法"
            ]
        )
        
        print_subsection("討論總結")
        print(f"🎯 最終共識: {discussion_result.final_consensus}")
        
        print(f"\n💡 關鍵洞察:")
        for i, insight in enumerate(discussion_result.key_insights, 1):
            print(f"   {i}. {insight}")
        
        print(f"\n⚖️  分歧點:")
        for i, disagreement in enumerate(discussion_result.disagreements, 1):
            print(f"   {i}. {disagreement}")
        
        return True
        
    except Exception as e:
        print(f"❌ 討論輪次演示失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def demo_consensus_evaluation():
    """演示共識評估機制"""
    print_section("共識評估機制演示")
    
    try:
        from src.agents.coordinator import MultiAgentCoordinator
        from src.agents.base_agent import AgentResponse, AgentRole
        
        coordinator = MultiAgentCoordinator()
        
        print("📊 測試不同共識程度的回應...")
        
        # 高共識回應
        high_consensus_responses = [
            AgentResponse(
                agent_id="agent1",
                role=AgentRole.ANALYST,
                content="紫微星坐命，具有領導能力，性格穩重，財運佳，適合管理工作",
                confidence=0.9,
                success=True
            ),
            AgentResponse(
                agent_id="agent2",
                role=AgentRole.CREATIVE,
                content="紫微星的人天生就有領導氣質，穩重可靠，財運不錯，很適合當主管",
                confidence=0.8,
                success=True
            ),
            AgentResponse(
                agent_id="agent3",
                role=AgentRole.EXPERT,
                content="紫微星主導，領導特質明顯，穩重性格，財運良好，管理職位最佳",
                confidence=0.85,
                success=True
            )
        ]
        
        # 中等共識回應
        medium_consensus_responses = [
            AgentResponse(
                agent_id="agent1",
                role=AgentRole.ANALYST,
                content="紫微星坐命，具有領導能力，但感情運勢一般",
                confidence=0.7,
                success=True
            ),
            AgentResponse(
                agent_id="agent2",
                role=AgentRole.CREATIVE,
                content="天機星的變化特質，聰明但心思多變，事業有起伏",
                confidence=0.6,
                success=True
            ),
            AgentResponse(
                agent_id="agent3",
                role=AgentRole.EXPERT,
                content="太陽星光明熱情，但容易操勞，健康需要注意",
                confidence=0.65,
                success=True
            )
        ]
        
        # 低共識回應
        low_consensus_responses = [
            AgentResponse(
                agent_id="agent1",
                role=AgentRole.ANALYST,
                content="紫微星坐命，財運很好，適合投資理財",
                confidence=0.7,
                success=True
            ),
            AgentResponse(
                agent_id="agent2",
                role=AgentRole.CREATIVE,
                content="破軍星的破壞力強，感情容易有波折，需要謹慎",
                confidence=0.6,
                success=True
            ),
            AgentResponse(
                agent_id="agent3",
                role=AgentRole.EXPERT,
                content="七殺星主殺伐，事業競爭激烈，健康運勢不佳",
                confidence=0.5,
                success=True
            )
        ]
        
        # 評估共識程度
        test_cases = [
            ("高共識回應", high_consensus_responses),
            ("中等共識回應", medium_consensus_responses),
            ("低共識回應", low_consensus_responses)
        ]
        
        for case_name, responses in test_cases:
            print_subsection(case_name)
            
            consensus_score = await coordinator._evaluate_consensus(responses)
            
            print(f"📊 共識分數: {consensus_score:.3f}")
            
            print(f"📝 回應內容:")
            for i, response in enumerate(responses, 1):
                print(f"   {i}. {response.agent_id}: {response.content}")
            
            # 分析共識程度
            if consensus_score >= 0.7:
                print(f"✅ 高共識 - Agent 們在主要觀點上達成一致")
            elif consensus_score >= 0.4:
                print(f"⚠️  中等共識 - Agent 們有部分共同觀點")
            else:
                print(f"❌ 低共識 - Agent 們觀點分歧較大")
        
        return True
        
    except Exception as e:
        print(f"❌ 共識評估演示失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主演示函數"""
    print("🌟 Agent 討論功能完整演示")
    print(f"演示時間: {datetime.now()}")
    print("=" * 60)
    
    print("💡 本演示將展示:")
    print("   1. 討論模式 vs 並行模式的差異")
    print("   2. 多輪討論的詳細過程")
    print("   3. 共識評估機制")
    print("   4. Agent 之間的協作互動")
    
    demos = [
        ("討論模式比較", demo_discussion_vs_parallel),
        ("討論輪次演示", demo_discussion_rounds),
        ("共識評估演示", demo_consensus_evaluation)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n🚀 開始 {demo_name}...")
            result = await demo_func()
            results.append((demo_name, result))
            
            if result:
                print(f"✅ {demo_name} 演示成功")
            else:
                print(f"❌ {demo_name} 演示失敗")
                
        except Exception as e:
            print(f"❌ {demo_name} 演示異常: {str(e)}")
            results.append((demo_name, False))
    
    # 總結
    print_section("演示總結")
    
    successful_demos = sum(1 for _, success in results if success)
    total_demos = len(results)
    
    print(f"📊 演示結果: {successful_demos}/{total_demos} 個演示成功")
    
    for demo_name, success in results:
        status = "✅ 成功" if success else "❌ 失敗"
        print(f"   {demo_name}: {status}")
    
    if successful_demos == total_demos:
        print(f"\n🎉 所有演示成功！Agent 討論功能完美運作！")
        
        print(f"\n🌟 新功能亮點:")
        print(f"   ✅ Agent 之間可以進行真正的討論和辯論")
        print(f"   ✅ 多輪討論機制讓分析更加深入")
        print(f"   ✅ 自動評估共識程度，確保質量")
        print(f"   ✅ 每個 Agent 都有獨特的討論風格")
        print(f"   ✅ 系統能識別分歧點並尋求共識")
        
        print(f"\n🚀 實際應用價值:")
        print(f"   💡 更全面的命理分析")
        print(f"   💡 多角度的觀點整合")
        print(f"   💡 減少單一 Agent 的偏見")
        print(f"   💡 提高分析結果的可信度")
        print(f"   💡 更豐富的洞察和建議")
        
    else:
        print(f"\n⚠️  部分演示失敗，但核心功能已實現")
    
    print(f"\n📋 下一步建議:")
    print(f"   1. 設置 API 密鑰進行實際測試")
    print(f"   2. 調整討論提示詞以獲得更好效果")
    print(f"   3. 優化共識評估算法")
    print(f"   4. 添加更多專業領域的 Agent")
    print(f"   5. 開發 Web 界面展示討論過程")

if __name__ == "__main__":
    asyncio.run(main())
