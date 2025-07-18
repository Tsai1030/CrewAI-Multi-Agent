"""
MCP 錯誤處理器
提供統一的錯誤處理和恢復機制
"""

import logging
import traceback
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class ErrorSeverity(Enum):
    """錯誤嚴重程度"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """錯誤類別"""
    VALIDATION = "validation"
    EXECUTION = "execution"
    NETWORK = "network"
    TIMEOUT = "timeout"
    RESOURCE = "resource"
    UNKNOWN = "unknown"

class MCPErrorHandler:
    """MCP 錯誤處理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_history = []
        self.error_patterns = {}
        self.recovery_strategies = {}
        
        # 初始化錯誤模式和恢復策略
        self._initialize_error_patterns()
        self._initialize_recovery_strategies()
    
    def _initialize_error_patterns(self):
        """初始化錯誤模式識別"""
        self.error_patterns = {
            # 網絡相關錯誤
            "network": [
                "connection", "timeout", "network", "socket", "dns",
                "連接", "超時", "網絡", "網路"
            ],
            # 驗證相關錯誤
            "validation": [
                "validation", "invalid", "missing", "required", "format",
                "驗證", "無效", "缺少", "必要", "格式"
            ],
            # 資源相關錯誤
            "resource": [
                "memory", "disk", "cpu", "resource", "limit",
                "內存", "磁盤", "資源", "限制"
            ],
            # 執行相關錯誤
            "execution": [
                "execution", "runtime", "process", "thread",
                "執行", "運行", "進程", "線程"
            ]
        }
    
    def _initialize_recovery_strategies(self):
        """初始化恢復策略"""
        self.recovery_strategies = {
            ErrorCategory.NETWORK: {
                "retry_count": 3,
                "retry_delay": 2.0,
                "fallback_action": "use_cached_data"
            },
            ErrorCategory.VALIDATION: {
                "retry_count": 1,
                "retry_delay": 0.0,
                "fallback_action": "use_default_values"
            },
            ErrorCategory.TIMEOUT: {
                "retry_count": 2,
                "retry_delay": 5.0,
                "fallback_action": "reduce_complexity"
            },
            ErrorCategory.RESOURCE: {
                "retry_count": 1,
                "retry_delay": 1.0,
                "fallback_action": "cleanup_and_retry"
            },
            ErrorCategory.EXECUTION: {
                "retry_count": 2,
                "retry_delay": 1.0,
                "fallback_action": "alternative_method"
            }
        }
    
    def handle_tool_error(self, tool_name: str, error_message: str, 
                         arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        處理工具錯誤
        
        Args:
            tool_name: 工具名稱
            error_message: 錯誤信息
            arguments: 工具參數
            
        Returns:
            錯誤處理結果
        """
        try:
            # 分析錯誤
            error_analysis = self._analyze_error(error_message)
            
            # 記錄錯誤
            error_record = self._record_error(tool_name, error_message, error_analysis, arguments)
            
            # 生成恢復建議
            recovery_suggestions = self._generate_recovery_suggestions(error_analysis, tool_name)
            
            # 構建錯誤回應
            error_response = {
                "success": False,
                "error": error_message,
                "tool_name": tool_name,
                "error_analysis": error_analysis,
                "recovery_suggestions": recovery_suggestions,
                "error_id": error_record["error_id"],
                "timestamp": error_record["timestamp"],
                "can_retry": error_analysis["category"] in [
                    ErrorCategory.NETWORK, ErrorCategory.TIMEOUT, ErrorCategory.EXECUTION
                ]
            }
            
            self.logger.error(f"❌ 工具錯誤處理: {tool_name} - {error_analysis['category'].value}")
            
            return error_response
            
        except Exception as e:
            # 錯誤處理器本身出錯
            self.logger.critical(f"💥 錯誤處理器失敗: {str(e)}")
            return {
                "success": False,
                "error": error_message,
                "tool_name": tool_name,
                "handler_error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_error(self, error_message: str) -> Dict[str, Any]:
        """分析錯誤信息"""
        error_message_lower = error_message.lower()
        
        # 確定錯誤類別
        category = ErrorCategory.UNKNOWN
        for cat_name, keywords in self.error_patterns.items():
            if any(keyword in error_message_lower for keyword in keywords):
                category = ErrorCategory(cat_name)
                break
        
        # 確定嚴重程度
        severity = self._determine_severity(error_message_lower, category)
        
        # 提取關鍵信息
        key_info = self._extract_key_info(error_message)
        
        return {
            "category": category,
            "severity": severity,
            "key_info": key_info,
            "is_recoverable": category in [
                ErrorCategory.NETWORK, ErrorCategory.TIMEOUT, 
                ErrorCategory.EXECUTION, ErrorCategory.RESOURCE
            ]
        }
    
    def _determine_severity(self, error_message: str, category: ErrorCategory) -> ErrorSeverity:
        """確定錯誤嚴重程度"""
        # 關鍵詞嚴重程度映射
        critical_keywords = ["critical", "fatal", "crash", "崩潰", "致命"]
        high_keywords = ["failed", "error", "exception", "失敗", "錯誤", "異常"]
        medium_keywords = ["warning", "invalid", "missing", "警告", "無效", "缺少"]
        
        if any(keyword in error_message for keyword in critical_keywords):
            return ErrorSeverity.CRITICAL
        elif any(keyword in error_message for keyword in high_keywords):
            return ErrorSeverity.HIGH
        elif any(keyword in error_message for keyword in medium_keywords):
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW
    
    def _extract_key_info(self, error_message: str) -> Dict[str, Any]:
        """提取錯誤關鍵信息"""
        key_info = {
            "original_message": error_message,
            "message_length": len(error_message),
            "contains_stack_trace": "traceback" in error_message.lower() or "stack trace" in error_message.lower()
        }
        
        # 提取數字信息（可能是錯誤代碼、行號等）
        import re
        numbers = re.findall(r'\d+', error_message)
        if numbers:
            key_info["numbers"] = numbers
        
        # 提取文件路徑
        file_paths = re.findall(r'[/\\][\w/\\.-]+\.\w+', error_message)
        if file_paths:
            key_info["file_paths"] = file_paths
        
        return key_info
    
    def _record_error(self, tool_name: str, error_message: str, 
                     error_analysis: Dict[str, Any], arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """記錄錯誤到歷史記錄"""
        error_record = {
            "error_id": f"err_{len(self.error_history) + 1}_{int(datetime.now().timestamp())}",
            "tool_name": tool_name,
            "error_message": error_message,
            "error_analysis": error_analysis,
            "arguments": arguments,
            "timestamp": datetime.now().isoformat(),
            "stack_trace": traceback.format_exc() if error_analysis["key_info"]["contains_stack_trace"] else None
        }
        
        self.error_history.append(error_record)
        
        # 限制歷史記錄大小
        if len(self.error_history) > 1000:
            self.error_history = self.error_history[-500:]
        
        return error_record
    
    def _generate_recovery_suggestions(self, error_analysis: Dict[str, Any], tool_name: str) -> List[str]:
        """生成恢復建議"""
        suggestions = []
        category = error_analysis["category"]
        severity = error_analysis["severity"]
        
        # 基於錯誤類別的建議
        if category == ErrorCategory.NETWORK:
            suggestions.extend([
                "檢查網絡連接",
                "重試請求",
                "使用備用服務器",
                "檢查防火牆設置"
            ])
        elif category == ErrorCategory.VALIDATION:
            suggestions.extend([
                "檢查輸入參數格式",
                "驗證必要字段是否完整",
                "使用默認值替代無效參數",
                "參考工具文檔確認參數要求"
            ])
        elif category == ErrorCategory.TIMEOUT:
            suggestions.extend([
                "增加超時時間",
                "減少請求複雜度",
                "分批處理大量數據",
                "檢查服務器負載"
            ])
        elif category == ErrorCategory.RESOURCE:
            suggestions.extend([
                "清理臨時文件",
                "釋放未使用的資源",
                "減少並發請求數量",
                "檢查系統資源使用情況"
            ])
        elif category == ErrorCategory.EXECUTION:
            suggestions.extend([
                "檢查工具實現邏輯",
                "使用替代方法",
                "更新工具依賴",
                "聯繫技術支持"
            ])
        
        # 基於嚴重程度的建議
        if severity == ErrorSeverity.CRITICAL:
            suggestions.insert(0, "立即停止相關操作")
            suggestions.append("聯繫系統管理員")
        elif severity == ErrorSeverity.HIGH:
            suggestions.insert(0, "謹慎重試操作")
        
        # 工具特定建議
        tool_specific_suggestions = self._get_tool_specific_suggestions(tool_name, error_analysis)
        suggestions.extend(tool_specific_suggestions)
        
        return suggestions
    
    def _get_tool_specific_suggestions(self, tool_name: str, error_analysis: Dict[str, Any]) -> List[str]:
        """獲取工具特定的恢復建議"""
        suggestions = []
        
        if tool_name == "ziwei_scraper":
            suggestions.extend([
                "檢查出生資料格式是否正確",
                "確認網站是否可訪問",
                "嘗試使用不同的時辰格式"
            ])
        elif tool_name == "rag_knowledge":
            suggestions.extend([
                "檢查查詢字符串是否有效",
                "確認知識庫是否已初始化",
                "嘗試使用更簡單的查詢"
            ])
        elif tool_name == "format_output":
            suggestions.extend([
                "檢查輸入內容格式",
                "嘗試使用不同的輸出格式",
                "確認內容長度是否合理"
            ])
        elif tool_name == "data_validator":
            suggestions.extend([
                "檢查數據結構是否正確",
                "確認驗證規則是否合理",
                "嘗試使用寬鬆驗證模式"
            ])
        
        return suggestions
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """獲取錯誤統計信息"""
        if not self.error_history:
            return {"total_errors": 0}
        
        # 統計錯誤類別
        category_counts = {}
        severity_counts = {}
        tool_counts = {}
        
        for error in self.error_history:
            category = error["error_analysis"]["category"].value
            severity = error["error_analysis"]["severity"].value
            tool_name = error["tool_name"]
            
            category_counts[category] = category_counts.get(category, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "category_distribution": category_counts,
            "severity_distribution": severity_counts,
            "tool_distribution": tool_counts,
            "most_common_category": max(category_counts, key=category_counts.get) if category_counts else None,
            "most_problematic_tool": max(tool_counts, key=tool_counts.get) if tool_counts else None,
            "recent_errors": self.error_history[-5:] if len(self.error_history) >= 5 else self.error_history
        }
    
    def clear_error_history(self):
        """清空錯誤歷史記錄"""
        self.error_history.clear()
        self.logger.info("✅ 錯誤歷史記錄已清空")
    
    def export_error_report(self) -> str:
        """導出錯誤報告"""
        statistics = self.get_error_statistics()
        
        report = f"""
# MCP 錯誤報告

## 統計摘要
- 總錯誤數: {statistics['total_errors']}
- 最常見錯誤類別: {statistics.get('most_common_category', 'N/A')}
- 最有問題的工具: {statistics.get('most_problematic_tool', 'N/A')}

## 錯誤類別分布
{self._format_distribution(statistics.get('category_distribution', {}))}

## 嚴重程度分布
{self._format_distribution(statistics.get('severity_distribution', {}))}

## 工具錯誤分布
{self._format_distribution(statistics.get('tool_distribution', {}))}

## 最近錯誤
{self._format_recent_errors(statistics.get('recent_errors', []))}

報告生成時間: {datetime.now().isoformat()}
        """
        
        return report.strip()
    
    def _format_distribution(self, distribution: Dict[str, int]) -> str:
        """格式化分布統計"""
        if not distribution:
            return "無數據"
        
        lines = []
        for key, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {key}: {count}")
        
        return "\n".join(lines)
    
    def _format_recent_errors(self, recent_errors: List[Dict[str, Any]]) -> str:
        """格式化最近錯誤"""
        if not recent_errors:
            return "無最近錯誤"
        
        lines = []
        for error in recent_errors:
            lines.append(f"- {error['timestamp']}: {error['tool_name']} - {error['error_message'][:100]}...")
        
        return "\n".join(lines)
