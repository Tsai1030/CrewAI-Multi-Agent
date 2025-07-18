"""
MCP 工具註冊管理器
負責管理所有 MCP 工具的註冊、發現和調用
"""

import logging
from typing import Dict, Any, List, Optional, Type
from datetime import datetime

class ToolRegistry:
    """MCP 工具註冊管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tools = {}  # tool_name -> tool_instance
        self.tool_definitions = {}  # tool_name -> tool_definition
        self.tool_statistics = {}  # tool_name -> statistics
        
    def register_tool(self, tool_name: str, tool_instance: Any) -> bool:
        """
        註冊工具
        
        Args:
            tool_name: 工具名稱
            tool_instance: 工具實例
            
        Returns:
            註冊是否成功
        """
        try:
            # 檢查工具是否已存在
            if tool_name in self.tools:
                self.logger.warning(f"⚠️ 工具 {tool_name} 已存在，將被覆蓋")
            
            # 驗證工具實例
            if not hasattr(tool_instance, 'get_tool_definition'):
                raise ValueError(f"工具 {tool_name} 缺少 get_tool_definition 方法")
            
            if not hasattr(tool_instance, 'execute'):
                raise ValueError(f"工具 {tool_name} 缺少 execute 方法")
            
            # 獲取工具定義
            tool_definition = tool_instance.get_tool_definition()
            
            # 註冊工具
            self.tools[tool_name] = tool_instance
            self.tool_definitions[tool_name] = tool_definition
            self.tool_statistics[tool_name] = {
                "registered_at": datetime.now().isoformat(),
                "call_count": 0,
                "total_execution_time": 0.0,
                "last_called": None,
                "error_count": 0
            }
            
            self.logger.info(f"✅ 工具 {tool_name} 註冊成功")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 工具 {tool_name} 註冊失敗: {str(e)}")
            return False
    
    def unregister_tool(self, tool_name: str) -> bool:
        """
        取消註冊工具
        
        Args:
            tool_name: 工具名稱
            
        Returns:
            取消註冊是否成功
        """
        try:
            if tool_name not in self.tools:
                self.logger.warning(f"⚠️ 工具 {tool_name} 不存在")
                return False
            
            # 清理工具
            tool_instance = self.tools[tool_name]
            if hasattr(tool_instance, 'cleanup'):
                tool_instance.cleanup()
            
            # 移除註冊
            del self.tools[tool_name]
            del self.tool_definitions[tool_name]
            del self.tool_statistics[tool_name]
            
            self.logger.info(f"✅ 工具 {tool_name} 取消註冊成功")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 工具 {tool_name} 取消註冊失敗: {str(e)}")
            return False
    
    def get_tool(self, tool_name: str) -> Optional[Any]:
        """
        獲取工具實例
        
        Args:
            tool_name: 工具名稱
            
        Returns:
            工具實例或 None
        """
        return self.tools.get(tool_name)
    
    def get_tool_definition(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        獲取工具定義
        
        Args:
            tool_name: 工具名稱
            
        Returns:
            工具定義或 None
        """
        return self.tool_definitions.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """
        列出所有已註冊的工具名稱
        
        Returns:
            工具名稱列表
        """
        return list(self.tools.keys())
    
    def list_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        列出所有工具定義
        
        Returns:
            工具定義列表
        """
        return list(self.tool_definitions.values())
    
    def tool_exists(self, tool_name: str) -> bool:
        """
        檢查工具是否存在
        
        Args:
            tool_name: 工具名稱
            
        Returns:
            工具是否存在
        """
        return tool_name in self.tools
    
    def update_tool_statistics(self, tool_name: str, execution_time: float, success: bool):
        """
        更新工具統計信息
        
        Args:
            tool_name: 工具名稱
            execution_time: 執行時間
            success: 是否成功
        """
        if tool_name in self.tool_statistics:
            stats = self.tool_statistics[tool_name]
            stats["call_count"] += 1
            stats["total_execution_time"] += execution_time
            stats["last_called"] = datetime.now().isoformat()
            
            if not success:
                stats["error_count"] += 1
    
    def get_tool_statistics(self, tool_name: str = None) -> Dict[str, Any]:
        """
        獲取工具統計信息
        
        Args:
            tool_name: 工具名稱，如果為 None 則返回所有工具統計
            
        Returns:
            統計信息
        """
        if tool_name:
            return self.tool_statistics.get(tool_name, {})
        else:
            return self.tool_statistics.copy()
    
    def get_registry_summary(self) -> Dict[str, Any]:
        """
        獲取註冊表摘要
        
        Returns:
            註冊表摘要信息
        """
        total_calls = sum(stats["call_count"] for stats in self.tool_statistics.values())
        total_errors = sum(stats["error_count"] for stats in self.tool_statistics.values())
        total_execution_time = sum(stats["total_execution_time"] for stats in self.tool_statistics.values())
        
        return {
            "total_tools": len(self.tools),
            "tool_names": list(self.tools.keys()),
            "total_calls": total_calls,
            "total_errors": total_errors,
            "total_execution_time": total_execution_time,
            "average_execution_time": total_execution_time / total_calls if total_calls > 0 else 0,
            "error_rate": total_errors / total_calls if total_calls > 0 else 0,
            "most_used_tool": self._get_most_used_tool(),
            "registry_created": datetime.now().isoformat()
        }
    
    def _get_most_used_tool(self) -> Optional[str]:
        """獲取使用最多的工具"""
        if not self.tool_statistics:
            return None
        
        most_used = max(
            self.tool_statistics.items(),
            key=lambda x: x[1]["call_count"]
        )
        
        return most_used[0] if most_used[1]["call_count"] > 0 else None
    
    def validate_all_tools(self) -> Dict[str, Any]:
        """
        驗證所有已註冊的工具
        
        Returns:
            驗證結果
        """
        validation_results = {}
        
        for tool_name, tool_instance in self.tools.items():
            try:
                # 檢查必要方法
                required_methods = ["get_tool_definition", "execute"]
                missing_methods = []
                
                for method in required_methods:
                    if not hasattr(tool_instance, method):
                        missing_methods.append(method)
                
                # 檢查工具定義
                tool_definition = tool_instance.get_tool_definition()
                required_definition_keys = ["name", "description", "parameters"]
                missing_definition_keys = []
                
                for key in required_definition_keys:
                    if key not in tool_definition:
                        missing_definition_keys.append(key)
                
                validation_results[tool_name] = {
                    "valid": len(missing_methods) == 0 and len(missing_definition_keys) == 0,
                    "missing_methods": missing_methods,
                    "missing_definition_keys": missing_definition_keys,
                    "tool_definition": tool_definition
                }
                
            except Exception as e:
                validation_results[tool_name] = {
                    "valid": False,
                    "error": str(e)
                }
        
        return validation_results
    
    def cleanup_all_tools(self):
        """清理所有工具"""
        for tool_name, tool_instance in self.tools.items():
            try:
                if hasattr(tool_instance, 'cleanup'):
                    tool_instance.cleanup()
                self.logger.info(f"✅ 工具 {tool_name} 清理完成")
            except Exception as e:
                self.logger.error(f"❌ 工具 {tool_name} 清理失敗: {str(e)}")
        
        self.tools.clear()
        self.tool_definitions.clear()
        self.tool_statistics.clear()
        
        self.logger.info("✅ 所有工具清理完成")
    
    def __len__(self) -> int:
        """返回已註冊工具數量"""
        return len(self.tools)
    
    def __contains__(self, tool_name: str) -> bool:
        """檢查工具是否在註冊表中"""
        return tool_name in self.tools
    
    def __iter__(self):
        """迭代工具名稱"""
        return iter(self.tools.keys())
    
    def __str__(self) -> str:
        return f"ToolRegistry({len(self.tools)} tools: {list(self.tools.keys())})"
    
    def __repr__(self) -> str:
        return f"ToolRegistry(tools={list(self.tools.keys())})"
