"""
簡化版MCP工具測試 - 不依賴外部庫
"""

import urllib.request
import urllib.parse
import json
import re
from html.parser import HTMLParser

class SimpleZiweiTool:
    """簡化版紫微斗數工具"""
    
    def __init__(self):
        self.base_url = "https://fate.windada.com/cgi-bin/fate"
        
        # 時辰對應表
        self.hour_mapping = {
            "子": "00:00~00:59",
            "丑": "01:00~01:59", 
            "寅": "02:00~02:59",
            "卯": "03:00~03:59",
            "辰": "04:00~04:59",
            "巳": "05:00~05:59",
            "午": "06:00~06:59",
            "未": "07:00~07:59",
            "申": "08:00~08:59",
            "酉": "09:00~09:59",
            "戌": "10:00~10:59",
            "亥": "11:00~11:59"
        }
    
    def get_ziwei_chart(self, birth_data):
        """獲取紫微斗數命盤"""
        try:
            print(f"📝 準備請求參數...")
            params = self._prepare_request_params(birth_data)
            print(f"參數: {params}")
            
            print(f"🌐 發送HTTP請求...")
            response_text = self._send_request(params)
            print(f"回應長度: {len(response_text)} 字符")
            
            print(f"🔍 解析回應...")
            parsed_data = self._parse_response(response_text)
            
            return {
                "success": True,
                "data": parsed_data,
                "raw_response_preview": response_text[:500]
            }
            
        except Exception as e:
            print(f"❌ 錯誤: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _prepare_request_params(self, birth_data):
        """準備請求參數"""
        birth_hour = birth_data.get('birth_hour', '子')
        if birth_hour not in self.hour_mapping:
            birth_hour = '子'
        
        params = {
            'sex': '1' if birth_data.get('gender', '男') == '男' else '2',
            'year': str(birth_data.get('birth_year', 1990)),
            'month': str(birth_data.get('birth_month', 1)),
            'day': str(birth_data.get('birth_day', 1)),
            'hour': birth_hour,
            'submit': '開始排盤'
        }
        
        return params
    
    def _send_request(self, params):
        """發送HTTP請求"""
        # 編碼參數
        data = urllib.parse.urlencode(params).encode('utf-8')
        
        # 創建請求
        req = urllib.request.Request(
            self.base_url,
            data=data,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
        )
        
        # 發送請求
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='ignore')
    
    def _parse_response(self, response_text):
        """解析回應"""
        # 簡單的文本解析
        data = {
            "basic_info": {},
            "chart_info": {},
            "palaces": {},
            "main_stars": [],
            "parsing_status": "completed"
        }
        
        # 查找基本信息
        if '性別' in response_text:
            data["basic_info"]["gender_found"] = True
        
        if '出生' in response_text:
            data["basic_info"]["birth_info_found"] = True
        
        # 查找主要星曜
        major_stars = ['紫微', '天機', '太陽', '武曲', '天同', '廉貞', '天府', '太陰', '貪狼', '巨門', '天相', '天梁', '七殺', '破軍']
        
        for star in major_stars:
            if star in response_text:
                data["main_stars"].append(star)
        
        # 查找宮位
        palace_names = ['命宮', '兄弟宮', '夫妻宮', '子女宮', '財帛宮', '疾厄宮', '遷移宮', '奴僕宮', '官祿宮', '田宅宮', '福德宮', '父母宮']
        
        for palace in palace_names:
            if palace in response_text:
                data["palaces"][palace] = {"found": True}
        
        # 檢查是否有錯誤信息
        if '錯誤' in response_text or 'error' in response_text.lower():
            data["error_detected"] = True
        
        return data

def test_simple_tool():
    """測試簡化工具"""
    print("🌟 簡化版紫微斗數工具測試")
    print("=" * 50)
    
    tool = SimpleZiweiTool()
    
    # 測試數據
    test_data = {
        "gender": "男",
        "birth_year": 1990,
        "birth_month": 5,
        "birth_day": 15,
        "birth_hour": "午"
    }
    
    print(f"🧪 測試數據: {test_data}")
    print("-" * 30)
    
    result = tool.get_ziwei_chart(test_data)
    
    if result.get('success'):
        print("✅ 調用成功!")
        
        data = result.get('data', {})
        print(f"📊 解析結果:")
        print(f"  基本信息: {data.get('basic_info')}")
        print(f"  主要星曜: {data.get('main_stars')}")
        print(f"  宮位數量: {len(data.get('palaces', {}))}")
        print(f"  解析狀態: {data.get('parsing_status')}")
        
        if data.get('error_detected'):
            print("⚠️  檢測到可能的錯誤")
        
        print(f"\n📄 回應預覽:")
        print(result.get('raw_response_preview', '')[:300] + "...")
        
    else:
        print("❌ 調用失敗!")
        print(f"錯誤: {result.get('error')}")

def test_parameter_formats():
    """測試不同參數格式"""
    print("\n" + "=" * 50)
    print("測試不同參數格式")
    print("=" * 50)
    
    tool = SimpleZiweiTool()
    
    test_cases = [
        {
            "name": "標準格式",
            "data": {"gender": "女", "birth_year": 1985, "birth_month": 8, "birth_day": 20, "birth_hour": "子"}
        },
        {
            "name": "邊界值測試",
            "data": {"gender": "男", "birth_year": 2000, "birth_month": 12, "birth_day": 31, "birth_hour": "亥"}
        }
    ]
    
    for case in test_cases:
        print(f"\n🧪 {case['name']}: {case['data']}")
        try:
            result = tool.get_ziwei_chart(case['data'])
            if result.get('success'):
                stars_count = len(result['data'].get('main_stars', []))
                palaces_count = len(result['data'].get('palaces', {}))
                print(f"✅ 成功 - 找到 {stars_count} 個主星, {palaces_count} 個宮位")
            else:
                print(f"❌ 失敗: {result.get('error')}")
        except Exception as e:
            print(f"❌ 異常: {str(e)}")

if __name__ == "__main__":
    try:
        test_simple_tool()
        test_parameter_formats()
        print("\n✅ 測試完成!")
    except Exception as e:
        print(f"\n❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
