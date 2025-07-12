"""
完整系統測試
測試Multi-Agent + Claude MCP + GPT-4o輸出的完整工作流程
"""

import asyncio
import sys
import os
import json
import logging
from datetime import datetime

# 添加src目錄到路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_environment_setup():
    """測試環境設定"""
    print("🔧 測試環境設定...")
    
    try:
        from config.settings import get_settings, validate_settings
        
        settings = get_settings()
        print(f"✅ 設定載入成功")
        
        # 檢查API金鑰（不顯示完整金鑰）
        openai_key = settings.openai.api_key
        anthropic_key = settings.anthropic.api_key
        
        print(f"OpenAI API Key: {'✅ 已設定' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ 未設定'}")
        print(f"Anthropic API Key: {'✅ 已設定' if anthropic_key and anthropic_key != 'your_anthropic_api_key_here' else '❌ 未設定'}")
        
        # 驗證設定
        is_valid = validate_settings()
        print(f"設定驗證: {'✅ 通過' if is_valid else '❌ 失敗'}")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ 環境設定測試失敗: {str(e)}")
        return False

async def test_agents():
    """測試各個Agent"""
    print("\n🤖 測試Multi-Agent系統...")
    
    try:
        from agents.claude_agent import ClaudeAgent
        from agents.gpt_agent import GPTAgent
        from agents.domain_agent import DomainAgent
        from agents.base_agent import AgentTask
        
        # 測試Claude Agent
        print("測試Claude Agent...")
        claude_agent = ClaudeAgent()
        claude_health = await claude_agent.health_check()
        print(f"Claude Agent健康檢查: {'✅ 通過' if claude_health else '❌ 失敗'}")
        
        # 測試GPT Agent
        print("測試GPT Agent...")
        gpt_agent = GPTAgent()
        gpt_health = await gpt_agent.health_check()
        print(f"GPT Agent健康檢查: {'✅ 通過' if gpt_health else '❌ 失敗'}")
        
        # 測試Domain Agent
        print("測試Domain Agent...")
        domain_agent = DomainAgent(domain_type="love")
        domain_health = await domain_agent.health_check()
        print(f"Domain Agent健康檢查: {'✅ 通過' if domain_health else '❌ 失敗'}")
        
        return claude_health and gpt_health and domain_health
        
    except Exception as e:
        print(f"❌ Agent測試失敗: {str(e)}")
        return False

async def test_mcp_integration():
    """測試MCP整合"""
    print("\n🔌 測試Claude MCP整合...")
    
    try:
        from mcp.claude_mcp_client import ClaudeMCPClient, test_mcp_connection
        
        # 測試MCP連接
        print("測試MCP連接...")
        connection_ok = await test_mcp_connection()
        print(f"MCP連接: {'✅ 成功' if connection_ok else '❌ 失敗'}")
        
        if connection_ok:
            # 測試工具調用
            async with ClaudeMCPClient() as client:
                test_data = {
                    "gender": "男",
                    "birth_year": 1990,
                    "birth_month": 5,
                    "birth_day": 15,
                    "birth_hour": "午"
                }
                
                result = await client.get_ziwei_chart(test_data)
                print(f"紫微斗數工具調用: {'✅ 成功' if result.get('success') else '❌ 失敗'}")
                
                return result.get('success', False)
        
        return False
        
    except Exception as e:
        print(f"❌ MCP整合測試失敗: {str(e)}")
        print("💡 提示: 請確保已按照claude_mcp_setup.md設定Claude MCP")
        return False

async def test_coordinator():
    """測試Multi-Agent協調器"""
    print("\n🎯 測試Multi-Agent協調器...")
    
    try:
        from agents.coordinator import MultiAgentCoordinator, CoordinationStrategy
        
        coordinator = MultiAgentCoordinator()
        
        # 檢查Agent狀態
        agent_status = coordinator.get_agent_status()
        print(f"已載入Agent數量: {len(agent_status)}")
        
        for agent_id, status in agent_status.items():
            print(f"  {agent_id}: {status['role']}")
        
        # 健康檢查
        health_status = await coordinator.health_check()
        healthy_agents = sum(1 for is_healthy in health_status.values() if is_healthy)
        total_agents = len(health_status)
        
        print(f"Agent健康狀態: {healthy_agents}/{total_agents} 正常")
        
        return healthy_agents > 0
        
    except Exception as e:
        print(f"❌ 協調器測試失敗: {str(e)}")
        return False

async def test_gpt4o_formatter():
    """測試GPT-4o格式化器"""
    print("\n📝 測試GPT-4o格式化器...")
    
    try:
        from output.gpt4o_formatter import GPT4oFormatter
        from agents.coordinator import CoordinationResult
        
        formatter = GPT4oFormatter()
        
        # 創建模擬協調結果
        mock_result = CoordinationResult(
            success=True,
            responses=[],
            integrated_result="這是一個測試分析結果，包含紫微斗數的基本分析內容。",
            metadata={"strategy": "parallel", "agents_used": ["claude", "gpt", "domain_love"]},
            total_time=2.5
        )
        
        # 測試格式化
        formatted_output = await formatter.format_coordination_result(
            mock_result, 
            "love",
            {"age": 30, "gender": "男"}
        )
        
        print(f"格式化結果: {'✅ 成功' if formatted_output.success else '❌ 失敗'}")
        print(f"JSON驗證: {'✅ 通過' if formatted_output.validation_passed else '❌ 失敗'}")
        
        if formatted_output.success:
            # 保存測試結果
            with open('test_formatted_output.json', 'w', encoding='utf-8') as f:
                f.write(formatted_output.formatted_content)
            print("💾 格式化結果已保存到 test_formatted_output.json")
        
        return formatted_output.success and formatted_output.validation_passed
        
    except Exception as e:
        print(f"❌ GPT-4o格式化器測試失敗: {str(e)}")
        return False

async def test_complete_workflow():
    """測試完整工作流程"""
    print("\n🚀 測試完整工作流程...")
    
    try:
        from agents.coordinator import MultiAgentCoordinator
        from output.gpt4o_formatter import format_final_output
        
        # 準備測試數據
        test_input = {
            "chart_data": {
                "basic_info": {
                    "solar_date": "1990年 5月15日11時",
                    "lunar_date": "1990年 4月21日午時",
                    "ganzhi": "庚午年辛巳月庚辰日壬午時"
                },
                "main_stars": ["天同廟", "武曲旺", "天府旺"],
                "palaces": {
                    "命宮": {"stars": ["天梁陷"], "ganzhi": "丁亥"}
                }
            },
            "user_profile": {
                "age": 35,
                "gender": "男",
                "occupation": "工程師"
            },
            "user_concerns": ["感情發展", "事業規劃"]
        }
        
        # 執行協調分析
        coordinator = MultiAgentCoordinator()
        
        print("執行Multi-Agent協調分析...")
        coordination_result = await coordinator.coordinate_analysis(
            input_data=test_input,
            domain_type="love"
        )
        
        print(f"協調分析: {'✅ 成功' if coordination_result.success else '❌ 失敗'}")
        
        if coordination_result.success:
            print(f"參與Agent: {coordination_result.metadata.get('agents_used', [])}")
            print(f"處理時間: {coordination_result.total_time:.2f}秒")
            
            # 格式化最終輸出
            print("執行GPT-4o格式化...")
            final_output = await format_final_output(
                coordination_result,
                "love",
                test_input["user_profile"]
            )
            
            print(f"最終格式化: {'✅ 成功' if final_output.success else '❌ 失敗'}")
            
            if final_output.success:
                # 保存完整結果
                with open('test_complete_result.json', 'w', encoding='utf-8') as f:
                    f.write(final_output.formatted_content)
                print("💾 完整結果已保存到 test_complete_result.json")
                
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ 完整工作流程測試失敗: {str(e)}")
        return False

async def main():
    """主測試函數"""
    
    print("🌟 紫微斗數AI系統 - 完整系統測試")
    print(f"測試時間: {datetime.now()}")
    print("="*60)
    
    test_results = {}
    
    # 1. 環境設定測試
    test_results['environment'] = await test_environment_setup()
    
    # 2. Agent測試
    test_results['agents'] = await test_agents()
    
    # 3. MCP整合測試
    test_results['mcp'] = await test_mcp_integration()
    
    # 4. 協調器測試
    test_results['coordinator'] = await test_coordinator()
    
    # 5. GPT-4o格式化器測試
    test_results['formatter'] = await test_gpt4o_formatter()
    
    # 6. 完整工作流程測試
    if all(test_results.values()):
        test_results['complete_workflow'] = await test_complete_workflow()
    else:
        print("\n⚠️ 跳過完整工作流程測試（前置測試未全部通過）")
        test_results['complete_workflow'] = False
    
    # 測試總結
    print("\n" + "="*60)
    print("📊 測試結果總結")
    print("="*60)
    
    for test_name, result in test_results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    
    print(f"\n總體結果: {passed_tests}/{total_tests} 測試通過")
    
    if passed_tests == total_tests:
        print("🎉 所有測試通過！系統準備就緒！")
        print("\n📋 下一步建議:")
        print("1. 設定Claude MCP服務器")
        print("2. 建立RAG知識庫")
        print("3. 開發前端介面")
        print("4. 部署到生產環境")
    else:
        print("⚠️ 部分測試失敗，請檢查相關配置")
        print("\n🔧 故障排除建議:")
        
        if not test_results['environment']:
            print("- 檢查.env文件和API金鑰設定")
        if not test_results['agents']:
            print("- 檢查API連接和網絡設定")
        if not test_results['mcp']:
            print("- 按照claude_mcp_setup.md設定Claude MCP")
        if not test_results['coordinator']:
            print("- 檢查Agent初始化和依賴包")
        if not test_results['formatter']:
            print("- 檢查GPT-4o API設定")

if __name__ == "__main__":
    asyncio.run(main())
