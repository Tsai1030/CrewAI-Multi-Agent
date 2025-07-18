"""
MCP 客戶端工具
為 CrewAI Agents 提供統一的 MCP 工具調用接口
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ...config.settings import get_settings

settings = get_settings()

@dataclass
class MCPToolCall:
    """MCP 工具調用結果"""
    success: bool
    result: Any = None
    error: str = None
    tool_name: str = None
    execution_time: float = 0.0

class MCPClientTool(BaseTool):
    """MCP 客戶端工具基類"""

    name: str = "mcp_client"
    description: str = "MCP 協議客戶端工具"

    def __init__(self, tool_name: str = None, description: str = None, **kwargs):
        # 設置 name 和 description
        if tool_name:
            self.name = tool_name
        if description:
            self.description = description

        super().__init__()

        # 在初始化後設置私有屬性
        object.__setattr__(self, '_mcp_client', kwargs.get('mcp_client', None))
        object.__setattr__(self, '_logger', logging.getLogger(__name__))
        object.__setattr__(self, '_mcp_server_host', settings.mcp.server_host)
        object.__setattr__(self, '_mcp_server_port', settings.mcp.server_port)
        object.__setattr__(self, '_mcp_timeout', settings.mcp.timeout)
        object.__setattr__(self, '_connected', False)
        object.__setattr__(self, '_connection', None)
    
    async def initialize(self):
        """初始化 MCP 客戶端連接"""
        try:
            # 這裡實現 MCP 客戶端連接邏輯
            # 暫時模擬連接成功
            object.__setattr__(self, '_connected', True)
            self._logger.info(f"✅ MCP 客戶端 {self.name} 連接成功")
        except Exception as e:
            self._logger.error(f"❌ MCP 客戶端連接失敗: {str(e)}")
            raise
    
    def _run(self, **kwargs) -> str:
        """同步執行工具（CrewAI 要求的接口）"""
        # 將同步調用轉換為異步調用
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self._async_run(**kwargs))
            return json.dumps(result, ensure_ascii=False, indent=2)
        finally:
            loop.close()
    
    async def _async_run(self, **kwargs) -> Dict[str, Any]:
        """異步執行工具"""
        import time
        start_time = time.time()
        
        try:
            if not getattr(self, '_connected', False):
                await self.initialize()
            
            # 根據工具類型調用相應的處理方法
            if self.name == "ziwei_scraper":
                result = await self._call_ziwei_scraper(**kwargs)
            elif self.name == "rag_knowledge":
                result = await self._call_rag_knowledge(**kwargs)
            elif self.name == "format_output":
                result = await self._call_format_output(**kwargs)
            elif self.name == "data_validator":
                result = await self._call_data_validator(**kwargs)
            else:
                raise ValueError(f"未知的工具類型: {self.name}")
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "result": result,
                "tool_name": self.name,
                "execution_time": execution_time
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"❌ MCP 工具調用失敗 ({self.name}): {str(e)}")

            return {
                "success": False,
                "error": str(e),
                "tool_name": self.name,
                "execution_time": execution_time
            }
    
    async def _call_ziwei_scraper(self, **kwargs) -> Dict[str, Any]:
        """調用紫微斗數爬蟲工具"""
        # 暫時直接調用現有的 ZiweiTool
        from ...mcp.tools.ziwei_tool import ZiweiTool
        
        ziwei_tool = ZiweiTool(logger=self._logger)

        # 提取出生資料
        birth_data = kwargs.get('birth_data', {})
        if isinstance(birth_data, str):
            try:
                birth_data = json.loads(birth_data)
            except:
                # 如果不是 JSON，嘗試從 kwargs 中提取
                birth_data = {
                    'gender': kwargs.get('gender'),
                    'birth_year': kwargs.get('birth_year'),
                    'birth_month': kwargs.get('birth_month'),
                    'birth_day': kwargs.get('birth_day'),
                    'birth_hour': kwargs.get('birth_hour')
                }

        self._logger.info(f"🔮 調用紫微斗數爬蟲: {birth_data}")
        result = ziwei_tool.get_ziwei_chart(birth_data)
        
        return result
    
    async def _call_rag_knowledge(self, **kwargs) -> Dict[str, Any]:
        """調用 RAG 知識檢索工具"""
        # 暫時直接調用現有的 RAG 系統
        from ...rag.rag_system import ZiweiRAGSystem
        
        try:
            rag_system = ZiweiRAGSystem(logger=self._logger)
            
            query = kwargs.get('query', '')
            context_type = kwargs.get('context_type', 'auto')
            top_k = kwargs.get('top_k', 5)
            
            self._logger.info(f"🔍 調用 RAG 知識檢索: {query}")
            
            if context_type == 'search_only':
                # 只搜索，不生成
                results = rag_system.search_knowledge(query, top_k=top_k)
                return {
                    "search_results": results,
                    "query": query
                }
            else:
                # 搜索並生成回答
                result = rag_system.generate_answer(query, context_type=context_type, **kwargs)
                return result
                
        except Exception as e:
            self._logger.error(f"❌ RAG 知識檢索失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": kwargs.get('query', '')
            }
    
    async def _call_format_output(self, **kwargs) -> Dict[str, Any]:
        """調用輸出格式化工具"""
        # 暫時直接調用現有的格式化器
        from ...output.gpt4o_formatter import GPT4oFormatter
        
        try:
            formatter = GPT4oFormatter(logger=self._logger)

            content = kwargs.get('content', '')
            output_format = kwargs.get('output_format', 'detailed')
            domain_type = kwargs.get('domain_type', 'comprehensive')

            self._logger.info(f"📝 調用輸出格式化: {output_format}")
            
            result = await formatter.format_analysis_result(
                content=content,
                output_format=output_format,
                domain_type=domain_type
            )
            
            return result
            
        except Exception as e:
            self._logger.error(f"❌ 輸出格式化失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": kwargs.get('content', '')
            }
    
    async def _call_data_validator(self, **kwargs) -> Dict[str, Any]:
        """調用數據驗證工具"""
        try:
            data = kwargs.get('data', {})
            validation_type = kwargs.get('validation_type', 'ziwei_chart')
            
            self._logger.info(f"✅ 調用數據驗證: {validation_type}")
            
            if validation_type == 'ziwei_chart':
                return self._validate_ziwei_chart_data(data)
            elif validation_type == 'birth_data':
                return self._validate_birth_data(data)
            else:
                return self._validate_generic_data(data)
                
        except Exception as e:
            self._logger.error(f"❌ 數據驗證失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": kwargs.get('data', {})
            }
    
    def _validate_ziwei_chart_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """驗證紫微斗數命盤數據"""
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "completeness_score": 0.0
        }
        
        required_fields = ['basic_info', 'palaces', 'main_stars']
        score = 0
        
        for field in required_fields:
            if field in data and data[field]:
                score += 1
            else:
                validation_result["warnings"].append(f"缺少必要字段: {field}")
        
        validation_result["completeness_score"] = score / len(required_fields)
        
        if validation_result["completeness_score"] < 0.5:
            validation_result["valid"] = False
            validation_result["errors"].append("數據完整性不足")
        
        return validation_result
    
    def _validate_birth_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """驗證出生資料"""
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }
        
        required_fields = ['gender', 'birth_year', 'birth_month', 'birth_day', 'birth_hour']
        
        for field in required_fields:
            if field not in data or not data[field]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"缺少必要字段: {field}")
        
        # 驗證數據範圍
        if 'birth_year' in data:
            year = data['birth_year']
            if not (1900 <= year <= 2100):
                validation_result["warnings"].append("出生年份可能不正確")
        
        return validation_result
    
    def _validate_generic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """通用數據驗證"""
        return {
            "valid": True,
            "warnings": [],
            "errors": [],
            "data_type": type(data).__name__,
            "data_size": len(str(data))
        }
    
    async def cleanup(self):
        """清理連接"""
        try:
            if self._connection:
                # 關閉 MCP 連接
                pass
            object.__setattr__(self, '_connected', False)
            self._logger.info(f"✅ MCP 客戶端 {self.name} 清理完成")
        except Exception as e:
            self._logger.error(f"❌ MCP 客戶端清理失敗: {str(e)}")

# 具體工具類
class ZiweiScraperTool(MCPClientTool):
    """紫微斗數爬蟲工具"""
    name: str = "ziwei_scraper"
    description: str = "從紫微斗數網站獲取命盤數據"
    
    def __init__(self):
        super().__init__(tool_name="ziwei_scraper", description=self.description)

class RAGKnowledgeTool(MCPClientTool):
    """RAG 知識檢索工具"""
    name: str = "rag_knowledge"
    description: str = "從知識庫檢索紫微斗數相關理論和解釋"
    
    def __init__(self):
        super().__init__(tool_name="rag_knowledge", description=self.description)

class FormatOutputTool(MCPClientTool):
    """輸出格式化工具"""
    name: str = "format_output"
    description: str = "將分析結果格式化為指定格式"
    
    def __init__(self):
        super().__init__(tool_name="format_output", description=self.description)

class DataValidatorTool(MCPClientTool):
    """數據驗證工具"""
    name: str = "data_validator"
    description: str = "驗證數據完整性和準確性"
    
    def __init__(self):
        super().__init__(tool_name="data_validator", description=self.description)
