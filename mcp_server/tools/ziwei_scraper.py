"""
紫微斗數爬蟲 MCP 工具
封裝現有的 ZiweiTool 為 MCP 工具
"""

import json
import sys
import os
from typing import Dict, Any

# 添加項目根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .base_tool import BaseMCPTool

class ZiweiScraperTool(BaseMCPTool):
    """紫微斗數爬蟲 MCP 工具"""
    
    def __init__(self):
        super().__init__(
            name="ziwei_scraper",
            description="從紫微斗數網站獲取完整命盤數據"
        )
        self.ziwei_tool = None
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """返回工具的 MCP 定義"""
        return {
            "name": "ziwei_scraper",
            "description": "從紫微斗數網站獲取完整命盤數據，包含十二宮位、主星配置、四化等信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "birth_data": {
                        "type": "object",
                        "description": "出生資料",
                        "properties": {
                            "gender": {
                                "type": "string",
                                "description": "性別（男/女）",
                                "enum": ["男", "女"]
                            },
                            "birth_year": {
                                "type": "integer",
                                "description": "出生年份（西元年）",
                                "minimum": 1900,
                                "maximum": 2100
                            },
                            "birth_month": {
                                "type": "integer",
                                "description": "出生月份",
                                "minimum": 1,
                                "maximum": 12
                            },
                            "birth_day": {
                                "type": "integer",
                                "description": "出生日期",
                                "minimum": 1,
                                "maximum": 31
                            },
                            "birth_hour": {
                                "type": "string",
                                "description": "出生時辰（子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥）"
                            }
                        },
                        "required": ["gender", "birth_year", "birth_month", "birth_day", "birth_hour"]
                    }
                },
                "required": ["birth_data"]
            }
        }
    
    async def initialize(self):
        """初始化爬蟲工具"""
        try:
            from src.mcp.tools.ziwei_tool import ZiweiTool
            self.ziwei_tool = ZiweiTool(logger=self.logger)
            await super().initialize()
        except ImportError as e:
            self.logger.error(f"❌ 無法導入 ZiweiTool: {str(e)}")
            raise
    
    def _validate_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """驗證參數"""
        # 調用父類基本驗證
        base_result = super()._validate_arguments(arguments)
        if not base_result["valid"]:
            return base_result
        
        # 檢查 birth_data
        if "birth_data" not in arguments:
            return {
                "valid": False,
                "error": "缺少必要參數: birth_data"
            }
        
        birth_data = arguments["birth_data"]
        
        # 如果 birth_data 是字符串，嘗試解析為 JSON
        if isinstance(birth_data, str):
            try:
                birth_data = json.loads(birth_data)
                arguments["birth_data"] = birth_data
            except json.JSONDecodeError:
                return {
                    "valid": False,
                    "error": "birth_data 不是有效的 JSON 格式"
                }
        
        # 檢查必要字段
        required_fields = ["gender", "birth_year", "birth_month", "birth_day", "birth_hour"]
        for field in required_fields:
            if field not in birth_data:
                return {
                    "valid": False,
                    "error": f"birth_data 缺少必要字段: {field}"
                }
        
        # 驗證數據範圍
        year = birth_data.get("birth_year")
        if not isinstance(year, int) or not (1900 <= year <= 2100):
            return {
                "valid": False,
                "error": "birth_year 必須是 1900-2100 之間的整數"
            }
        
        month = birth_data.get("birth_month")
        if not isinstance(month, int) or not (1 <= month <= 12):
            return {
                "valid": False,
                "error": "birth_month 必須是 1-12 之間的整數"
            }
        
        day = birth_data.get("birth_day")
        if not isinstance(day, int) or not (1 <= day <= 31):
            return {
                "valid": False,
                "error": "birth_day 必須是 1-31 之間的整數"
            }
        
        gender = birth_data.get("gender")
        if gender not in ["男", "女"]:
            return {
                "valid": False,
                "error": "gender 必須是 '男' 或 '女'"
            }
        
        hour = birth_data.get("birth_hour")
        valid_hours = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        if hour not in valid_hours:
            return {
                "valid": False,
                "error": f"birth_hour 必須是以下之一: {', '.join(valid_hours)}"
            }
        
        return {"valid": True, "error": None}
    
    async def _pre_execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行前處理"""
        # 記錄請求信息
        birth_data = arguments["birth_data"]
        self.logger.info(f"🔮 準備獲取命盤: {birth_data['gender']} {birth_data['birth_year']}/{birth_data['birth_month']}/{birth_data['birth_day']} {birth_data['birth_hour']}時")
        
        return arguments
    
    async def _execute_impl(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行爬蟲獲取命盤數據"""
        birth_data = arguments["birth_data"]
        
        try:
            # 調用現有的 ZiweiTool
            result = self.ziwei_tool.get_ziwei_chart(birth_data)
            
            # 檢查結果
            if not result.get("success", False):
                return {
                    "success": False,
                    "error": result.get("error", "未知錯誤"),
                    "birth_data": birth_data
                }
            
            # 提取和整理數據
            chart_data = result.get("data", {})
            
            return {
                "success": True,
                "chart_data": chart_data,
                "birth_data": birth_data,
                "data_quality": result.get("data_quality", {}),
                "source": "fate.windada.com",
                "extraction_method": "web_scraping"
            }
            
        except Exception as e:
            self.logger.error(f"❌ 爬蟲執行失敗: {str(e)}")
            return {
                "success": False,
                "error": f"爬蟲執行失敗: {str(e)}",
                "birth_data": birth_data
            }
    
    async def _post_execute(self, result: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行後處理"""
        if result.get("success", False):
            chart_data = result.get("chart_data", {})
            palaces_count = len(chart_data.get("palaces", {}))
            stars_count = len(chart_data.get("main_stars", []))
            
            self.logger.info(f"✅ 成功獲取命盤: {palaces_count} 個宮位, {stars_count} 個主星")
            
            # 添加統計信息
            result["statistics"] = {
                "palaces_count": palaces_count,
                "main_stars_count": stars_count,
                "has_basic_info": bool(chart_data.get("basic_info")),
                "data_completeness": self._calculate_completeness(chart_data)
            }
        else:
            self.logger.warning(f"⚠️ 命盤獲取失敗: {result.get('error', '未知錯誤')}")
        
        return result
    
    def _calculate_completeness(self, chart_data: Dict[str, Any]) -> float:
        """計算數據完整性分數"""
        total_score = 0
        max_score = 0
        
        # 基本信息 (權重: 20%)
        max_score += 20
        if chart_data.get("basic_info"):
            basic_info = chart_data["basic_info"]
            if basic_info.get("solar_date"):
                total_score += 5
            if basic_info.get("lunar_date"):
                total_score += 5
            if basic_info.get("ganzhi"):
                total_score += 5
            if basic_info.get("wuxing_ju"):
                total_score += 5
        
        # 宮位信息 (權重: 50%)
        max_score += 50
        palaces = chart_data.get("palaces", {})
        if len(palaces) >= 12:  # 應該有12個宮位
            total_score += 30
            # 檢查宮位是否有星曜
            palaces_with_stars = sum(1 for p in palaces.values() if p.get("stars"))
            if palaces_with_stars >= 6:  # 至少一半宮位有星曜
                total_score += 20
        
        # 主星信息 (權重: 30%)
        max_score += 30
        main_stars = chart_data.get("main_stars", [])
        if len(main_stars) >= 10:  # 應該有14主星，至少10個
            total_score += 30
        elif len(main_stars) >= 5:
            total_score += 15
        
        return total_score / max_score if max_score > 0 else 0.0

    async def cleanup(self):
        """清理資源"""
        if self.ziwei_tool and hasattr(self.ziwei_tool, 'session'):
            self.ziwei_tool.session.close()
        await super().cleanup()
