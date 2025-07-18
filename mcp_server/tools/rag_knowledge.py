"""
RAG 知識檢索 MCP 工具
封裝現有的 RAG 系統為 MCP 工具
"""

import json
import sys
import os
from typing import Dict, Any, List

# 添加項目根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .base_tool import BaseMCPTool

class RAGKnowledgeTool(BaseMCPTool):
    """RAG 知識檢索 MCP 工具"""
    
    def __init__(self):
        super().__init__(
            name="rag_knowledge",
            description="從紫微斗數知識庫檢索相關理論和解釋"
        )
        self.rag_system = None
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """返回工具的 MCP 定義"""
        return {
            "name": "rag_knowledge",
            "description": "從紫微斗數知識庫檢索相關理論和解釋，支援搜索和生成回答",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "查詢字符串，可以是星曜名稱、宮位、或具體問題"
                    },
                    "context_type": {
                        "type": "string",
                        "description": "上下文類型",
                        "enum": ["auto", "search_only", "generate_only", "manual"],
                        "default": "auto"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "返回結果數量",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 5
                    },
                    "min_score": {
                        "type": "number",
                        "description": "最小相似度分數",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "default": 0.3
                    },
                    "domain_filter": {
                        "type": "string",
                        "description": "領域過濾器",
                        "enum": ["all", "stars", "palaces", "theory", "interpretation"],
                        "default": "all"
                    }
                },
                "required": ["query"]
            }
        }
    
    async def initialize(self):
        """初始化 RAG 系統"""
        try:
            from src.rag.rag_system import ZiweiRAGSystem
            self.rag_system = ZiweiRAGSystem(logger=self.logger)
            await super().initialize()
        except ImportError as e:
            self.logger.error(f"❌ 無法導入 ZiweiRAGSystem: {str(e)}")
            raise
    
    def _validate_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """驗證參數"""
        # 調用父類基本驗證
        base_result = super()._validate_arguments(arguments)
        if not base_result["valid"]:
            return base_result
        
        # 檢查 query
        if "query" not in arguments:
            return {
                "valid": False,
                "error": "缺少必要參數: query"
            }
        
        query = arguments["query"]
        if not isinstance(query, str) or not query.strip():
            return {
                "valid": False,
                "error": "query 必須是非空字符串"
            }
        
        # 檢查 top_k
        top_k = arguments.get("top_k", 5)
        if not isinstance(top_k, int) or not (1 <= top_k <= 20):
            return {
                "valid": False,
                "error": "top_k 必須是 1-20 之間的整數"
            }
        
        # 檢查 min_score
        min_score = arguments.get("min_score", 0.3)
        if not isinstance(min_score, (int, float)) or not (0.0 <= min_score <= 1.0):
            return {
                "valid": False,
                "error": "min_score 必須是 0.0-1.0 之間的數字"
            }
        
        return {"valid": True, "error": None}
    
    async def _pre_execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行前處理"""
        query = arguments["query"].strip()
        context_type = arguments.get("context_type", "auto")
        top_k = arguments.get("top_k", 5)
        
        self.logger.info(f"🔍 準備檢索知識: '{query}' (類型: {context_type}, 數量: {top_k})")
        
        # 設置默認值
        arguments.setdefault("min_score", 0.3)
        arguments.setdefault("domain_filter", "all")
        
        return arguments
    
    async def _execute_impl(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行知識檢索"""
        query = arguments["query"]
        context_type = arguments["context_type"]
        top_k = arguments["top_k"]
        min_score = arguments["min_score"]
        domain_filter = arguments["domain_filter"]
        
        try:
            if context_type == "search_only":
                # 只搜索，不生成回答
                search_results = self.rag_system.search_knowledge(
                    query=query,
                    top_k=top_k,
                    min_score=min_score
                )
                
                # 應用領域過濾
                filtered_results = self._apply_domain_filter(search_results, domain_filter)
                
                return {
                    "success": True,
                    "search_results": filtered_results,
                    "query": query,
                    "total_results": len(filtered_results),
                    "context_type": context_type
                }
            
            elif context_type == "generate_only":
                # 只生成，不搜索（使用現有上下文）
                context_documents = arguments.get("context_documents", [])
                result = self.rag_system.generate_answer(
                    query=query,
                    context_type="manual",
                    context_documents=context_documents
                )
                
                return {
                    "success": True,
                    "generated_answer": result,
                    "query": query,
                    "context_type": context_type
                }
            
            else:
                # auto 或 manual：搜索並生成回答
                result = self.rag_system.generate_answer(
                    query=query,
                    context_type=context_type,
                    top_k=top_k,
                    min_score=min_score,
                    **arguments
                )
                
                # 如果結果包含搜索結果，應用領域過濾
                if "search_results" in result:
                    result["search_results"] = self._apply_domain_filter(
                        result["search_results"], domain_filter
                    )
                
                return {
                    "success": True,
                    "rag_result": result,
                    "query": query,
                    "context_type": context_type
                }
                
        except Exception as e:
            self.logger.error(f"❌ RAG 檢索失敗: {str(e)}")
            return {
                "success": False,
                "error": f"RAG 檢索失敗: {str(e)}",
                "query": query
            }
    
    def _apply_domain_filter(self, results: List[Dict[str, Any]], domain_filter: str) -> List[Dict[str, Any]]:
        """應用領域過濾器"""
        if domain_filter == "all":
            return results
        
        filtered_results = []
        
        for result in results:
            content = result.get("content", "").lower()
            metadata = result.get("metadata", {})
            
            should_include = False
            
            if domain_filter == "stars":
                # 星曜相關
                star_keywords = ["紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府", "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍"]
                should_include = any(star in content for star in star_keywords)
            
            elif domain_filter == "palaces":
                # 宮位相關
                palace_keywords = ["命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮", "遷移宮", "奴僕宮", "官祿宮", "田宅宮", "福德宮", "父母宮"]
                should_include = any(palace in content for palace in palace_keywords)
            
            elif domain_filter == "theory":
                # 理論相關
                theory_keywords = ["四化", "大限", "流年", "五行", "陰陽", "干支", "納音"]
                should_include = any(theory in content for theory in theory_keywords)
            
            elif domain_filter == "interpretation":
                # 解釋相關
                interpretation_keywords = ["性格", "命運", "運勢", "感情", "事業", "財運", "健康"]
                should_include = any(keyword in content for keyword in interpretation_keywords)
            
            if should_include:
                filtered_results.append(result)
        
        return filtered_results
    
    async def _post_execute(self, result: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行後處理"""
        if result.get("success", False):
            query = arguments["query"]
            context_type = arguments["context_type"]
            
            if context_type == "search_only":
                results_count = result.get("total_results", 0)
                self.logger.info(f"✅ 知識檢索完成: '{query}' 找到 {results_count} 個結果")
            else:
                self.logger.info(f"✅ RAG 生成完成: '{query}'")
            
            # 添加統計信息
            result["statistics"] = {
                "query_length": len(query),
                "query_type": self._classify_query_type(query),
                "domain_filter": arguments.get("domain_filter", "all")
            }
        else:
            self.logger.warning(f"⚠️ RAG 檢索失敗: {result.get('error', '未知錯誤')}")
        
        return result
    
    def _classify_query_type(self, query: str) -> str:
        """分類查詢類型"""
        query_lower = query.lower()
        
        # 星曜查詢
        star_keywords = ["紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府", "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍"]
        if any(star in query for star in star_keywords):
            return "star_query"
        
        # 宮位查詢
        palace_keywords = ["宮"]
        if any(palace in query for palace in palace_keywords):
            return "palace_query"
        
        # 問題查詢
        question_keywords = ["什麼", "如何", "為什麼", "怎麼", "?", "？"]
        if any(keyword in query for keyword in question_keywords):
            return "question_query"
        
        # 概念查詢
        return "concept_query"
    
    async def cleanup(self):
        """清理資源"""
        if self.rag_system and hasattr(self.rag_system, 'cleanup'):
            await self.rag_system.cleanup()
        await super().cleanup()
