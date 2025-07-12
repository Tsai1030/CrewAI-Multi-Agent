"""
PDF 文件導入向量資料庫工具
專門用於處理紫微斗數PDF文件並建立持久化向量庫
"""

import asyncio
import logging
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import argparse

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> str:
    """從PDF文件提取文本"""
    try:
        # 嘗試使用 PyPDF2
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                logger.info(f"PDF 總頁數: {len(pdf_reader.pages)}")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    text += f"\n--- 第 {page_num} 頁 ---\n{page_text}\n"
                    
                    if page_num % 10 == 0:
                        logger.info(f"已處理 {page_num} 頁...")
                
                logger.info(f"PDF 文本提取完成，總字數: {len(text)}")
                return text
                
        except ImportError:
            logger.warning("PyPDF2 未安裝，嘗試使用 pdfplumber...")
            
            # 嘗試使用 pdfplumber
            try:
                import pdfplumber
                
                text = ""
                with pdfplumber.open(pdf_path) as pdf:
                    logger.info(f"PDF 總頁數: {len(pdf.pages)}")
                    
                    for page_num, page in enumerate(pdf.pages, 1):
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- 第 {page_num} 頁 ---\n{page_text}\n"
                        
                        if page_num % 10 == 0:
                            logger.info(f"已處理 {page_num} 頁...")
                
                logger.info(f"PDF 文本提取完成，總字數: {len(text)}")
                return text
                
            except ImportError:
                logger.error("請安裝 PDF 處理庫: pip install PyPDF2 或 pip install pdfplumber")
                return None
                
    except Exception as e:
        logger.error(f"PDF 文本提取失敗: {str(e)}")
        return None

def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """將長文本分割成適合的塊"""
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        # 如果不是最後一塊，嘗試在句號處分割
        if end < text_length:
            # 尋找最近的句號
            last_period = text.rfind('。', start, end)
            if last_period > start:
                end = last_period + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap if end < text_length else end
    
    logger.info(f"文本分割完成，共 {len(chunks)} 個塊")
    return chunks

def create_knowledge_from_chunks(chunks: List[str], source_file: str) -> List[Dict[str, Any]]:
    """將文本塊轉換為知識格式"""
    knowledge_items = []
    
    for i, chunk in enumerate(chunks, 1):
        # 嘗試識別內容類型
        content_type = "general"
        category = "紫微斗數"
        
        # 簡單的內容分類
        if any(star in chunk for star in ['紫微星', '天機星', '太陽星', '武曲星', '天同星', '廉貞星']):
            content_type = "主星解析"
        elif any(palace in chunk for palace in ['命宮', '夫妻宮', '財帛宮', '事業宮']):
            content_type = "宮位解析"
        elif any(concept in chunk for concept in ['格局', '組合', '會照']):
            content_type = "格局分析"
        elif any(fortune in chunk for fortune in ['運勢', '流年', '大限']):
            content_type = "運勢分析"
        
        knowledge_item = {
            "content": chunk,
            "metadata": {
                "source": source_file,
                "chunk_id": i,
                "category": category,
                "content_type": content_type,
                "total_chunks": len(chunks)
            }
        }
        
        knowledge_items.append(knowledge_item)
    
    return knowledge_items

async def import_pdf_to_vector_db(pdf_path: str, chunk_size: int = 1000, overlap: int = 200):
    """將PDF文件導入向量資料庫"""
    
    print(f"🌟 PDF 導入向量資料庫工具")
    print(f"📁 PDF 文件: {pdf_path}")
    print("=" * 60)
    
    # 檢查文件是否存在
    if not Path(pdf_path).exists():
        logger.error(f"PDF 文件不存在: {pdf_path}")
        return False
    
    try:
        # 1. 提取PDF文本
        print("📖 步驟 1: 提取PDF文本...")
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            logger.error("PDF 文本提取失敗")
            return False
        
        print(f"✅ 文本提取成功，總字數: {len(text)}")
        
        # 2. 分割文本
        print(f"✂️  步驟 2: 分割文本 (塊大小: {chunk_size}, 重疊: {overlap})...")
        chunks = split_text_into_chunks(text, chunk_size, overlap)
        
        if not chunks:
            logger.error("文本分割失敗")
            return False
        
        print(f"✅ 文本分割成功，共 {len(chunks)} 個塊")
        
        # 3. 創建知識格式
        print("📝 步驟 3: 轉換為知識格式...")
        source_filename = Path(pdf_path).name
        knowledge_items = create_knowledge_from_chunks(chunks, source_filename)
        
        print(f"✅ 知識格式轉換成功，共 {len(knowledge_items)} 條知識")
        
        # 4. 保存為JSON文件（可選）
        output_json = f"data/knowledge/{Path(pdf_path).stem}_knowledge.json"
        os.makedirs("data/knowledge", exist_ok=True)
        
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(knowledge_items, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 知識文件已保存: {output_json}")
        
        # 5. 導入向量資料庫
        print("🗄️  步驟 4: 導入向量資料庫...")
        
        from src.rag.rag_system import ZiweiRAGSystem
        
        # 創建RAG系統
        rag_system = ZiweiRAGSystem(logger=logger)
        
        # 檢查向量庫狀態
        stats = rag_system.get_system_status()
        vector_stats = stats.get('vector_store', {})
        initial_docs = vector_stats.get('total_documents', 0)
        
        print(f"📊 向量庫初始狀態: {initial_docs} 條文檔")
        
        # 添加知識到向量庫
        success = rag_system.add_knowledge(knowledge_items)
        
        if success:
            # 檢查更新後的狀態
            updated_stats = rag_system.get_system_status()
            updated_vector_stats = updated_stats.get('vector_store', {})
            final_docs = updated_vector_stats.get('total_documents', 0)
            
            added_docs = final_docs - initial_docs
            
            print(f"✅ 向量庫導入成功！")
            print(f"   新增文檔: {added_docs}")
            print(f"   總文檔數: {final_docs}")
            print(f"   向量庫路徑: {updated_vector_stats.get('persist_directory', 'unknown')}")
            
            # 測試搜索
            print("\n🔍 測試搜索功能...")
            test_query = "紫微星"
            search_results = rag_system.search_knowledge(test_query, top_k=3)
            
            print(f"搜索 '{test_query}' 找到 {len(search_results)} 條結果:")
            for i, result in enumerate(search_results[:2], 1):
                content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                print(f"  {i}. {content_preview}")
            
            return True
        else:
            logger.error("向量庫導入失敗")
            return False
            
    except Exception as e:
        logger.error(f"PDF 導入過程失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="PDF 文件導入向量資料庫工具")
    parser.add_argument('pdf_path', help='PDF 文件路徑')
    parser.add_argument('--chunk-size', type=int, default=1000, help='文本塊大小 (默認: 1000)')
    parser.add_argument('--overlap', type=int, default=200, help='文本塊重疊大小 (默認: 200)')
    
    args = parser.parse_args()
    
    # 執行導入
    success = await import_pdf_to_vector_db(
        pdf_path=args.pdf_path,
        chunk_size=args.chunk_size,
        overlap=args.overlap
    )
    
    if success:
        print("\n🎉 PDF 導入完成！")
        print("\n📋 下一步:")
        print("  1. 運行 python main.py 使用完整系統")
        print("  2. 運行 python manage_vector_db.py status 查看向量庫狀態")
        print("  3. 運行 python manage_vector_db.py search --query '關鍵詞' 測試搜索")
    else:
        print("\n❌ PDF 導入失敗，請檢查錯誤信息")

if __name__ == "__main__":
    print("📚 紫微斗數PDF導入工具")
    print("請確保已安裝PDF處理庫:")
    print("  pip install PyPDF2")
    print("  或")
    print("  pip install pdfplumber")
    print()
    
    asyncio.run(main())
