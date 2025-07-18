"""
MCP 工具基類
定義所有 MCP 工具的通用接口和行為
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class BaseMCPTool(ABC):
    """MCP 工具基類"""
    
    def __init__(self, name: str, description: str, logger=None):
        self.name = name
        self.description = description
        self.logger = logger or logging.getLogger(__name__)
        
        # 執行統計
        self.execution_count = 0
        self.total_execution_time = 0.0
        self.last_execution_time = None
        
        # 初始化狀態
        self._initialized = False
    
    @abstractmethod
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        返回工具的 MCP 定義
        
        Returns:
            包含 name, description, parameters 的字典
        """
        pass
    
    @abstractmethod
    async def _execute_impl(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        工具的具體實現邏輯
        
        Args:
            arguments: 工具參數
            
        Returns:
            執行結果
        """
        pass
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        執行工具（包含通用邏輯）
        
        Args:
            arguments: 工具參數
            
        Returns:
            執行結果
        """
        start_time = time.time()
        self.execution_count += 1
        
        try:
            # 初始化檢查
            if not self._initialized:
                await self.initialize()
            
            # 參數驗證
            validation_result = self._validate_arguments(arguments)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": f"參數驗證失敗: {validation_result['error']}",
                    "tool_name": self.name
                }
            
            # 執行前處理
            processed_arguments = await self._pre_execute(arguments)
            
            # 執行主邏輯
            self.logger.info(f"🔧 執行工具 {self.name}...")
            result = await self._execute_impl(processed_arguments)
            
            # 執行後處理
            final_result = await self._post_execute(result, processed_arguments)
            
            # 更新統計
            execution_time = time.time() - start_time
            self.total_execution_time += execution_time
            self.last_execution_time = datetime.now()
            
            self.logger.info(f"✅ 工具 {self.name} 執行成功，耗時 {execution_time:.2f}s")
            
            # 添加元數據
            if isinstance(final_result, dict):
                final_result.update({
                    "tool_name": self.name,
                    "execution_time": execution_time,
                    "timestamp": self.last_execution_time.isoformat()
                })
            
            return final_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"❌ 工具 {self.name} 執行失敗: {str(e)}")
            
            return {
                "success": False,
                "error": str(e),
                "tool_name": self.name,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
    
    async def initialize(self):
        """初始化工具（子類可重寫）"""
        self._initialized = True
        self.logger.info(f"✅ 工具 {self.name} 初始化完成")
    
    def _validate_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        驗證參數（子類可重寫）
        
        Args:
            arguments: 工具參數
            
        Returns:
            驗證結果 {"valid": bool, "error": str}
        """
        # 基本驗證：檢查參數是否為字典
        if not isinstance(arguments, dict):
            return {
                "valid": False,
                "error": "參數必須是字典類型"
            }
        
        return {"valid": True, "error": None}
    
    async def _pre_execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        執行前處理（子類可重寫）
        
        Args:
            arguments: 原始參數
            
        Returns:
            處理後的參數
        """
        return arguments
    
    async def _post_execute(self, result: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        執行後處理（子類可重寫）
        
        Args:
            result: 執行結果
            arguments: 執行參數
            
        Returns:
            處理後的結果
        """
        return result
    
    async def cleanup(self):
        """清理資源（子類可重寫）"""
        self.logger.info(f"🧹 工具 {self.name} 清理完成")
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取執行統計"""
        avg_execution_time = (
            self.total_execution_time / self.execution_count 
            if self.execution_count > 0 else 0
        )
        
        return {
            "tool_name": self.name,
            "execution_count": self.execution_count,
            "total_execution_time": self.total_execution_time,
            "average_execution_time": avg_execution_time,
            "last_execution_time": self.last_execution_time.isoformat() if self.last_execution_time else None
        }
    
    def __str__(self) -> str:
        return f"MCPTool({self.name})"
    
    def __repr__(self) -> str:
        return f"MCPTool(name='{self.name}', description='{self.description[:50]}...')"
