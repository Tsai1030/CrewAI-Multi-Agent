#!/usr/bin/env python3
"""
統一 MCP 服務器
整合所有工具（爬蟲、RAG、格式化、驗證）為統一的 MCP 工具集
"""

import asyncio
import json
import logging
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

# MCP SDK imports (需要安裝 mcp 包)
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("警告: MCP SDK 未安裝，使用模擬實現")
    # 模擬 MCP 類型
    class Tool:
        def __init__(self, name: str, description: str, inputSchema: dict):
            self.name = name
            self.description = description
            self.inputSchema = inputSchema
    
    class TextContent:
        def __init__(self, type: str, text: str):
            self.type = type
            self.text = text
    
    class Server:
        def __init__(self, name: str, version: str):
            self.name = name
            self.version = version
            self.tools = {}
        
        def list_tools(self):
            return list(self.tools.values())
        
        def call_tool(self, name: str, arguments: dict):
            pass

from .tools.ziwei_scraper import ZiweiScraperTool
from .tools.rag_knowledge import RAGKnowledgeTool
from .tools.format_output import FormatOutputTool
from .tools.data_validator import DataValidatorTool
from .utils.tool_registry import ToolRegistry
from .utils.error_handler import MCPErrorHandler

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedMCPServer:
    """統一 MCP 服務器"""
    
    def __init__(self):
        self.server = Server("ziwei-unified-mcp-server", "1.0.0")
        self.tool_registry = ToolRegistry()
        self.error_handler = MCPErrorHandler()
        
        # 工具實例
        self.tools = {}
        
        # 初始化工具
        self._initialize_tools()
        self._register_handlers()
    
    def _initialize_tools(self):
        """初始化所有工具"""
        try:
            # 創建工具實例
            self.tools = {
                "ziwei_scraper": ZiweiScraperTool(),
                "rag_knowledge": RAGKnowledgeTool(),
                "format_output": FormatOutputTool(),
                "data_validator": DataValidatorTool()
            }
            
            # 註冊工具到註冊表
            for tool_name, tool_instance in self.tools.items():
                self.tool_registry.register_tool(tool_name, tool_instance)
            
            logger.info(f"✅ 初始化了 {len(self.tools)} 個工具")
            
        except Exception as e:
            logger.error(f"❌ 工具初始化失敗: {str(e)}")
            raise
    
    def _register_handlers(self):
        """註冊 MCP 處理器"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """列出所有可用工具"""
            tools = []
            
            for tool_name, tool_instance in self.tools.items():
                tool_def = tool_instance.get_tool_definition()
                tools.append(Tool(
                    name=tool_def["name"],
                    description=tool_def["description"],
                    inputSchema=tool_def["parameters"]
                ))
            
            logger.info(f"📋 列出 {len(tools)} 個工具")
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """調用指定工具"""
            start_time = datetime.now()
            
            try:
                logger.info(f"🔧 調用工具: {name} with {arguments}")
                
                # 檢查工具是否存在
                if name not in self.tools:
                    raise ValueError(f"未知工具: {name}")
                
                # 獲取工具實例
                tool_instance = self.tools[name]
                
                # 執行工具
                result = await tool_instance.execute(arguments)
                
                # 記錄執行時間
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"✅ 工具 {name} 執行完成，耗時 {execution_time:.2f}s")
                
                # 格式化結果
                if isinstance(result, dict):
                    result_text = json.dumps(result, ensure_ascii=False, indent=2)
                else:
                    result_text = str(result)
                
                return [TextContent(type="text", text=result_text)]
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                error_msg = f"❌ 工具 {name} 執行失敗: {str(e)} (耗時 {execution_time:.2f}s)"
                logger.error(error_msg)
                
                # 使用錯誤處理器
                error_response = self.error_handler.handle_tool_error(name, str(e), arguments)
                
                return [TextContent(type="text", text=json.dumps(error_response, ensure_ascii=False, indent=2))]
    
    async def run(self):
        """運行 MCP 服務器"""
        try:
            logger.info("🚀 啟動統一 MCP 服務器...")
            
            # 如果有真正的 MCP SDK，使用 stdio_server
            if 'mcp.server.stdio' in sys.modules:
                async with stdio_server() as (read_stream, write_stream):
                    await self.server.run(read_stream, write_stream)
            else:
                # 模擬運行
                logger.info("📡 MCP 服務器運行中 (模擬模式)...")
                while True:
                    await asyncio.sleep(1)
                    
        except KeyboardInterrupt:
            logger.info("🛑 收到停止信號，正在關閉服務器...")
        except Exception as e:
            logger.error(f"❌ MCP 服務器運行失敗: {str(e)}")
            raise
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """清理資源"""
        try:
            # 清理所有工具
            for tool_name, tool_instance in self.tools.items():
                if hasattr(tool_instance, 'cleanup'):
                    await tool_instance.cleanup()
            
            logger.info("✅ MCP 服務器清理完成")
        except Exception as e:
            logger.error(f"❌ MCP 服務器清理失敗: {str(e)}")

# 獨立運行的 MCP 服務器
class StandaloneMCPServer:
    """獨立運行的 MCP 服務器（用於測試）"""
    
    def __init__(self):
        self.unified_server = UnifiedMCPServer()
    
    async def test_tools(self):
        """測試所有工具"""
        logger.info("🧪 開始測試所有工具...")
        
        # 測試數據
        test_birth_data = {
            "gender": "男",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "birth_hour": "午"
        }
        
        # 測試紫微斗數爬蟲
        try:
            logger.info("🔮 測試紫微斗數爬蟲...")
            scraper_result = await self.unified_server.tools["ziwei_scraper"].execute({
                "birth_data": test_birth_data
            })
            logger.info(f"✅ 爬蟲測試成功: {scraper_result.get('success', False)}")
        except Exception as e:
            logger.error(f"❌ 爬蟲測試失敗: {str(e)}")
        
        # 測試 RAG 知識檢索
        try:
            logger.info("🔍 測試 RAG 知識檢索...")
            rag_result = await self.unified_server.tools["rag_knowledge"].execute({
                "query": "紫微星的特質",
                "context_type": "search_only",
                "top_k": 3
            })
            logger.info(f"✅ RAG 測試成功: {len(rag_result.get('search_results', []))} 個結果")
        except Exception as e:
            logger.error(f"❌ RAG 測試失敗: {str(e)}")
        
        # 測試數據驗證
        try:
            logger.info("✅ 測試數據驗證...")
            validator_result = await self.unified_server.tools["data_validator"].execute({
                "data": test_birth_data,
                "validation_type": "birth_data"
            })
            logger.info(f"✅ 驗證測試成功: {validator_result.get('valid', False)}")
        except Exception as e:
            logger.error(f"❌ 驗證測試失敗: {str(e)}")
        
        # 測試格式化輸出
        try:
            logger.info("📝 測試格式化輸出...")
            format_result = await self.unified_server.tools["format_output"].execute({
                "content": "這是一個測試內容",
                "output_format": "detailed",
                "domain_type": "comprehensive"
            })
            logger.info(f"✅ 格式化測試成功: {format_result.get('success', False)}")
        except Exception as e:
            logger.error(f"❌ 格式化測試失敗: {str(e)}")
        
        logger.info("🎉 工具測試完成")

async def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="統一 MCP 服務器")
    parser.add_argument("--test", action="store_true", help="運行工具測試")
    parser.add_argument("--standalone", action="store_true", help="獨立運行模式")
    
    args = parser.parse_args()
    
    if args.test:
        # 測試模式
        standalone_server = StandaloneMCPServer()
        await standalone_server.test_tools()
    elif args.standalone:
        # 獨立運行模式
        standalone_server = StandaloneMCPServer()
        await standalone_server.unified_server.run()
    else:
        # 標準 MCP 服務器模式
        server = UnifiedMCPServer()
        await server.run()

if __name__ == "__main__":
    asyncio.run(main())
