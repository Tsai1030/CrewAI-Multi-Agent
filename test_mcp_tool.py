"""
測試MCP紫微斗數工具
"""

import sys
import os
import logging
from datetime import datetime

# 添加src目錄到路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from mcp.tools.ziwei_tool import ZiweiTool, MCPZiweiTool

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_ziwei_tool():
    """測試紫微斗數工具"""
    print("=" * 50)
    print("測試紫微斗數MCP工具")
    print("=" * 50)
    
    # 創建工具實例
    tool = ZiweiTool()
    
    # 測試數據
    test_cases = [
        {
            "name": "測試案例1 - 男性",
            "data": {
                "gender": "男",
                "birth_year": 1990,
                "birth_month": 5,
                "birth_day": 15,
                "birth_hour": "午"
            }
        },
        {
            "name": "測試案例2 - 女性", 
            "data": {
                "gender": "女",
                "birth_year": 1985,
                "birth_month": 8,
                "birth_day": 20,
                "birth_hour": "子"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 {test_case['name']}")
        print(f"輸入數據: {test_case['data']}")
        print("-" * 30)
        
        try:
            # 調用工具
            result = tool.get_ziwei_chart(test_case['data'])
            
            if result.get('success'):
                print("✅ 調用成功!")
                
                # 顯示解析結果
                data = result.get('data', {})
                print(f"📊 解析結果:")
                
                if 'basic_info' in data:
                    print(f"  基本信息: {data['basic_info']}")
                
                if 'chart_info' in data:
                    print(f"  命盤信息: {data['chart_info']}")
                
                if 'main_stars' in data:
                    print(f"  主要星曜: {data['main_stars']}")
                
                if 'palaces' in data:
                    print(f"  宮位數量: {len(data['palaces'])}")
                    for palace_name, palace_data in data['palaces'].items():
                        if palace_data.get('stars'):
                            print(f"    {palace_name}: {palace_data['stars']}")
                
                # 顯示部分原始回應（用於調試）
                if 'raw_response' in result:
                    print(f"📄 原始回應片段: {result['raw_response'][:200]}...")
                
            else:
                print("❌ 調用失敗!")
                print(f"錯誤信息: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ 測試異常: {str(e)}")
        
        print("-" * 50)

def test_mcp_interface():
    """測試MCP接口"""
    print("\n" + "=" * 50)
    print("測試MCP接口")
    print("=" * 50)
    
    mcp_tool = MCPZiweiTool()
    
    # 測試工具定義
    print("🔧 工具定義:")
    definition = mcp_tool.get_tool_definition()
    print(f"  名稱: {definition['name']}")
    print(f"  描述: {definition['description']}")
    print(f"  參數: {list(definition['parameters']['properties'].keys())}")
    
    # 測試執行
    print("\n🚀 測試執行:")
    test_params = {
        "gender": "男",
        "birth_year": 1992,
        "birth_month": 3,
        "birth_day": 10,
        "birth_hour": "辰"
    }
    
    print(f"輸入參數: {test_params}")
    
    try:
        result = mcp_tool.execute(test_params)
        
        if result.get('success'):
            print("✅ MCP工具執行成功!")
            print(f"返回數據類型: {type(result.get('data'))}")
        else:
            print("❌ MCP工具執行失敗!")
            print(f"錯誤: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ MCP測試異常: {str(e)}")

def test_parameter_validation():
    """測試參數驗證"""
    print("\n" + "=" * 50)
    print("測試參數驗證")
    print("=" * 50)
    
    tool = ZiweiTool()
    
    # 測試無效參數
    invalid_cases = [
        {
            "name": "缺少性別",
            "data": {
                "birth_year": 1990,
                "birth_month": 5,
                "birth_day": 15,
                "birth_hour": "午"
            }
        },
        {
            "name": "無效年份",
            "data": {
                "gender": "男",
                "birth_year": 1800,  # 太早
                "birth_month": 5,
                "birth_day": 15,
                "birth_hour": "午"
            }
        },
        {
            "name": "無效月份",
            "data": {
                "gender": "女",
                "birth_year": 1990,
                "birth_month": 13,  # 無效
                "birth_day": 15,
                "birth_hour": "午"
            }
        }
    ]
    
    for case in invalid_cases:
        print(f"\n🧪 {case['name']}")
        try:
            result = tool.get_ziwei_chart(case['data'])
            if result.get('success'):
                print("⚠️  預期失敗但成功了")
            else:
                print(f"✅ 正確捕獲錯誤: {result.get('error')}")
        except Exception as e:
            print(f"✅ 正確拋出異常: {str(e)}")

def main():
    """主測試函數"""
    print("🌟 紫微斗數MCP工具測試開始")
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 基本功能測試
        test_ziwei_tool()
        
        # MCP接口測試
        test_mcp_interface()
        
        # 參數驗證測試
        test_parameter_validation()
        
        print("\n" + "=" * 50)
        print("✅ 所有測試完成!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
