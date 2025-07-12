"""
調試網站回應內容
"""

import requests
from bs4 import BeautifulSoup
import sys
import os

# 添加src目錄到路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_website_response():
    """測試網站回應內容"""
    
    url = "https://fate.windada.com/cgi-bin/fate"
    
    # 測試參數
    params = {
        'sex': '1',
        'year': '1990',
        'month': '5',
        'day': '15',
        'hour': '午',
        'submit': '開始排盤'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }
    
    session = requests.Session()
    
    try:
        # 先訪問主頁
        print("1. 訪問主頁...")
        main_response = session.get("https://fate.windada.com/", headers=headers)
        print(f"主頁狀態碼: {main_response.status_code}")
        
        # 發送POST請求
        print("2. 發送紫微斗數請求...")
        response = session.post(url, data=params, headers=headers, timeout=30)
        print(f"回應狀態碼: {response.status_code}")
        print(f"回應編碼: {response.encoding}")
        
        # 嘗試不同編碼
        encodings_to_try = ['utf-8', 'big5', 'gb2312', 'gbk']
        
        for encoding in encodings_to_try:
            print(f"\n=== 嘗試編碼: {encoding} ===")
            try:
                response.encoding = encoding
                content = response.text[:1000]  # 只顯示前1000字符
                print(f"內容預覽:\n{content}")
                
                # 檢查是否包含中文字符
                if any('\u4e00' <= char <= '\u9fff' for char in content):
                    print(f"✅ {encoding} 編碼看起來正確!")
                    
                    # 使用BeautifulSoup解析
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 查找表格
                    tables = soup.find_all('table')
                    print(f"找到 {len(tables)} 個表格")
                    
                    # 查找包含紫微斗數相關內容的元素
                    ziwei_elements = soup.find_all(text=lambda text: text and any(
                        keyword in text for keyword in ['紫微', '命宮', '財帛', '夫妻', '子女', '官祿']
                    ))
                    print(f"找到 {len(ziwei_elements)} 個紫微斗數相關元素")
                    
                    if ziwei_elements:
                        print("相關元素示例:")
                        for i, element in enumerate(ziwei_elements[:5]):
                            print(f"  {i+1}. {element.strip()}")
                    
                    break
                    
            except Exception as e:
                print(f"❌ {encoding} 編碼失敗: {str(e)}")
        
        # 保存原始HTML到文件以供檢查
        with open('debug_response.html', 'w', encoding='utf-8', errors='ignore') as f:
            f.write(response.text)
        print(f"\n原始HTML已保存到 debug_response.html")
        
    except Exception as e:
        print(f"請求失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_website_response()
