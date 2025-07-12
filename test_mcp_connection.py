"""
測試 MCP 服務器連接
驗證 Claude MCP 服務器是否正常工作
"""

import subprocess
import json
import sys
import time
import os
from pathlib import Path

def test_mcp_server():
    """測試 MCP 服務器基本功能"""
    print("=== MCP 服務器測試 ===")
    
    # 檢查 Node.js 版本
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ Node.js 版本: {result.stdout.strip()}")
        else:
            print("✗ Node.js 未安裝或無法運行")
            return False
    except Exception as e:
        print(f"✗ Node.js 檢查失敗: {str(e)}")
        return False
    
    # 檢查 MCP 服務器文件
    mcp_server_path = Path("mcp-server/ziwei-server.js")
    if not mcp_server_path.exists():
        print(f"✗ MCP 服務器文件不存在: {mcp_server_path}")
        return False
    print(f"✓ MCP 服務器文件存在: {mcp_server_path}")
    
    # 檢查 package.json
    package_json_path = Path("mcp-server/package.json")
    if not package_json_path.exists():
        print(f"✗ package.json 不存在: {package_json_path}")
        return False
    
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        print(f"✓ package.json 有效")
        print(f"  - 名稱: {package_data.get('name', 'N/A')}")
        print(f"  - 版本: {package_data.get('version', 'N/A')}")
        
        # 檢查依賴
        deps = package_data.get('dependencies', {})
        mcp_sdk_version = deps.get('@modelcontextprotocol/sdk', 'N/A')
        print(f"  - MCP SDK 版本: {mcp_sdk_version}")
        
    except Exception as e:
        print(f"✗ package.json 解析失敗: {str(e)}")
        return False
    
    # 檢查 node_modules
    node_modules_path = Path("mcp-server/node_modules")
    if not node_modules_path.exists():
        print("✗ node_modules 不存在，請運行 npm install")
        return False
    print("✓ node_modules 存在")
    
    # 檢查 MCP SDK 安裝
    mcp_sdk_path = node_modules_path / "@modelcontextprotocol" / "sdk"
    if not mcp_sdk_path.exists():
        print("✗ MCP SDK 未安裝")
        return False
    print("✓ MCP SDK 已安裝")
    
    return True

def test_mcp_server_startup():
    """測試 MCP 服務器啟動"""
    print("\n=== MCP 服務器啟動測試 ===")
    
    try:
        # 啟動 MCP 服務器
        print("啟動 MCP 服務器...")
        process = subprocess.Popen(
            ['node', 'ziwei-server.js'],
            cwd='mcp-server',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待一段時間讓服務器啟動
        time.sleep(2)
        
        # 檢查進程是否還在運行
        if process.poll() is None:
            print("✓ MCP 服務器成功啟動")
            
            # 嘗試讀取輸出
            try:
                stdout, stderr = process.communicate(timeout=1)
                if stderr:
                    print(f"服務器輸出: {stderr}")
            except subprocess.TimeoutExpired:
                # 這是正常的，因為服務器應該持續運行
                pass
            
            # 終止進程
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
            return True
        else:
            # 進程已經退出，檢查錯誤
            stdout, stderr = process.communicate()
            print(f"✗ MCP 服務器啟動失敗")
            if stderr:
                print(f"錯誤輸出: {stderr}")
            if stdout:
                print(f"標準輸出: {stdout}")
            return False
            
    except Exception as e:
        print(f"✗ MCP 服務器啟動測試失敗: {str(e)}")
        return False

def test_claude_config():
    """測試 Claude Desktop 配置"""
    print("\n=== Claude Desktop 配置測試 ===")
    
    # Windows 配置路徑
    config_path = Path(os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json"))
    
    if not config_path.exists():
        print(f"✗ Claude Desktop 配置文件不存在: {config_path}")
        print("請確保已安裝 Claude Desktop 並創建配置文件")
        return False
    
    print(f"✓ Claude Desktop 配置文件存在: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        print("✓ 配置文件格式有效")
        
        # 檢查 MCP 服務器配置
        mcp_servers = config_data.get('mcpServers', {})
        if 'ziwei-mcp-server' in mcp_servers:
            print("✓ 找到 ziwei-mcp-server 配置")
            
            server_config = mcp_servers['ziwei-mcp-server']
            command = server_config.get('command', '')
            args = server_config.get('args', [])
            
            print(f"  - 命令: {command}")
            print(f"  - 參數: {args}")
            
            # 檢查路徑是否正確
            if args and len(args) > 0:
                server_path = Path(args[0])
                if server_path.exists():
                    print(f"✓ 服務器路徑有效: {server_path}")
                else:
                    print(f"✗ 服務器路徑無效: {server_path}")
                    return False
            
        else:
            print("✗ 未找到 ziwei-mcp-server 配置")
            print("請在 Claude Desktop 配置中添加 MCP 服務器")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 配置文件解析失敗: {str(e)}")
        return False

def provide_troubleshooting_tips():
    """提供故障排除建議"""
    print("\n=== 故障排除建議 ===")
    
    print("如果 MCP 連接失敗，請嘗試以下步驟：")
    print()
    print("1. 檢查依賴安裝：")
    print("   cd mcp-server")
    print("   npm install")
    print()
    print("2. 手動測試服務器：")
    print("   cd mcp-server")
    print("   node ziwei-server.js")
    print()
    print("3. 檢查 Claude Desktop 配置：")
    print("   配置文件位置: %APPDATA%\\Claude\\claude_desktop_config.json")
    print("   確保路徑指向正確的服務器文件")
    print()
    print("4. 重啟 Claude Desktop：")
    print("   完全關閉 Claude Desktop 應用程式")
    print("   重新啟動應用程式")
    print()
    print("5. 檢查日誌：")
    print("   Claude Desktop 日誌位置: %APPDATA%\\Claude\\logs\\")
    print("   查看是否有錯誤信息")

def main():
    """主測試函數"""
    print("Claude MCP 連接測試")
    print("=" * 50)
    
    all_tests_passed = True
    
    # 運行測試
    tests = [
        ("MCP 服務器基本檢查", test_mcp_server),
        ("MCP 服務器啟動測試", test_mcp_server_startup),
        ("Claude Desktop 配置", test_claude_config)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if not result:
                all_tests_passed = False
        except Exception as e:
            print(f"✗ {test_name} 測試異常: {str(e)}")
            all_tests_passed = False
    
    # 總結
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 所有測試通過！MCP 服務器配置正確。")
        print("請重啟 Claude Desktop 以載入 MCP 服務器。")
    else:
        print("⚠️  部分測試失敗，請檢查配置。")
        provide_troubleshooting_tips()
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
