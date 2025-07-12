"""
簡單的主程式測試
逐步測試各個組件
"""

import sys
import os
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """測試導入"""
    print("=== 測試模組導入 ===")
    
    try:
        print("1. 測試基礎模組...")
        import asyncio
        import json
        from datetime import datetime
        print("✅ 基礎模組導入成功")
        
        print("2. 測試配置模組...")
        from src.config.settings import get_settings
        settings = get_settings()
        print("✅ 配置模組導入成功")
        
        print("3. 測試 Agent 模組...")
        from src.agents.base_agent import BaseAgent, AgentRole, AgentStatus
        print("✅ 基礎 Agent 模組導入成功")
        
        print("4. 測試 Claude Agent...")
        from src.agents.claude_agent import ClaudeAgent
        print("✅ Claude Agent 導入成功")
        
        print("5. 測試 GPT Agent...")
        from src.agents.gpt_agent import GPTAgent
        print("✅ GPT Agent 導入成功")
        
        print("6. 測試協調器...")
        from src.agents.coordinator import MultiAgentCoordinator
        print("✅ 協調器導入成功")
        
        print("7. 測試 MCP 工具...")
        from src.mcp.tools.ziwei_tool import ZiweiTool
        print("✅ MCP 工具導入成功")
        
        print("8. 測試 RAG 系統...")
        from src.rag.rag_system import create_rag_system
        print("✅ RAG 系統導入成功")
        
        print("9. 測試格式化器...")
        from src.output.gpt4o_formatter import GPT4oFormatter
        print("✅ 格式化器導入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 導入失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_environment():
    """測試環境配置"""
    print("\n=== 測試環境配置 ===")
    
    try:
        from src.config.settings import get_settings
        settings = get_settings()
        
        # 檢查 API 密鑰
        print("1. 檢查 OpenAI API 密鑰...")
        if hasattr(settings.openai, 'api_key') and settings.openai.api_key:
            print("✅ OpenAI API 密鑰已設置")
        else:
            print("⚠️  OpenAI API 密鑰未設置")
        
        print("2. 檢查 Anthropic API 密鑰...")
        if hasattr(settings.anthropic, 'api_key') and settings.anthropic.api_key:
            print("✅ Anthropic API 密鑰已設置")
        else:
            print("⚠️  Anthropic API 密鑰未設置")
        
        print("3. 檢查模型配置...")
        print(f"  - OpenAI 模型: {getattr(settings.openai, 'model_gpt4o', 'N/A')}")
        print(f"  - Anthropic 模型: {getattr(settings.anthropic, 'model', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 環境配置檢查失敗: {str(e)}")
        return False

async def test_individual_components():
    """測試各個組件"""
    print("\n=== 測試各個組件 ===")
    
    # 測試 RAG 系統
    print("1. 測試 RAG 系統...")
    try:
        from src.rag.rag_system import create_rag_system
        
        rag_system = create_rag_system()
        status = rag_system.get_system_status()
        print(f"✅ RAG 系統狀態: {status['system']}")
        
        # 添加測試知識
        test_knowledge = [{
            "content": "這是一個測試知識條目",
            "metadata": {"type": "test"}
        }]
        
        success = rag_system.add_knowledge(test_knowledge)
        if success:
            print("✅ RAG 知識添加成功")
        else:
            print("⚠️  RAG 知識添加失敗")
            
    except Exception as e:
        print(f"❌ RAG 系統測試失敗: {str(e)}")
    
    # 測試紫微斗數工具
    print("\n2. 測試紫微斗數工具...")
    try:
        from src.mcp.tools.ziwei_tool import ZiweiTool
        
        ziwei_tool = ZiweiTool()
        print("✅ 紫微斗數工具初始化成功")
        
        # 測試基本功能（不實際調用網站）
        test_data = {
            "gender": "男",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "birth_hour": "午"
        }
        
        # 只測試參數準備功能
        if hasattr(ziwei_tool, '_prepare_request_params'):
            params = ziwei_tool._prepare_request_params(test_data)
            print("✅ 參數準備功能正常")
        
    except Exception as e:
        print(f"❌ 紫微斗數工具測試失敗: {str(e)}")
    
    # 測試協調器（不初始化 Agent）
    print("\n3. 測試協調器結構...")
    try:
        from src.agents.coordinator import MultiAgentCoordinator, CoordinationStrategy
        print("✅ 協調器類別導入成功")
        print(f"✅ 協調策略: {[s.value for s in CoordinationStrategy]}")
        
    except Exception as e:
        print(f"❌ 協調器測試失敗: {str(e)}")

def test_main_import():
    """測試主程式導入"""
    print("\n=== 測試主程式導入 ===")
    
    try:
        from main import ZiweiAISystem, create_ziwei_ai_system, quick_analysis
        print("✅ 主程式類別導入成功")
        
        # 測試創建實例（不初始化）
        system = ZiweiAISystem()
        print("✅ 系統實例創建成功")
        
        # 檢查系統狀態
        status = system.get_system_status()
        print(f"✅ 系統狀態檢查: 初始化={status['initialized']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 主程式導入失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_simple_initialization():
    """測試簡單初始化"""
    print("\n=== 測試簡單初始化 ===")
    
    try:
        from main import ZiweiAISystem
        
        system = ZiweiAISystem()
        print("✅ 系統實例創建成功")
        
        # 嘗試初始化（可能會失敗，但我們可以看到具體錯誤）
        try:
            await system.initialize()
            print("✅ 系統初始化完全成功")
            
            status = system.get_system_status()
            print(f"📊 初始化時間: {status['initialization_time']:.2f} 秒")
            
            return system
            
        except Exception as init_error:
            print(f"⚠️  初始化部分失敗: {str(init_error)}")
            
            # 檢查哪些組件成功初始化
            if hasattr(system, 'rag_system') and system.rag_system:
                print("✅ RAG 系統初始化成功")
            if hasattr(system, 'ziwei_tool') and system.ziwei_tool:
                print("✅ 紫微斗數工具初始化成功")
            if hasattr(system, 'coordinator') and system.coordinator:
                print("✅ 協調器初始化成功")
            if hasattr(system, 'formatter') and system.formatter:
                print("✅ 格式化器初始化成功")
            
            return system
            
    except Exception as e:
        print(f"❌ 系統創建失敗: {str(e)}")
        return None

async def main():
    """主測試函數"""
    print("🌟 紫微斗數AI系統 - 簡單測試")
    print("=" * 50)
    
    # 1. 測試導入
    import_success = test_imports()
    if not import_success:
        print("❌ 導入測試失敗，終止測試")
        return
    
    # 2. 測試環境
    env_success = test_environment()
    
    # 3. 測試各個組件
    await test_individual_components()
    
    # 4. 測試主程式導入
    main_import_success = test_main_import()
    
    if main_import_success:
        # 5. 測試簡單初始化
        system = await test_simple_initialization()
        
        if system:
            print("\n✅ 基本測試完成")
            
            # 顯示最終狀態
            status = system.get_system_status()
            print(f"\n📊 最終狀態:")
            print(f"  - 系統初始化: {'✅' if status['initialized'] else '❌'}")
            
            components = status.get('components', {})
            for comp_name, comp_status in components.items():
                print(f"  - {comp_name}: {'✅' if comp_status else '❌'}")
    
    print("\n" + "=" * 50)
    print("🎉 簡單測試完成！")
    
    print("\n📋 測試總結:")
    print(f"✅ 模組導入: {'成功' if import_success else '失敗'}")
    print(f"✅ 環境配置: {'成功' if env_success else '失敗'}")
    print(f"✅ 主程式: {'成功' if main_import_success else '失敗'}")
    
    if import_success and main_import_success:
        print("\n🚀 系統基礎架構正常，可以進行完整測試")
        print("💡 建議下一步:")
        print("  1. 確保所有 API 密鑰正確設置")
        print("  2. 運行 python main.py 進行完整測試")
        print("  3. 檢查網絡連接和 API 配額")
    else:
        print("\n⚠️  系統存在基礎問題，需要修復")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
