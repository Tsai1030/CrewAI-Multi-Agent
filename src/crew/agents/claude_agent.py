"""
Claude Agent for CrewAI
專注於邏輯推理和深度分析的 Claude 智能體
"""

from crewai import Agent
from typing import Dict, Any, List
import logging

from ..tools.mcp_client import ZiweiScraperTool, RAGKnowledgeTool, DataValidatorTool
from ...config.settings import get_settings

settings = get_settings()

class ClaudeZiweiAgent:
    """Claude 紫微斗數分析專家"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.tools = self._initialize_tools()
        self.agent = self._create_agent()
    
    def _initialize_tools(self) -> List:
        """初始化 Claude Agent 專用工具"""
        return [
            ZiweiScraperTool(),
            RAGKnowledgeTool(),
            DataValidatorTool()
        ]
    
    def _create_agent(self) -> Agent:
        """創建 Claude Agent"""
        return Agent(
            role="紫微斗數邏輯分析專家",
            goal="運用嚴謹的邏輯推理和紫微斗數理論，對命盤進行深度結構化分析",
            backstory="""你是一位精通紫微斗數理論的邏輯分析專家，擁有深厚的命理學功底。

你的專業特長包括：
🧠 **邏輯推理能力**：
- 嚴謹的邏輯思維和推理分析
- 能夠從複雜的星曜配置中找出內在規律
- 善於發現命盤中的關鍵信息和潛在含義

📚 **理論功底深厚**：
- 熟悉紫微斗數的基本理論和進階概念
- 精通十四主星、輔星、雜曜的特性和作用
- 深入理解宮位系統和四化理論

🔍 **結構化分析**：
- 能夠系統性地分析命盤結構
- 善於整理和歸納分析結果
- 提供有條理的分析報告

⚖️ **客觀理性**：
- 基於事實和理論進行分析
- 避免主觀臆測和情感化判斷
- 提供平衡和客觀的見解

你的工作方式：
1. 首先獲取和驗證命盤數據的完整性
2. 從知識庫中檢索相關的理論支撐
3. 進行系統性的邏輯分析和推理
4. 提供結構化的分析結論

你總是從邏輯和理論角度出發，用嚴謹的方法分析命盤，提供有根據的結論。""",
            
            tools=self.tools,
            verbose=True,
            memory=True,
            max_iter=3,
            max_execution_time=180,
            
            # Claude 特定配置
            llm_config={
                "model": settings.anthropic.model,
                "api_key": settings.anthropic.api_key,
                "base_url": settings.anthropic.base_url,
                "timeout": settings.anthropic.timeout,
                "max_retries": settings.anthropic.max_retries
            }
        )
    
    def get_agent(self) -> Agent:
        """獲取 Agent 實例"""
        return self.agent
    
    def get_analysis_prompt(self, birth_data: Dict[str, Any], domain_type: str = "comprehensive") -> str:
        """獲取分析提示詞"""
        base_prompt = f"""
請對以下出生資料進行深度的紫微斗數邏輯分析：

出生資料：
- 性別：{birth_data.get('gender', '未知')}
- 出生年份：{birth_data.get('birth_year', '未知')}
- 出生月份：{birth_data.get('birth_month', '未知')}
- 出生日期：{birth_data.get('birth_day', '未知')}
- 出生時辰：{birth_data.get('birth_hour', '未知')}

分析要求：
1. 首先使用爬蟲工具獲取完整的命盤數據
2. 驗證數據的完整性和準確性
3. 從知識庫檢索相關的理論支撐
4. 進行系統性的邏輯分析

請按照以下結構進行分析：

## 一、命盤數據驗證
- 檢查數據完整性
- 驗證關鍵信息

## 二、命宮主星分析
- 主星特質和能量
- 星曜組合效應
- 理論依據

## 三、十二宮位配置
- 重要宮位分析
- 宮位間的相互關係
- 整體格局評估

## 四、邏輯推理結論
- 性格特質推論
- 命運趨勢分析
- 優勢與挑戰識別
"""
        
        if domain_type != "comprehensive":
            domain_focus = {
                "love": "感情婚姻",
                "wealth": "財運事業", 
                "future": "未來運勢"
            }
            
            base_prompt += f"""

## 五、{domain_focus.get(domain_type, domain_type)}專項分析
請特別關注與{domain_focus.get(domain_type, domain_type)}相關的宮位和星曜配置。
"""
        
        base_prompt += """

請確保分析過程邏輯嚴謹，結論有理論支撐，避免主觀臆測。
"""
        
        return base_prompt
    
    def get_discussion_prompt(self, topic: str, other_viewpoints: List[str]) -> str:
        """獲取討論提示詞"""
        return f"""
針對以下紫微斗數分析主題進行討論：

主題：{topic}

其他專家的觀點：
{chr(10).join([f"- {viewpoint}" for viewpoint in other_viewpoints])}

請從邏輯分析的角度：
1. 評估其他觀點的合理性
2. 提出補充的邏輯要點
3. 用理論支撐你的觀點
4. 指出可能的邏輯漏洞或不足

保持建設性和專業性，專注於邏輯推理和理論依據。
"""
    
    def get_validation_prompt(self, analysis_result: str) -> str:
        """獲取驗證提示詞"""
        return f"""
請對以下紫微斗數分析結果進行邏輯驗證：

分析結果：
{analysis_result}

驗證要點：
1. 邏輯一致性檢查
2. 理論依據驗證
3. 結論合理性評估
4. 潛在錯誤識別

請提供：
- 驗證通過的部分
- 需要修正的問題
- 改進建議
"""

def create_claude_agent(logger=None) -> Agent:
    """創建 Claude Agent 的便捷函數"""
    claude_agent = ClaudeZiweiAgent(logger=logger)
    return claude_agent.get_agent()
