"""
簡單的向量資料庫建立程式
使用 BGE-M3 處理紫微斗數PDF文件，建立持久化向量庫
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
import chromadb
from chromadb.config import Settings

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_pdf_content(pdf_path: str) -> str:
    """提取PDF內容"""
    logger.info(f"開始提取PDF內容: {pdf_path}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            logger.info(f"PDF總頁數: {total_pages}")
            
            full_text = ""
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text += text + "\n"
                
                if (page_num + 1) % 50 == 0:
                    logger.info(f"已處理 {page_num + 1}/{total_pages} 頁")
            
            logger.info(f"PDF內容提取完成，總字數: {len(full_text)}")
            return full_text
            
    except Exception as e:
        logger.error(f"PDF提取失敗: {str(e)}")
        raise

def analyze_content_structure(text: str) -> Dict[str, Any]:
    """分析內容結構"""
    logger.info("分析PDF內容結構...")
    
    # 檢查常見的紫微斗數關鍵詞
    keywords = {
        '主星': ['紫微星', '天機星', '太陽星', '武曲星', '天同星', '廉貞星', '天府星', '太陰星', '貪狼星', '巨門星', '天相星', '天梁星', '七殺星', '破軍星'],
        '宮位': ['命宮', '兄弟宮', '夫妻宮', '子女宮', '財帛宮', '疾厄宮', '遷移宮', '奴僕宮', '官祿宮', '田宅宮', '福德宮', '父母宮'],
        '輔星': ['左輔', '右弼', '天魁', '天鉞', '文昌', '文曲', '祿存', '天馬'],
        '煞星': ['擎羊', '陀羅', '火星', '鈴星', '地空', '地劫'],
        '格局': ['格局', '三合', '對宮', '會照', '同宮'],
        '運勢': ['大限', '流年', '小限', '運勢', '流月', '流日']
    }
    
    analysis = {
        'total_length': len(text),
        'keyword_counts': {},
        'estimated_sections': 0
    }
    
    # 統計關鍵詞出現次數
    for category, words in keywords.items():
        count = sum(text.count(word) for word in words)
        analysis['keyword_counts'][category] = count
        logger.info(f"{category}相關內容: {count} 次提及")
    
    # 估算章節數量（基於常見分隔符）
    section_markers = text.count('第') + text.count('章') + text.count('節')
    analysis['estimated_sections'] = section_markers
    
    logger.info(f"估計章節數量: {section_markers}")
    
    return analysis

def smart_text_chunking(text: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """智能文本分塊"""
    logger.info("開始智能文本分塊...")
    
    # 根據內容分析決定分塊策略
    total_length = analysis['total_length']
    
    if total_length < 50000:  # 短文檔
        chunk_size = 800
        overlap = 100
    elif total_length < 200000:  # 中等文檔
        chunk_size = 1200
        overlap = 200
    else:  # 長文檔
        chunk_size = 1500
        overlap = 300
    
    logger.info(f"選擇分塊策略: 塊大小={chunk_size}, 重疊={overlap}")
    
    chunks = []
    start = 0
    chunk_id = 1
    
    while start < len(text):
        end = start + chunk_size
        
        # 尋找合適的分割點
        if end < len(text):
            # 優先在句號處分割
            last_period = text.rfind('。', start, end)
            if last_period > start + chunk_size // 2:
                end = last_period + 1
            else:
                # 其次在逗號處分割
                last_comma = text.rfind('，', start, end)
                if last_comma > start + chunk_size // 2:
                    end = last_comma + 1
        
        chunk_text = text[start:end].strip()
        
        if len(chunk_text) > 50:  # 只保留有意義的塊
            # 簡單的內容分類
            content_type = classify_content(chunk_text)
            
            chunk_data = {
                'content': chunk_text,
                'metadata': {
                    'chunk_id': chunk_id,
                    'start_pos': start,
                    'end_pos': end,
                    'content_type': content_type,
                    'source': '紫微斗数集成全书.pdf'
                }
            }
            chunks.append(chunk_data)
            chunk_id += 1
        
        start = end - overlap if end < len(text) else end
        
        if chunk_id % 100 == 0:
            logger.info(f"已處理 {chunk_id} 個文本塊...")
    
    logger.info(f"文本分塊完成，共 {len(chunks)} 個塊")
    return chunks

def classify_content(text: str) -> str:
    """簡單的內容分類"""
    text_lower = text.lower()
    
    # 主星相關
    main_stars = ['紫微星', '天機星', '太陽星', '武曲星', '天同星', '廉貞星', '天府星', '太陰星', '貪狼星', '巨門星', '天相星', '天梁星', '七殺星', '破軍星']
    if any(star in text for star in main_stars):
        return '主星解析'
    
    # 宮位相關
    palaces = ['命宮', '兄弟宮', '夫妻宮', '子女宮', '財帛宮', '疾厄宮', '遷移宮', '奴僕宮', '官祿宮', '田宅宮', '福德宮', '父母宮']
    if any(palace in text for palace in palaces):
        return '宮位解析'
    
    # 格局相關
    if any(word in text for word in ['格局', '三合', '對宮', '會照']):
        return '格局分析'
    
    # 運勢相關
    if any(word in text for word in ['大限', '流年', '運勢', '流月']):
        return '運勢分析'
    
    # 基礎理論
    if any(word in text for word in ['基礎', '理論', '概念', '原理']):
        return '基礎理論'
    
    return '一般內容'

def create_vector_database(chunks: List[Dict[str, Any]], db_name: str = "test1"):
    """建立向量資料庫"""
    logger.info(f"開始建立向量資料庫: {db_name}")
    
    try:
        # 設置 BGE-M3 嵌入
        from src.rag.bge_embeddings import BGEM3Embeddings
        
        # 創建嵌入模型
        embeddings = BGEM3Embeddings(
            model_name="BAAI/bge-m3",
            device="cpu",
            max_length=1024,
            batch_size=8,
            use_fp16=False
        )
        
        logger.info("BGE-M3 嵌入模型載入成功")
        
        # 創建 ChromaDB 客戶端
        persist_directory = f"./vector_db_{db_name}"
        client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 創建或獲取集合
        collection_name = f"ziwei_knowledge_{db_name}"
        try:
            collection = client.get_collection(collection_name)
            logger.info(f"使用現有集合: {collection_name}")
        except:
            collection = client.create_collection(collection_name)
            logger.info(f"創建新集合: {collection_name}")
        
        # 批次處理文檔
        batch_size = 50
        total_chunks = len(chunks)
        
        for i in range(0, total_chunks, batch_size):
            batch_chunks = chunks[i:i + batch_size]
            
            # 準備批次數據
            texts = [chunk['content'] for chunk in batch_chunks]
            metadatas = [chunk['metadata'] for chunk in batch_chunks]
            ids = [f"chunk_{chunk['metadata']['chunk_id']}" for chunk in batch_chunks]
            
            # 生成嵌入
            logger.info(f"處理批次 {i//batch_size + 1}/{(total_chunks + batch_size - 1)//batch_size}")
            embeddings_vectors = embeddings.embed_documents(texts)
            
            # 添加到向量庫
            collection.add(
                embeddings=embeddings_vectors,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"已添加 {len(batch_chunks)} 個文檔到向量庫")
        
        # 檢查最終狀態
        final_count = collection.count()
        logger.info(f"向量資料庫建立完成！")
        logger.info(f"資料庫名稱: {db_name}")
        logger.info(f"存儲路徑: {persist_directory}")
        logger.info(f"集合名稱: {collection_name}")
        logger.info(f"總文檔數: {final_count}")
        
        # 測試搜索
        logger.info("測試搜索功能...")
        test_query = "紫微星的特質"
        query_embedding = embeddings.embed_query(test_query)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        logger.info(f"搜索測試成功，找到 {len(results['documents'][0])} 條相關結果")
        
        return True
        
    except Exception as e:
        logger.error(f"向量資料庫建立失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函數"""
    pdf_path = r"C:\Users\user\Desktop\test2\紫微斗数集成全书.pdf"
    db_name = "test1"
    
    print("🌟 紫微斗數向量資料庫建立程式")
    print(f"📁 PDF文件: {pdf_path}")
    print(f"🗄️ 資料庫名稱: {db_name}")
    print("=" * 60)
    
    try:
        # 檢查文件是否存在
        if not Path(pdf_path).exists():
            logger.error(f"PDF文件不存在: {pdf_path}")
            return
        
        # 1. 提取PDF內容
        text = extract_pdf_content(pdf_path)
        
        # 2. 分析內容結構
        analysis = analyze_content_structure(text)
        
        # 3. 智能分塊
        chunks = smart_text_chunking(text, analysis)
        
        # 4. 建立向量資料庫
        success = create_vector_database(chunks, db_name)
        
        if success:
            print("\n🎉 向量資料庫建立成功！")
            print(f"📍 位置: ./vector_db_{db_name}")
            print(f"📊 文檔數: {len(chunks)}")
            print("\n✅ 可以開始使用向量資料庫進行搜索了！")
        else:
            print("\n❌ 向量資料庫建立失敗")
            
    except Exception as e:
        logger.error(f"程式執行失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
