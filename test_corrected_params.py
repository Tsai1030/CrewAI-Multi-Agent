"""
測試修正後的參數
"""

import requests
from bs4 import BeautifulSoup
import sys
import os

def test_corrected_params():
    """測試修正後的參數"""
    
    url = "https://fate.windada.com/cgi-bin/fate"
    
    # 使用正確的參數名稱
    params = {
        'FUNC': 'Basic',
        'Target': '0',
        'SubTarget': '-1',
        'Sex': '1',      # 男性
        'Solar': '1',    # 國曆
        'Year': '1990',
        'Month': '5',
        'Day': '15',
        'Hour': '11'     # 午時 11:00~11:59
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }
    
    session = requests.Session()
    
    try:
        print("發送修正後的參數...")
        print(f"參數: {params}")
        
        # 先訪問主頁
        session.get("https://fate.windada.com/", headers=headers)
        
        # 發送POST請求
        response = session.post(url, data=params, headers=headers, timeout=30)
        print(f"回應狀態碼: {response.status_code}")
        
        # 設置編碼
        response.encoding = 'utf-8'
        
        # 檢查回應內容
        content = response.text
        print(f"回應長度: {len(content)} 字符")
        
        # 保存到文件
        with open('corrected_response.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 解析內容
        soup = BeautifulSoup(content, 'html.parser')
        
        # 查找命盤相關內容
        print("\n=== 查找命盤內容 ===")
        
        # 查找表格
        tables = soup.find_all('table')
        print(f"找到 {len(tables)} 個表格")
        
        # 查找包含星曜的內容
        star_keywords = ['紫微', '天機', '太陽', '武曲', '天同', '廉貞', '天府', '太陰', '貪狼', '巨門', '天相', '天梁', '七殺', '破軍']
        palace_keywords = ['命宮', '兄弟宮', '夫妻宮', '子女宮', '財帛宮', '疾厄宮', '遷移宮', '奴僕宮', '官祿宮', '田宅宮', '福德宮', '父母宮']
        
        found_stars = []
        found_palaces = []
        
        for keyword in star_keywords:
            if keyword in content:
                found_stars.append(keyword)
        
        for keyword in palace_keywords:
            if keyword in content:
                found_palaces.append(keyword)
        
        print(f"找到的星曜: {found_stars}")
        print(f"找到的宮位: {found_palaces}")
        
        # 查找特定的命盤表格
        chart_table = None
        for table in tables:
            table_text = table.get_text()
            if any(palace in table_text for palace in palace_keywords[:3]):  # 檢查前3個宮位
                chart_table = table
                break
        
        if chart_table:
            print("\n✅ 找到命盤表格!")
            print("表格內容預覽:")
            print(chart_table.get_text()[:500])
        else:
            print("\n❌ 未找到命盤表格")
            
        # 檢查是否有錯誤信息
        if "錯誤" in content or "error" in content.lower():
            print("\n⚠️ 可能包含錯誤信息")
            
        # 顯示頁面標題
        title = soup.find('title')
        if title:
            print(f"\n頁面標題: {title.get_text()}")
            
    except Exception as e:
        print(f"測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_corrected_params()
