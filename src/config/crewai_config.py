"""
CrewAI 框架配置
定義 Agent 角色、任務和工具配置
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class AgentRole(Enum):
    """Agent 角色定義"""
    CLAUDE_ANALYST = "claude_analyst"      # Claude 邏輯分析專家
    GPT_CREATIVE = "gpt_creative"          # GPT 創意表達專家
    DOMAIN_EXPERT = "domain_expert"        # 領域專業專家

class TaskType(Enum):
    """任務類型定義"""
    DATA_EXTRACTION = "data_extraction"    # 數據提取
    ANALYSIS = "analysis"                  # 分析推理
    KNOWLEDGE_RESEARCH = "knowledge_research"  # 知識檢索
    CREATIVE_INTERPRETATION = "creative_interpretation"  # 創意解釋
    DOMAIN_ANALYSIS = "domain_analysis"    # 領域專業分析
    RESULT_INTEGRATION = "result_integration"  # 結果整合
    FORMAT_OUTPUT = "format_output"        # 格式化輸出

@dataclass
class AgentConfig:
    """Agent 配置"""
    role: str
    goal: str
    backstory: str
    tools: List[str]
    verbose: bool = True
    memory: bool = True
    max_iter: int = 5
    max_execution_time: int = 300  # 5分鐘

@dataclass
class TaskConfig:
    """任務配置"""
    description: str
    expected_output: str
    agent_role: AgentRole
    tools: List[str]
    context: List[str] = None
    output_file: str = None

class CrewAIConfig:
    """CrewAI 主配置類"""
    
    def __init__(self):
        self.agents = self._define_agents()
        self.tasks = self._define_tasks()
        self.tools = self._define_tools()
    
    def _define_agents(self) -> Dict[AgentRole, AgentConfig]:
        """定義所有 Agent 配置"""
        return {
            AgentRole.CLAUDE_ANALYST: AgentConfig(
                role="紫微斗數邏輯分析專家",
                goal="運用嚴謹的邏輯推理和紫微斗數理論，對命盤進行深度結構化分析",
                backstory="""你是一位精通紫微斗數理論的邏輯分析專家，擁有深厚的命理學功底。
                你的特長是：
                1. 邏輯嚴謹的推理分析
                2. 深入的理論支撐和引證
                3. 結構化的命盤解讀
                4. 客觀理性的判斷
                
                你總是從邏輯和理論角度出發，提供有根據的分析結論。""",
                tools=["mcp_ziwei_scraper", "mcp_rag_knowledge", "mcp_data_validator"],
                max_iter=3,
                max_execution_time=180
            ),
            
            AgentRole.GPT_CREATIVE: AgentConfig(
                role="紫微斗數創意表達專家", 
                goal="將命理分析轉化為生動、易懂、富有洞察力的人性化表達",
                backstory="""你是一位擅長創意表達的命理解讀專家，能夠將深奧的紫微斗數理論
                轉化為生動有趣的人生指導。
                你的特長是：
                1. 富有創意的表達方式
                2. 人性化的語言風格
                3. 生動的比喻和故事
                4. 實用的人生建議
                
                你總是能讓複雜的命理分析變得親切易懂，給人啟發。""",
                tools=["mcp_rag_knowledge", "mcp_format_output"],
                max_iter=3,
                max_execution_time=180
            ),
            
            AgentRole.DOMAIN_EXPERT: AgentConfig(
                role="紫微斗數領域專業專家",
                goal="針對特定領域（感情、財運、事業）提供專業深度的命理分析",
                backstory="""你是一位在特定領域有深度專業知識的紫微斗數專家。
                根據分析需求，你可以專精於：
                1. 感情婚姻分析 - 深諳感情宮位和桃花星曜
                2. 財運事業分析 - 精通財帛宮和官祿宮解讀  
                3. 未來運勢分析 - 擅長大限流年推算
                
                你總是能在專業領域提供最深入和準確的見解。""",
                tools=["mcp_rag_knowledge", "mcp_data_validator"],
                max_iter=4,
                max_execution_time=240
            )
        }
    
    def _define_tasks(self) -> Dict[TaskType, TaskConfig]:
        """定義所有任務配置"""
        return {
            TaskType.DATA_EXTRACTION: TaskConfig(
                description="""從紫微斗數網站提取用戶的完整命盤數據。
                需要：
                1. 驗證輸入的出生資料
                2. 調用網站API獲取命盤
                3. 解析並結構化命盤數據
                4. 驗證數據完整性""",
                expected_output="結構化的紫微斗數命盤數據，包含十二宮位、主星配置、四化等完整信息",
                agent_role=AgentRole.CLAUDE_ANALYST,
                tools=["mcp_ziwei_scraper", "mcp_data_validator"]
            ),
            
            TaskType.KNOWLEDGE_RESEARCH: TaskConfig(
                description="""基於命盤數據，從知識庫中檢索相關的紫微斗數理論和解釋。
                需要：
                1. 分析命盤中的關鍵星曜組合
                2. 檢索相關的理論知識
                3. 整理相關的解釋資料
                4. 提供理論支撐""",
                expected_output="與命盤相關的紫微斗數理論知識和解釋資料",
                agent_role=AgentRole.CLAUDE_ANALYST,
                tools=["mcp_rag_knowledge"]
            ),
            
            TaskType.ANALYSIS: TaskConfig(
                description="""對命盤進行深度邏輯分析和推理。
                需要：
                1. 分析命宮主星特質
                2. 解讀十二宮位配置
                3. 分析星曜組合效應
                4. 推理性格特徵和命運趨勢""",
                expected_output="邏輯嚴謹的命盤分析報告，包含性格特質、優勢劣勢、人生趨勢等",
                agent_role=AgentRole.CLAUDE_ANALYST,
                tools=["mcp_rag_knowledge", "mcp_data_validator"]
            ),
            
            TaskType.CREATIVE_INTERPRETATION: TaskConfig(
                description="""將分析結果轉化為生動易懂的創意表達。
                需要：
                1. 將理論分析人性化表達
                2. 使用生動的比喻和故事
                3. 提供實用的人生建議
                4. 創造富有洞察力的解讀""",
                expected_output="生動有趣、易於理解的命理解讀，包含人生指導和建議",
                agent_role=AgentRole.GPT_CREATIVE,
                tools=["mcp_format_output"]
            ),
            
            TaskType.DOMAIN_ANALYSIS: TaskConfig(
                description="""針對特定領域進行專業深度分析。
                需要：
                1. 專注於特定領域宮位
                2. 深入分析相關星曜
                3. 提供專業見解
                4. 給出具體建議""",
                expected_output="特定領域的專業分析報告和建議",
                agent_role=AgentRole.DOMAIN_EXPERT,
                tools=["mcp_rag_knowledge", "mcp_data_validator"]
            ),
            
            TaskType.RESULT_INTEGRATION: TaskConfig(
                description="""整合所有Agent的分析結果，形成統一的最終報告。
                需要：
                1. 整合各Agent的分析結果
                2. 消除矛盾和重複
                3. 形成一致的結論
                4. 確保邏輯連貫性""",
                expected_output="整合後的完整分析報告",
                agent_role=AgentRole.CLAUDE_ANALYST,
                tools=["mcp_data_validator"]
            ),
            
            TaskType.FORMAT_OUTPUT: TaskConfig(
                description="""將最終結果格式化為用戶要求的輸出格式。
                需要：
                1. 根據用戶需求選擇格式
                2. 美化排版和結構
                3. 添加適當的標記和分段
                4. 確保可讀性""",
                expected_output="格式化的最終分析報告",
                agent_role=AgentRole.GPT_CREATIVE,
                tools=["mcp_format_output"]
            )
        }
    
    def _define_tools(self) -> Dict[str, Dict[str, Any]]:
        """定義所有工具配置"""
        return {
            "mcp_ziwei_scraper": {
                "name": "紫微斗數數據爬取工具",
                "description": "從紫微斗數網站獲取命盤數據",
                "mcp_tool": "ziwei_scraper"
            },
            "mcp_rag_knowledge": {
                "name": "紫微斗數知識檢索工具", 
                "description": "從知識庫檢索相關理論和解釋",
                "mcp_tool": "rag_knowledge"
            },
            "mcp_format_output": {
                "name": "輸出格式化工具",
                "description": "將分析結果格式化為指定格式",
                "mcp_tool": "format_output"
            },
            "mcp_data_validator": {
                "name": "數據驗證工具",
                "description": "驗證數據完整性和準確性",
                "mcp_tool": "data_validator"
            }
        }
    
    def get_agent_config(self, role: AgentRole) -> AgentConfig:
        """獲取指定角色的Agent配置"""
        return self.agents[role]
    
    def get_task_config(self, task_type: TaskType) -> TaskConfig:
        """獲取指定類型的任務配置"""
        return self.tasks[task_type]
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """獲取指定工具的配置"""
        return self.tools.get(tool_name, {})

# 全局配置實例
crewai_config = CrewAIConfig()

def get_crewai_config() -> CrewAIConfig:
    """獲取CrewAI配置實例"""
    return crewai_config
