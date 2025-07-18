"""
輸出格式化 MCP 工具
封裝現有的格式化器為 MCP 工具
"""

import json
import sys
import os
from typing import Dict, Any

# 添加項目根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .base_tool import BaseMCPTool

class FormatOutputTool(BaseMCPTool):
    """輸出格式化 MCP 工具"""
    
    def __init__(self):
        super().__init__(
            name="format_output",
            description="將分析結果格式化為指定的輸出格式"
        )
        self.formatter = None
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """返回工具的 MCP 定義"""
        return {
            "name": "format_output",
            "description": "將分析結果格式化為指定的輸出格式，支援多種格式和樣式",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "要格式化的內容"
                    },
                    "output_format": {
                        "type": "string",
                        "description": "輸出格式",
                        "enum": ["detailed", "summary", "json", "markdown", "narrative"],
                        "default": "detailed"
                    },
                    "domain_type": {
                        "type": "string",
                        "description": "分析領域類型",
                        "enum": ["comprehensive", "love", "wealth", "future"],
                        "default": "comprehensive"
                    },
                    "style": {
                        "type": "string",
                        "description": "輸出風格",
                        "enum": ["professional", "casual", "poetic", "scientific"],
                        "default": "professional"
                    },
                    "include_metadata": {
                        "type": "boolean",
                        "description": "是否包含元數據",
                        "default": true
                    },
                    "language": {
                        "type": "string",
                        "description": "輸出語言",
                        "enum": ["zh-TW", "zh-CN", "en"],
                        "default": "zh-TW"
                    }
                },
                "required": ["content"]
            }
        }
    
    async def initialize(self):
        """初始化格式化器"""
        try:
            from src.output.gpt4o_formatter import GPT4oFormatter
            self.formatter = GPT4oFormatter(logger=self.logger)
            await super().initialize()
        except ImportError as e:
            self.logger.error(f"❌ 無法導入 GPT4oFormatter: {str(e)}")
            raise
    
    def _validate_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """驗證參數"""
        # 調用父類基本驗證
        base_result = super()._validate_arguments(arguments)
        if not base_result["valid"]:
            return base_result
        
        # 檢查 content
        if "content" not in arguments:
            return {
                "valid": False,
                "error": "缺少必要參數: content"
            }
        
        content = arguments["content"]
        if not isinstance(content, str):
            # 如果不是字符串，嘗試轉換
            try:
                if isinstance(content, dict):
                    arguments["content"] = json.dumps(content, ensure_ascii=False, indent=2)
                else:
                    arguments["content"] = str(content)
            except Exception:
                return {
                    "valid": False,
                    "error": "content 無法轉換為字符串"
                }
        
        # 檢查內容長度
        if len(arguments["content"]) > 100000:  # 100KB 限制
            return {
                "valid": False,
                "error": "content 內容過長，超過 100KB 限制"
            }
        
        return {"valid": True, "error": None}
    
    async def _pre_execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行前處理"""
        content_length = len(arguments["content"])
        output_format = arguments.get("output_format", "detailed")
        domain_type = arguments.get("domain_type", "comprehensive")
        
        self.logger.info(f"📝 準備格式化內容: {content_length} 字符 -> {output_format} 格式 ({domain_type})")
        
        # 設置默認值
        arguments.setdefault("style", "professional")
        arguments.setdefault("include_metadata", True)
        arguments.setdefault("language", "zh-TW")
        
        return arguments
    
    async def _execute_impl(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行格式化"""
        content = arguments["content"]
        output_format = arguments["output_format"]
        domain_type = arguments["domain_type"]
        style = arguments["style"]
        include_metadata = arguments["include_metadata"]
        language = arguments["language"]
        
        try:
            # 調用現有的格式化器
            result = await self.formatter.format_analysis_result(
                content=content,
                output_format=output_format,
                domain_type=domain_type,
                style=style,
                include_metadata=include_metadata,
                language=language
            )
            
            if not result.get("success", False):
                return {
                    "success": False,
                    "error": result.get("error", "格式化失敗"),
                    "original_content": content[:200] + "..." if len(content) > 200 else content
                }
            
            formatted_content = result.get("formatted_result", content)
            
            return {
                "success": True,
                "formatted_content": formatted_content,
                "original_length": len(content),
                "formatted_length": len(formatted_content),
                "output_format": output_format,
                "domain_type": domain_type,
                "style": style,
                "language": language
            }
            
        except Exception as e:
            self.logger.error(f"❌ 格式化執行失敗: {str(e)}")
            return {
                "success": False,
                "error": f"格式化執行失敗: {str(e)}",
                "original_content": content[:200] + "..." if len(content) > 200 else content
            }
    
    async def _post_execute(self, result: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行後處理"""
        if result.get("success", False):
            original_length = result.get("original_length", 0)
            formatted_length = result.get("formatted_length", 0)
            output_format = result.get("output_format", "unknown")
            
            compression_ratio = formatted_length / original_length if original_length > 0 else 0
            
            self.logger.info(f"✅ 格式化完成: {original_length} -> {formatted_length} 字符 ({output_format})")
            
            # 添加統計信息
            result["statistics"] = {
                "compression_ratio": compression_ratio,
                "format_efficiency": self._calculate_format_efficiency(arguments, result),
                "content_type": self._detect_content_type(arguments["content"])
            }
        else:
            self.logger.warning(f"⚠️ 格式化失敗: {result.get('error', '未知錯誤')}")
        
        return result
    
    def _calculate_format_efficiency(self, arguments: Dict[str, Any], result: Dict[str, Any]) -> float:
        """計算格式化效率"""
        original_length = result.get("original_length", 0)
        formatted_length = result.get("formatted_length", 0)
        output_format = arguments.get("output_format", "detailed")
        
        if original_length == 0:
            return 0.0
        
        # 根據格式類型調整效率計算
        if output_format == "summary":
            # 摘要格式：越短越好（但不能太短）
            ideal_ratio = 0.3  # 理想壓縮比 30%
            actual_ratio = formatted_length / original_length
            efficiency = 1.0 - abs(actual_ratio - ideal_ratio)
        elif output_format == "detailed":
            # 詳細格式：可以比原文長
            efficiency = min(1.0, formatted_length / (original_length * 1.5))
        else:
            # 其他格式：保持相近長度
            ratio = formatted_length / original_length
            efficiency = 1.0 - abs(ratio - 1.0)
        
        return max(0.0, min(1.0, efficiency))
    
    def _detect_content_type(self, content: str) -> str:
        """檢測內容類型"""
        content_lower = content.lower()
        
        # JSON 格式
        if content.strip().startswith('{') and content.strip().endswith('}'):
            return "json"
        
        # Markdown 格式
        if any(marker in content for marker in ['#', '**', '*', '```']):
            return "markdown"
        
        # 命理分析內容
        ziwei_keywords = ["命宮", "紫微", "天機", "太陽", "宮位", "主星"]
        if any(keyword in content for keyword in ziwei_keywords):
            return "ziwei_analysis"
        
        # 結構化數據
        if any(marker in content for marker in [':', '：', '•', '-', '1.', '2.']):
            return "structured_text"
        
        # 純文本
        return "plain_text"
    
    async def cleanup(self):
        """清理資源"""
        if self.formatter and hasattr(self.formatter, 'cleanup'):
            await self.formatter.cleanup()
        await super().cleanup()
