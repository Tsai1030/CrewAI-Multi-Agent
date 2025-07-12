"""
修復配置問題
"""

import os
from pathlib import Path

def fix_env_file():
    """修復 .env 文件中的配置問題"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env 文件不存在")
        return False
    
    # 讀取現有內容
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 修復 .env 文件配置...")
    
    # 修復 Anthropic 模型名稱
    if "Claude Sonnet 3.5 2024-10-22" in content:
        content = content.replace(
            "ANTHROPIC_MODEL=Claude Sonnet 3.5 2024-10-22",
            "ANTHROPIC_MODEL=claude-3-5-sonnet-20241022"
        )
        print("✅ 修復 Anthropic 模型名稱格式")
    
    # 檢查必要的配置
    required_configs = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY"
    ]
    
    missing_configs = []
    for config in required_configs:
        if f"{config}=" not in content or f"{config}=your_" in content:
            missing_configs.append(config)
    
    if missing_configs:
        print(f"⚠️  缺少或未設置的配置: {', '.join(missing_configs)}")
        
        # 添加缺少的配置
        if "OPENAI_API_KEY" not in content:
            content += "\n# OpenAI API 設定\nOPENAI_API_KEY=your_openai_api_key_here\n"
        
    # 寫回文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ .env 文件修復完成")
    return True

def test_imports():
    """測試重要模組的導入"""
    print("\n🧪 測試模組導入...")
    
    try:
        from src.config.settings import get_settings
        settings = get_settings()
        print("✅ 設定模組導入成功")
        
        # 檢查 Anthropic 設定
        print(f"📋 Anthropic 模型: {settings.anthropic.model}")
        print(f"📋 Anthropic API Key: {'已設置' if settings.anthropic.api_key and not settings.anthropic.api_key.startswith('your_') else '未設置'}")
        
    except Exception as e:
        print(f"❌ 設定模組導入失敗: {e}")
        return False
    
    try:
        from src.rag.bge_embeddings import BGEM3Embeddings, HybridEmbeddings
        print("✅ BGE 嵌入模組導入成功")
    except Exception as e:
        print(f"❌ BGE 嵌入模組導入失敗: {e}")
        return False
    
    try:
        from src.rag.rag_system import ZiweiRAGSystem
        print("✅ RAG 系統模組導入成功")
    except Exception as e:
        print(f"❌ RAG 系統模組導入失敗: {e}")
        return False
    
    try:
        from src.agents.claude_agent import ClaudeAgent
        print("✅ Claude Agent 模組導入成功")
    except Exception as e:
        print(f"❌ Claude Agent 模組導入失敗: {e}")
        return False
    
    return True

def main():
    """主函數"""
    print("🔧 配置問題修復工具")
    print("=" * 50)
    
    # 1. 修復 .env 文件
    fix_env_file()
    
    # 2. 測試導入
    if test_imports():
        print("\n🎉 所有模組導入測試通過！")
        print("\n📋 下一步:")
        print("1. 確保在 .env 文件中設置有效的 API 密鑰")
        print("2. 運行 python main.py 測試完整系統")
        
        # 顯示當前配置狀態
        try:
            from src.config.settings import get_settings
            settings = get_settings()
            
            print(f"\n📊 當前配置狀態:")
            print(f"   OpenAI API Key: {'✅ 已設置' if settings.openai.api_key and not settings.openai.api_key.startswith('your_') else '❌ 未設置'}")
            print(f"   Anthropic API Key: {'✅ 已設置' if settings.anthropic.api_key and not settings.anthropic.api_key.startswith('your_') else '❌ 未設置'}")
            print(f"   Anthropic Model: {settings.anthropic.model}")
            
        except Exception as e:
            print(f"⚠️  無法讀取配置: {e}")
    else:
        print("\n❌ 部分模組導入失敗，請檢查錯誤信息")

if __name__ == "__main__":
    main()
