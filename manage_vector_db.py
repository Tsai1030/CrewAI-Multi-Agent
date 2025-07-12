"""
向量庫管理工具
用於管理紫微斗數知識向量庫
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
import argparse

from src.rag.rag_system import ZiweiRAGSystem

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VectorDBManager:
    """向量庫管理器"""
    
    def __init__(self):
        self.rag_system = None
    
    async def initialize(self):
        """初始化 RAG 系統"""
        try:
            self.rag_system = ZiweiRAGSystem(logger=logger)
            logger.info("RAG 系統初始化成功")
        except Exception as e:
            logger.error(f"RAG 系統初始化失敗: {str(e)}")
            raise
    
    def show_status(self):
        """顯示向量庫狀態"""
        try:
            stats = self.rag_system.get_system_status()
            
            print("\n=== 向量庫狀態 ===")
            print(f"系統狀態: {stats.get('system', 'unknown')}")
            
            vector_stats = stats.get('vector_store', {})
            print(f"總文檔數: {vector_stats.get('total_documents', 0)}")
            print(f"集合名稱: {vector_stats.get('collection_name', 'unknown')}")
            print(f"持久化目錄: {vector_stats.get('persist_directory', 'unknown')}")
            
            generator_stats = stats.get('generator', {})
            print(f"生成器狀態: {generator_stats.get('status', 'unknown')}")
            print(f"使用模型: {generator_stats.get('model', 'unknown')}")
            
        except Exception as e:
            logger.error(f"獲取狀態失敗: {str(e)}")
    
    def add_knowledge_from_file(self, file_path: str):
        """從文件添加知識"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"文件不存在: {file_path}")
                return False
            
            logger.info(f"從文件載入知識: {file_path}")
            
            if file_path.suffix == '.json':
                # JSON 格式
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge_data = json.load(f)
                
                if isinstance(knowledge_data, list):
                    success = self.rag_system.add_knowledge(knowledge_data)
                    if success:
                        logger.info(f"成功添加 {len(knowledge_data)} 條知識")
                        return True
                else:
                    logger.error("JSON 文件格式錯誤，應該是知識項目的列表")
                    return False
            
            else:
                # 文本格式
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if content:
                    knowledge_item = {
                        "content": content,
                        "metadata": {
                            "source": file_path.name,
                            "category": "用戶添加",
                            "file_type": file_path.suffix
                        }
                    }
                    
                    success = self.rag_system.add_knowledge([knowledge_item])
                    if success:
                        logger.info(f"成功添加知識文件: {file_path.name}")
                        return True
                
            return False
            
        except Exception as e:
            logger.error(f"添加知識失敗: {str(e)}")
            return False
    
    def add_knowledge_from_directory(self, dir_path: str):
        """從目錄批量添加知識"""
        try:
            dir_path = Path(dir_path)
            
            if not dir_path.exists() or not dir_path.is_dir():
                logger.error(f"目錄不存在: {dir_path}")
                return False
            
            # 支援的文件格式
            supported_extensions = ['.txt', '.md', '.json']
            knowledge_files = []
            
            for ext in supported_extensions:
                knowledge_files.extend(dir_path.glob(f"*{ext}"))
            
            if not knowledge_files:
                logger.warning("未發現支援的知識文件")
                return False
            
            logger.info(f"發現 {len(knowledge_files)} 個知識文件")
            
            success_count = 0
            for file_path in knowledge_files:
                if self.add_knowledge_from_file(str(file_path)):
                    success_count += 1
            
            logger.info(f"成功處理 {success_count}/{len(knowledge_files)} 個文件")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"批量添加知識失敗: {str(e)}")
            return False
    
    def search_knowledge(self, query: str, top_k: int = 5):
        """搜索知識"""
        try:
            results = self.rag_system.search_knowledge(query, top_k=top_k)
            
            print(f"\n=== 搜索結果 (查詢: '{query}') ===")
            
            if not results:
                print("未找到相關知識")
                return
            
            for i, result in enumerate(results, 1):
                print(f"\n--- 結果 {i} (相似度: {result.get('score', 0):.3f}) ---")
                print(f"內容: {result['content'][:200]}...")
                
                metadata = result.get('metadata', {})
                if metadata:
                    print(f"元數據: {metadata}")
                    
        except Exception as e:
            logger.error(f"搜索失敗: {str(e)}")
    
    def clear_database(self):
        """清空向量庫"""
        try:
            # 注意：這個操作會刪除所有數據
            confirm = input("⚠️  確定要清空向量庫嗎？這將刪除所有數據！(輸入 'YES' 確認): ")
            
            if confirm != 'YES':
                print("操作已取消")
                return False
            
            # 重新創建向量庫（這會清空數據）
            self.rag_system = ZiweiRAGSystem(logger=logger)
            logger.info("向量庫已清空")
            return True
            
        except Exception as e:
            logger.error(f"清空向量庫失敗: {str(e)}")
            return False
    
    def export_knowledge(self, output_file: str):
        """導出知識（如果支持的話）"""
        try:
            # 這是一個簡化的導出功能
            # 實際實現可能需要直接訪問 ChromaDB
            logger.warning("導出功能尚未完全實現")
            logger.info("建議直接備份 data/vector_db 目錄")
            
        except Exception as e:
            logger.error(f"導出失敗: {str(e)}")


async def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="紫微斗數向量庫管理工具")
    parser.add_argument('action', choices=['status', 'add-file', 'add-dir', 'search', 'clear', 'export'],
                       help='要執行的操作')
    parser.add_argument('--file', '-f', help='文件路徑')
    parser.add_argument('--directory', '-d', help='目錄路徑')
    parser.add_argument('--query', '-q', help='搜索查詢')
    parser.add_argument('--output', '-o', help='輸出文件路徑')
    parser.add_argument('--top-k', '-k', type=int, default=5, help='搜索結果數量')
    
    args = parser.parse_args()
    
    # 初始化管理器
    manager = VectorDBManager()
    await manager.initialize()
    
    # 執行操作
    if args.action == 'status':
        manager.show_status()
    
    elif args.action == 'add-file':
        if not args.file:
            print("錯誤: 請指定文件路徑 --file")
            return
        manager.add_knowledge_from_file(args.file)
        manager.show_status()
    
    elif args.action == 'add-dir':
        if not args.directory:
            print("錯誤: 請指定目錄路徑 --directory")
            return
        manager.add_knowledge_from_directory(args.directory)
        manager.show_status()
    
    elif args.action == 'search':
        if not args.query:
            print("錯誤: 請指定搜索查詢 --query")
            return
        manager.search_knowledge(args.query, args.top_k)
    
    elif args.action == 'clear':
        manager.clear_database()
        manager.show_status()
    
    elif args.action == 'export':
        if not args.output:
            print("錯誤: 請指定輸出文件路徑 --output")
            return
        manager.export_knowledge(args.output)


if __name__ == "__main__":
    print("🌟 紫微斗數向量庫管理工具")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        logger.error(f"程序執行失敗: {str(e)}")
        import traceback
        traceback.print_exc()
