"""
數據驗證 MCP 工具
提供各種數據驗證和質量檢查功能
"""

import json
import re
from typing import Dict, Any, List
from datetime import datetime

from .base_tool import BaseMCPTool

class DataValidatorTool(BaseMCPTool):
    """數據驗證 MCP 工具"""
    
    def __init__(self):
        super().__init__(
            name="data_validator",
            description="驗證數據完整性、準確性和質量"
        )
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """返回工具的 MCP 定義"""
        return {
            "name": "data_validator",
            "description": "驗證各種數據的完整性、準確性和質量，支援多種驗證類型",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": ["object", "string"],
                        "description": "要驗證的數據"
                    },
                    "validation_type": {
                        "type": "string",
                        "description": "驗證類型",
                        "enum": ["birth_data", "ziwei_chart", "analysis_result", "generic"],
                        "default": "generic"
                    },
                    "strict_mode": {
                        "type": "boolean",
                        "description": "是否使用嚴格模式驗證",
                        "default": false
                    },
                    "required_fields": {
                        "type": "array",
                        "description": "必要字段列表",
                        "items": {"type": "string"},
                        "default": []
                    },
                    "custom_rules": {
                        "type": "object",
                        "description": "自定義驗證規則",
                        "default": {}
                    }
                },
                "required": ["data"]
            }
        }
    
    def _validate_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """驗證參數"""
        # 調用父類基本驗證
        base_result = super()._validate_arguments(arguments)
        if not base_result["valid"]:
            return base_result
        
        # 檢查 data
        if "data" not in arguments:
            return {
                "valid": False,
                "error": "缺少必要參數: data"
            }
        
        # 如果 data 是字符串，嘗試解析為 JSON
        data = arguments["data"]
        if isinstance(data, str):
            try:
                arguments["data"] = json.loads(data)
            except json.JSONDecodeError:
                # 保持為字符串，某些驗證類型可能需要字符串
                pass
        
        return {"valid": True, "error": None}
    
    async def _pre_execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行前處理"""
        validation_type = arguments.get("validation_type", "generic")
        strict_mode = arguments.get("strict_mode", False)
        
        self.logger.info(f"✅ 準備驗證數據: 類型={validation_type}, 嚴格模式={strict_mode}")
        
        # 設置默認值
        arguments.setdefault("required_fields", [])
        arguments.setdefault("custom_rules", {})
        
        return arguments
    
    async def _execute_impl(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行數據驗證"""
        data = arguments["data"]
        validation_type = arguments.get("validation_type", "generic")
        strict_mode = arguments.get("strict_mode", False)
        required_fields = arguments.get("required_fields", [])
        custom_rules = arguments.get("custom_rules", {})
        
        try:
            # 根據驗證類型選擇驗證方法
            if validation_type == "birth_data":
                result = self._validate_birth_data(data, strict_mode)
            elif validation_type == "ziwei_chart":
                result = self._validate_ziwei_chart(data, strict_mode)
            elif validation_type == "analysis_result":
                result = self._validate_analysis_result(data, strict_mode)
            else:  # generic
                result = self._validate_generic_data(data, required_fields, custom_rules, strict_mode)
            
            # 添加驗證元數據
            result.update({
                "validation_type": validation_type,
                "strict_mode": strict_mode,
                "data_type": type(data).__name__,
                "data_size": len(str(data))
            })
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 數據驗證失敗: {str(e)}")
            return {
                "valid": False,
                "error": f"數據驗證失敗: {str(e)}",
                "validation_type": validation_type
            }
    
    def _validate_birth_data(self, data: Dict[str, Any], strict_mode: bool) -> Dict[str, Any]:
        """驗證出生資料"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "completeness_score": 0.0
        }
        
        required_fields = ["gender", "birth_year", "birth_month", "birth_day", "birth_hour"]
        score = 0
        
        # 檢查必要字段
        for field in required_fields:
            if field not in data or data[field] is None:
                result["errors"].append(f"缺少必要字段: {field}")
                result["valid"] = False
            else:
                score += 1
        
        if not result["valid"]:
            return result
        
        # 驗證性別
        gender = data.get("gender")
        if gender not in ["男", "女"]:
            if strict_mode:
                result["errors"].append("性別必須是 '男' 或 '女'")
                result["valid"] = False
            else:
                result["warnings"].append("性別格式不標準")
        
        # 驗證出生年份
        birth_year = data.get("birth_year")
        try:
            year = int(birth_year)
            if not (1900 <= year <= 2100):
                result["warnings"].append("出生年份可能不正確")
        except (ValueError, TypeError):
            result["errors"].append("出生年份必須是數字")
            result["valid"] = False
        
        # 驗證出生月份
        birth_month = data.get("birth_month")
        try:
            month = int(birth_month)
            if not (1 <= month <= 12):
                result["errors"].append("出生月份必須在 1-12 之間")
                result["valid"] = False
        except (ValueError, TypeError):
            result["errors"].append("出生月份必須是數字")
            result["valid"] = False
        
        # 驗證出生日期
        birth_day = data.get("birth_day")
        try:
            day = int(birth_day)
            if not (1 <= day <= 31):
                result["errors"].append("出生日期必須在 1-31 之間")
                result["valid"] = False
        except (ValueError, TypeError):
            result["errors"].append("出生日期必須是數字")
            result["valid"] = False
        
        # 驗證出生時辰
        birth_hour = data.get("birth_hour")
        valid_hours = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        if birth_hour not in valid_hours:
            if strict_mode:
                result["errors"].append(f"出生時辰必須是: {', '.join(valid_hours)}")
                result["valid"] = False
            else:
                result["warnings"].append("出生時辰格式不標準")
        
        result["completeness_score"] = score / len(required_fields)
        return result
    
    def _validate_ziwei_chart(self, data: Dict[str, Any], strict_mode: bool) -> Dict[str, Any]:
        """驗證紫微斗數命盤數據"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "completeness_score": 0.0
        }
        
        total_score = 0
        max_score = 0
        
        # 檢查基本信息 (權重: 20%)
        max_score += 20
        if "basic_info" in data and data["basic_info"]:
            basic_info = data["basic_info"]
            if basic_info.get("solar_date"):
                total_score += 5
            if basic_info.get("lunar_date"):
                total_score += 5
            if basic_info.get("ganzhi"):
                total_score += 5
            if basic_info.get("wuxing_ju"):
                total_score += 5
        else:
            result["warnings"].append("缺少基本信息")
        
        # 檢查宮位信息 (權重: 50%)
        max_score += 50
        if "palaces" in data and data["palaces"]:
            palaces = data["palaces"]
            palace_count = len(palaces)
            
            if palace_count >= 12:
                total_score += 30
            elif palace_count >= 8:
                total_score += 20
                result["warnings"].append("宮位數量不足12個")
            else:
                total_score += 10
                result["warnings"].append("宮位數量嚴重不足")
            
            # 檢查宮位是否有星曜
            palaces_with_stars = sum(1 for p in palaces.values() if p.get("stars"))
            if palaces_with_stars >= 8:
                total_score += 20
            elif palaces_with_stars >= 4:
                total_score += 10
                result["warnings"].append("部分宮位缺少星曜")
            else:
                result["warnings"].append("大部分宮位缺少星曜")
        else:
            result["errors"].append("缺少宮位信息")
            if strict_mode:
                result["valid"] = False
        
        # 檢查主星信息 (權重: 30%)
        max_score += 30
        if "main_stars" in data and data["main_stars"]:
            main_stars = data["main_stars"]
            star_count = len(main_stars)
            
            if star_count >= 10:
                total_score += 30
            elif star_count >= 6:
                total_score += 20
                result["warnings"].append("主星數量偏少")
            else:
                total_score += 10
                result["warnings"].append("主星數量嚴重不足")
        else:
            result["warnings"].append("缺少主星信息")
        
        result["completeness_score"] = total_score / max_score if max_score > 0 else 0.0
        
        if result["completeness_score"] < 0.5 and strict_mode:
            result["valid"] = False
            result["errors"].append("數據完整性不足50%")
        
        return result
    
    def _validate_analysis_result(self, data: Any, strict_mode: bool) -> Dict[str, Any]:
        """驗證分析結果"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "quality_score": 0.0
        }
        
        # 轉換為字符串進行分析
        if isinstance(data, dict):
            content = json.dumps(data, ensure_ascii=False)
        else:
            content = str(data)
        
        total_score = 0
        max_score = 0
        
        # 檢查內容長度 (權重: 20%)
        max_score += 20
        if len(content) >= 500:
            total_score += 20
        elif len(content) >= 200:
            total_score += 15
            result["warnings"].append("分析內容偏短")
        else:
            total_score += 5
            result["warnings"].append("分析內容過短")
        
        # 檢查紫微斗數相關內容 (權重: 40%)
        max_score += 40
        ziwei_keywords = ["命宮", "紫微", "天機", "太陽", "宮位", "主星", "四化", "大限"]
        keyword_count = sum(1 for keyword in ziwei_keywords if keyword in content)
        
        if keyword_count >= 6:
            total_score += 40
        elif keyword_count >= 4:
            total_score += 30
            result["warnings"].append("紫微斗數專業術語偏少")
        elif keyword_count >= 2:
            total_score += 20
            result["warnings"].append("紫微斗數專業術語不足")
        else:
            total_score += 5
            result["warnings"].append("缺乏紫微斗數專業內容")
        
        # 檢查結構化程度 (權重: 40%)
        max_score += 40
        structure_indicators = ["。", "：", "、", "\n", "1.", "2.", "•", "-"]
        structure_count = sum(1 for indicator in structure_indicators if indicator in content)
        
        if structure_count >= 6:
            total_score += 40
        elif structure_count >= 4:
            total_score += 30
        elif structure_count >= 2:
            total_score += 20
        else:
            total_score += 10
            result["warnings"].append("內容結構化程度不足")
        
        result["quality_score"] = total_score / max_score if max_score > 0 else 0.0
        
        if result["quality_score"] < 0.6 and strict_mode:
            result["valid"] = False
            result["errors"].append("分析質量不足60%")
        
        return result
    
    def _validate_generic_data(self, data: Any, required_fields: List[str], 
                             custom_rules: Dict[str, Any], strict_mode: bool) -> Dict[str, Any]:
        """通用數據驗證"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "completeness_score": 1.0
        }
        
        # 檢查必要字段
        if required_fields and isinstance(data, dict):
            missing_fields = []
            for field in required_fields:
                if field not in data or data[field] is None:
                    missing_fields.append(field)
            
            if missing_fields:
                result["errors"].extend([f"缺少必要字段: {field}" for field in missing_fields])
                result["completeness_score"] = (len(required_fields) - len(missing_fields)) / len(required_fields)
                if strict_mode:
                    result["valid"] = False
        
        # 應用自定義規則
        for rule_name, rule_config in custom_rules.items():
            try:
                if not self._apply_custom_rule(data, rule_config):
                    if rule_config.get("severity", "warning") == "error":
                        result["errors"].append(f"自定義規則失敗: {rule_name}")
                        if strict_mode:
                            result["valid"] = False
                    else:
                        result["warnings"].append(f"自定義規則警告: {rule_name}")
            except Exception as e:
                result["warnings"].append(f"自定義規則執行失敗: {rule_name} - {str(e)}")
        
        return result
    
    def _apply_custom_rule(self, data: Any, rule_config: Dict[str, Any]) -> bool:
        """應用自定義驗證規則"""
        rule_type = rule_config.get("type", "exists")
        
        if rule_type == "exists":
            field = rule_config.get("field")
            return field in data if isinstance(data, dict) else True
        
        elif rule_type == "regex":
            pattern = rule_config.get("pattern")
            field = rule_config.get("field")
            if isinstance(data, dict) and field in data:
                return bool(re.match(pattern, str(data[field])))
            return True
        
        elif rule_type == "range":
            field = rule_config.get("field")
            min_val = rule_config.get("min")
            max_val = rule_config.get("max")
            if isinstance(data, dict) and field in data:
                try:
                    value = float(data[field])
                    return (min_val is None or value >= min_val) and (max_val is None or value <= max_val)
                except (ValueError, TypeError):
                    return False
            return True
        
        return True
    
    async def _post_execute(self, result: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """執行後處理"""
        validation_type = arguments.get("validation_type", "generic")
        
        if result.get("valid", False):
            score = result.get("completeness_score") or result.get("quality_score", 1.0)
            self.logger.info(f"✅ 數據驗證通過: {validation_type} (分數: {score:.2f})")
        else:
            error_count = len(result.get("errors", []))
            self.logger.warning(f"⚠️ 數據驗證失敗: {validation_type} ({error_count} 個錯誤)")
        
        # 添加統計信息
        result["statistics"] = {
            "error_count": len(result.get("errors", [])),
            "warning_count": len(result.get("warnings", [])),
            "validation_timestamp": datetime.now().isoformat()
        }
        
        return result
