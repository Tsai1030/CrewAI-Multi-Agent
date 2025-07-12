"""
測試解析功能
"""

import sys
import os
from bs4 import BeautifulSoup

# 添加src目錄到路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from mcp.tools.ziwei_tool import ZiweiTool

def test_parsing_with_saved_file():
    """使用保存的HTML文件測試解析功能"""
    
    print("=== 測試解析功能 ===")
    
    # 讀取保存的HTML文件
    try:
        with open('corrected_response.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"HTML文件長度: {len(html_content)} 字符")
        
        # 創建工具實例
        tool = ZiweiTool()
        
        # 創建BeautifulSoup對象
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 測試各個解析函數
        print("\n1. 測試基本信息提取:")
        basic_info = tool._extract_basic_info(soup)
        for key, value in basic_info.items():
            print(f"  {key}: {value}")
        
        print("\n2. 測試主要星曜提取:")
        main_stars = tool._extract_main_stars(soup)
        print(f"  找到 {len(main_stars)} 個主星:")
        for star in main_stars:
            print(f"    - {star}")
        
        print("\n3. 測試宮位信息提取:")
        palaces = tool._extract_palaces(soup)
        print(f"  找到 {len(palaces)} 個宮位:")
        for palace_name, palace_data in palaces.items():
            print(f"    {palace_name}:")
            print(f"      干支: {palace_data.get('ganzhi', 'N/A')}")
            print(f"      大限: {palace_data.get('daxian', 'N/A')}")
            print(f"      星曜數量: {len(palace_data.get('stars', []))}")
            if palace_data.get('stars'):
                for star in palace_data['stars'][:3]:  # 只顯示前3個
                    print(f"        - {star}")
        
        print("\n4. 測試完整解析:")
        parsed_data = tool._parse_response_from_content(html_content)
        print(f"  解析結果鍵: {list(parsed_data.keys())}")
        
    except FileNotFoundError:
        print("❌ 找不到 corrected_response.html 文件")
        print("請先運行 test_corrected_params.py 生成該文件")
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()

def add_parse_from_content_method():
    """為ZiweiTool添加從內容解析的方法"""
    
    def _parse_response_from_content(self, html_content: str):
        """從HTML內容解析回應"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 解析基本信息
        basic_info = self._extract_basic_info(soup)
        
        # 解析命盤信息
        chart_info = self._extract_chart_info(soup)
        
        # 解析十二宮位
        palaces = self._extract_palaces(soup)
        
        # 解析主要星曜
        main_stars = self._extract_main_stars(soup)
        
        return {
            "basic_info": basic_info,
            "chart_info": chart_info,
            "palaces": palaces,
            "main_stars": main_stars,
            "total_palaces": len(palaces),
            "total_main_stars": len(main_stars)
        }
    
    # 動態添加方法到類
    ZiweiTool._parse_response_from_content = _parse_response_from_content

if __name__ == "__main__":
    add_parse_from_content_method()
    test_parsing_with_saved_file()
