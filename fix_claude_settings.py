"""
修復 Claude 設定問題
"""

import os
from pathlib import Path

def fix_claude_settings():
    """修復 Claude 設定"""
    print("🔧 修復 Claude 設定問題...")
    
    # 1. 檢查 .env 文件
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env 文件不存在")
        return False
    
    # 2. 讀取 .env 文件
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📋 檢查 .env 文件內容...")
    
    # 檢查是否有 ANTHROPIC_API_KEY
    if "ANTHROPIC_API_KEY=" in content:
        lines = content.split('\n')
        for line in lines:
            if line.startswith('ANTHROPIC_API_KEY='):
                key = line.split('=', 1)[1].strip()
                if key and not key.startswith('your_'):
                    print(f"✅ 找到有效的 ANTHROPIC_API_KEY: {key[:20]}...")
                else:
                    print("❌ ANTHROPIC_API_KEY 未設置或無效")
                    return False
                break
    else:
        print("❌ .env 文件中沒有 ANTHROPIC_API_KEY")
        return False
    
    # 3. 強制重新載入環境變數
    print("🔄 重新載入環境變數...")
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    # 4. 測試設定系統
    print("🧪 測試設定系統...")
    try:
        # 重新導入設定
        import importlib
        import sys
        
        # 清除設定模組快取
        if 'src.config.settings' in sys.modules:
            del sys.modules['src.config.settings']
        
        # 重新導入
        from src.config.settings import get_settings
        settings = get_settings()
        
        print(f"   Anthropic API Key: {'✅ 已設置' if settings.anthropic.api_key and not settings.anthropic.api_key.startswith('your_') else '❌ 未設置'}")
        print(f"   Anthropic Model: {settings.anthropic.model}")
        
        if settings.anthropic.api_key and not settings.anthropic.api_key.startswith('your_'):
            print("✅ 設定系統修復成功")
            return True
        else:
            print("❌ 設定系統仍有問題")
            return False
            
    except Exception as e:
        print(f"❌ 設定系統測試失敗: {str(e)}")
        return False

def create_simple_test():
    """創建簡單的 Claude 測試"""
    print("\n🧪 創建簡化的 Claude 測試...")
    
    try:
        # 直接從環境變數獲取
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        
        if not api_key or api_key.startswith('your_'):
            print("❌ 環境變數中沒有有效的 API 密鑰")
            return False
        
        print(f"✅ 環境變數 API Key: {api_key[:20]}...")
        print(f"✅ 環境變數 Model: {model}")
        
        # 直接測試 Anthropic
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model=model,
            max_tokens=20,
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        print("✅ 直接 Anthropic 測試成功")
        print(f"   回應: {response.content[0].text}")
        
        return True
        
    except Exception as e:
        print(f"❌ 直接測試失敗: {str(e)}")
        return False

def main():
    """主函數"""
    print("🔧 Claude 設定修復工具")
    print("=" * 50)
    
    # 1. 修復設定
    settings_fixed = fix_claude_settings()
    
    # 2. 直接測試
    direct_test = create_simple_test()
    
    print(f"\n📊 修復結果:")
    print(f"   設定系統: {'✅ 修復成功' if settings_fixed else '❌ 仍有問題'}")
    print(f"   直接測試: {'✅ 成功' if direct_test else '❌ 失敗'}")
    
    if direct_test:
        print(f"\n💡 結論:")
        print(f"   Claude API 本身是正常的")
        print(f"   問題可能在於系統中的設定載入")
        print(f"   建議重啟 Python 環境或重新運行 main.py")
        
        print(f"\n🚀 建議操作:")
        print(f"   1. 重啟 Python 環境")
        print(f"   2. 重新運行 python main.py")
        print(f"   3. 如果仍有問題，系統可以只使用 GPT Agent")
    else:
        print(f"\n⚠️  Claude API 有問題，但系統核心功能仍可用")

if __name__ == "__main__":
    main()
