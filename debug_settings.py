"""
調試設定問題
"""

import os
from dotenv import load_dotenv

def debug_settings():
    """調試設定讀取問題"""
    print("🔍 調試設定讀取問題")
    print("=" * 50)
    
    # 1. 檢查 .env 文件是否存在
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env 文件存在: {os.path.abspath(env_file)}")
    else:
        print(f"❌ .env 文件不存在: {os.path.abspath(env_file)}")
        return
    
    # 2. 強制重新載入環境變數
    print("\n🔄 重新載入環境變數...")
    load_dotenv(override=True)
    
    # 3. 直接檢查環境變數
    print("\n📋 直接檢查環境變數:")
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    secret_key = os.getenv("SECRET_KEY")
    
    print(f"   OPENAI_API_KEY: {openai_key[:20] + '...' if openai_key else 'None'}")
    print(f"   ANTHROPIC_API_KEY: {anthropic_key[:20] + '...' if anthropic_key else 'None'}")
    print(f"   SECRET_KEY: {secret_key}")
    
    # 4. 檢查設定類
    print("\n🧪 檢查設定類:")
    try:
        # 清除模組快取
        import sys
        if 'src.config.settings' in sys.modules:
            del sys.modules['src.config.settings']
        
        from src.config.settings import get_settings
        settings = get_settings()
        
        print(f"   設定中的 OpenAI Key: {settings.openai.api_key[:20] + '...' if settings.openai.api_key else 'None'}")
        print(f"   設定中的 Anthropic Key: {settings.anthropic.api_key[:20] + '...' if settings.anthropic.api_key else 'None'}")
        print(f"   設定中的 Secret Key: {settings.app.secret_key}")
        
        # 5. 手動驗證
        print("\n✅ 手動驗證:")
        valid_openai = settings.openai.api_key and settings.openai.api_key != "your_openai_api_key_here"
        valid_anthropic = settings.anthropic.api_key and settings.anthropic.api_key != "your_anthropic_api_key_here"
        valid_secret = settings.app.secret_key and settings.app.secret_key != "your_secret_key_here"
        
        print(f"   OpenAI Key 有效: {valid_openai}")
        print(f"   Anthropic Key 有效: {valid_anthropic}")
        print(f"   Secret Key 有效: {valid_secret}")
        
        if valid_openai and valid_anthropic and valid_secret:
            print("\n🎉 所有設定都正確！")
        else:
            print("\n❌ 部分設定有問題")
            
    except Exception as e:
        print(f"❌ 設定檢查失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_settings()
