"""
GitHub 上傳前的清理腳本
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_for_github():
    """清理不需要上傳到 GitHub 的文件"""
    
    print("🧹 開始清理文件以準備上傳到 GitHub...")
    
    # 要刪除的文件模式
    files_to_remove = [
        # 測試文件
        "test_*.py",
        "debug_*.py", 
        "*_test.py",
        "test_*.html",
        "test_*.json",
        "*_test.txt",
        
        # 回應文件
        "*_response_*.html",
        "debug_full_response_*.html",
        "correct_encoding_*.html",
        "final_test_*.html",
        "ziwei_raw_response_*.html",
        "ziwei_parsed_data_*.json",
        
        # 特定文件
        "love_analysis_test.txt",
        "corrected_response.html",
        "debug_response.html",
        "mcp_demo_response.json",
        "working_test_result.json",
        "test_result_*.json",
        "performance_test_results_*.json",
        
        # 批次檔案
        "*.bat",
    ]
    
    # 要刪除的目錄
    dirs_to_remove = [
        "cache",
        "__pycache__",
        "src/__pycache__",
        "logs",
        "vector_db_*",
        "test_*_vector_db",
        "全部檔案逐行解析",
        "前後端呈現畫面",
    ]
    
    removed_files = 0
    removed_dirs = 0
    
    # 刪除文件
    for pattern in files_to_remove:
        for file_path in glob.glob(pattern):
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"  ✅ 刪除文件: {file_path}")
                    removed_files += 1
                except Exception as e:
                    print(f"  ❌ 無法刪除文件 {file_path}: {e}")
    
    # 刪除目錄
    for pattern in dirs_to_remove:
        for dir_path in glob.glob(pattern):
            if os.path.isdir(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    print(f"  ✅ 刪除目錄: {dir_path}")
                    removed_dirs += 1
                except Exception as e:
                    print(f"  ❌ 無法刪除目錄 {dir_path}: {e}")
    
    # 清理 frontend/node_modules（如果存在）
    frontend_node_modules = "frontend/node_modules"
    if os.path.exists(frontend_node_modules):
        try:
            shutil.rmtree(frontend_node_modules)
            print(f"  ✅ 刪除目錄: {frontend_node_modules}")
            removed_dirs += 1
        except Exception as e:
            print(f"  ❌ 無法刪除目錄 {frontend_node_modules}: {e}")
    
    # 清理 mcp-server/node_modules（如果存在）
    mcp_node_modules = "mcp-server/node_modules"
    if os.path.exists(mcp_node_modules):
        try:
            shutil.rmtree(mcp_node_modules)
            print(f"  ✅ 刪除目錄: {mcp_node_modules}")
            removed_dirs += 1
        except Exception as e:
            print(f"  ❌ 無法刪除目錄 {mcp_node_modules}: {e}")
    
    print(f"\n📊 清理完成:")
    print(f"  刪除文件: {removed_files} 個")
    print(f"  刪除目錄: {removed_dirs} 個")

def check_sensitive_files():
    """檢查是否有敏感文件"""
    
    print("\n🔍 檢查敏感文件...")
    
    sensitive_patterns = [
        "*.env",
        "*key*",
        "*secret*", 
        "*token*",
        "*.pdf",
    ]
    
    found_sensitive = []
    
    for pattern in sensitive_patterns:
        for file_path in glob.glob(pattern, recursive=True):
            if file_path != ".env.example" and not file_path.startswith(".git"):
                found_sensitive.append(file_path)
    
    if found_sensitive:
        print("  ⚠️ 發現可能的敏感文件:")
        for file_path in found_sensitive:
            print(f"    - {file_path}")
        print("  請手動檢查這些文件是否包含敏感信息")
    else:
        print("  ✅ 未發現明顯的敏感文件")

def check_file_sizes():
    """檢查大文件"""
    
    print("\n📏 檢查大文件 (>10MB)...")
    
    large_files = []
    
    for root, dirs, files in os.walk("."):
        # 跳過 .git 目錄
        if ".git" in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if size > 10 * 1024 * 1024:  # 10MB
                    large_files.append((file_path, size))
            except:
                continue
    
    if large_files:
        print("  ⚠️ 發現大文件:")
        for file_path, size in large_files:
            size_mb = size / (1024 * 1024)
            print(f"    - {file_path}: {size_mb:.1f}MB")
        print("  請考慮是否需要排除這些文件")
    else:
        print("  ✅ 未發現大文件")

def show_final_structure():
    """顯示最終的項目結構"""
    
    print("\n📁 清理後的項目結構:")
    
    important_items = [
        "src/",
        "frontend/",
        "mcp-server/",
        "docs/",
        "examples/",
        "main.py",
        "api_server.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        ".env.example",
    ]
    
    for item in important_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                print(f"  📁 {item}")
            else:
                print(f"  📄 {item}")
        else:
            print(f"  ❌ {item} (缺失)")

def main():
    """主函數"""
    
    print("🚀 GitHub 上傳準備工具")
    print("=" * 50)
    
    # 確認操作
    response = input("確定要清理文件嗎？這將刪除測試文件和臨時文件 (y/N): ")
    if response.lower() != 'y':
        print("操作已取消")
        return
    
    # 執行清理
    cleanup_for_github()
    
    # 檢查敏感文件
    check_sensitive_files()
    
    # 檢查大文件
    check_file_sizes()
    
    # 顯示最終結構
    show_final_structure()
    
    print("\n✅ 清理完成！")
    print("\n📋 下一步:")
    print("1. 檢查 .env 文件是否包含真實的 API 金鑰（應該排除）")
    print("2. 確認 .gitignore 設定正確")
    print("3. 執行 git add . 和 git commit")
    print("4. 推送到 GitHub: git push origin main")

if __name__ == "__main__":
    main()
