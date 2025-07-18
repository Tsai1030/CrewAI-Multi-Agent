"""
CrewAI 主管理器
負責創建和管理多智能體團隊，協調任務執行
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

from ..config.crewai_config import (
    CrewAIConfig, AgentRole, TaskType, 
    get_crewai_config
)
from ..config.settings import get_settings
from .tools.simple_mcp_tool import get_all_tools

settings = get_settings()
crewai_config = get_crewai_config()

class ZiweiCrewManager:
    """紫微斗數 CrewAI 管理器"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.config = crewai_config
        self.settings = settings
        
        # 初始化組件
        self.mcp_client = None
        self.agents = {}
        self.tools = {}
        self.crew = None
        
        # 初始化標記
        self._initialized = False
    
    async def initialize(self):
        """初始化 CrewAI 系統"""
        if self._initialized:
            return
            
        try:
            self.logger.info("🚀 初始化 CrewAI 系統...")
            
            # 1. 初始化 MCP 客戶端
            await self._initialize_mcp_client()
            
            # 2. 初始化工具
            await self._initialize_tools()
            
            # 3. 初始化 Agents
            await self._initialize_agents()
            
            self._initialized = True
            self.logger.info("✅ CrewAI 系統初始化完成")
            
        except Exception as e:
            self.logger.error(f"❌ CrewAI 系統初始化失敗: {str(e)}")
            raise
    
    async def _initialize_mcp_client(self):
        """初始化 MCP 客戶端"""
        try:
            # 使用簡化的工具，不需要實際的 MCP 客戶端
            self.mcp_client = None
            self.logger.info("✅ MCP 客戶端初始化完成")
        except Exception as e:
            self.logger.error(f"❌ MCP 客戶端初始化失敗: {str(e)}")
            raise
    
    async def _initialize_tools(self):
        """初始化所有工具"""
        try:
            # 使用簡化的工具
            all_tools = get_all_tools()

            # 根據配置映射工具
            for tool_name, tool_config in self.config.tools.items():
                mcp_tool_name = tool_config["mcp_tool"]
                if mcp_tool_name in all_tools:
                    self.tools[tool_name] = all_tools[mcp_tool_name]
                else:
                    self.logger.warning(f"⚠️ 工具 {mcp_tool_name} 未找到")

            self.logger.info(f"✅ 初始化了 {len(self.tools)} 個工具")
        except Exception as e:
            self.logger.error(f"❌ 工具初始化失敗: {str(e)}")
            raise
    
    async def _initialize_agents(self):
        """初始化所有 Agents"""
        try:
            for role, agent_config in self.config.agents.items():
                # 獲取該 Agent 需要的工具
                agent_tools = []
                for tool_name in agent_config.tools:
                    if tool_name in self.tools:
                        agent_tools.append(self.tools[tool_name])
                
                # 創建 Agent
                agent = Agent(
                    role=agent_config.role,
                    goal=agent_config.goal,
                    backstory=agent_config.backstory,
                    tools=agent_tools,
                    verbose=agent_config.verbose,
                    memory=agent_config.memory,
                    max_iter=agent_config.max_iter,
                    max_execution_time=agent_config.max_execution_time,
                    # 根據角色配置不同的 LLM
                    llm=self._get_llm_for_role(role)
                )
                
                self.agents[role] = agent
            
            self.logger.info(f"✅ 初始化了 {len(self.agents)} 個 Agents")
        except Exception as e:
            self.logger.error(f"❌ Agents 初始化失敗: {str(e)}")
            raise
    
    def _get_llm_for_role(self, role: AgentRole):
        """根據角色獲取對應的 LLM"""
        # 這裡可以根據不同角色配置不同的模型
        # 暫時返回 None，讓 CrewAI 使用默認配置
        return None
    
    async def analyze_ziwei_chart(self, 
                                 birth_data: Dict[str, Any],
                                 domain_type: str = "comprehensive",
                                 output_format: str = "detailed") -> Dict[str, Any]:
        """執行紫微斗數分析"""
        
        if not self._initialized:
            await self.initialize()
        
        start_time = datetime.now()
        
        try:
            self.logger.info(f"🔮 開始 CrewAI 紫微斗數分析: {domain_type}")
            
            # 1. 創建任務序列
            tasks = await self._create_analysis_tasks(birth_data, domain_type, output_format)
            
            # 2. 創建 Crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,  # 使用順序處理
                verbose=True,
                memory=True
            )
            
            # 3. 執行分析
            self.logger.info("🚀 開始執行 CrewAI 任務...")
            result = crew.kickoff()
            
            # 4. 處理結果
            processing_time = (datetime.now() - start_time).total_seconds()

            # 提取 CrewOutput 的文本內容
            if hasattr(result, 'raw'):
                result_text = result.raw
            elif hasattr(result, 'content'):
                result_text = result.content
            elif hasattr(result, 'text'):
                result_text = result.text
            else:
                result_text = str(result)

            self.logger.info(f"✅ CrewAI 分析完成，結果長度: {len(result_text)} 字符")

            return {
                "success": True,
                "result": result_text,
                "metadata": {
                    "processing_time": processing_time,
                    "domain_type": domain_type,
                    "output_format": output_format,
                    "agents_used": list(self.agents.keys()),
                    "tasks_completed": len(tasks),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"❌ CrewAI 分析失敗: {str(e)}")
            
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "processing_time": processing_time,
                    "domain_type": domain_type,
                    "output_format": output_format,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    async def _create_analysis_tasks(self, 
                                   birth_data: Dict[str, Any],
                                   domain_type: str,
                                   output_format: str) -> List[Task]:
        """創建分析任務序列"""
        
        tasks = []
        
        # 1. 數據提取任務
        data_extraction_config = self.config.get_task_config(TaskType.DATA_EXTRACTION)
        data_extraction_task = Task(
            description=f"{data_extraction_config.description}\n\n出生資料: {birth_data}",
            expected_output=data_extraction_config.expected_output,
            agent=self.agents[AgentRole.CLAUDE_ANALYST]
        )
        tasks.append(data_extraction_task)
        
        # 2. 知識檢索任務
        knowledge_research_config = self.config.get_task_config(TaskType.KNOWLEDGE_RESEARCH)
        knowledge_research_task = Task(
            description=knowledge_research_config.description,
            expected_output=knowledge_research_config.expected_output,
            agent=self.agents[AgentRole.CLAUDE_ANALYST],
            context=[data_extraction_task]  # 依賴數據提取任務
        )
        tasks.append(knowledge_research_task)
        
        # 3. 邏輯分析任務
        analysis_config = self.config.get_task_config(TaskType.ANALYSIS)
        analysis_task = Task(
            description=analysis_config.description,
            expected_output=analysis_config.expected_output,
            agent=self.agents[AgentRole.CLAUDE_ANALYST],
            context=[data_extraction_task, knowledge_research_task]
        )
        tasks.append(analysis_task)
        
        # 4. 創意解釋任務
        creative_config = self.config.get_task_config(TaskType.CREATIVE_INTERPRETATION)
        creative_task = Task(
            description=creative_config.description,
            expected_output=creative_config.expected_output,
            agent=self.agents[AgentRole.GPT_CREATIVE],
            context=[analysis_task]
        )
        tasks.append(creative_task)
        
        # 5. 領域專業分析任務（如果需要）
        if domain_type != "comprehensive":
            domain_config = self.config.get_task_config(TaskType.DOMAIN_ANALYSIS)
            domain_task = Task(
                description=f"{domain_config.description}\n\n專注領域: {domain_type}",
                expected_output=f"{domain_type}領域的{domain_config.expected_output}",
                agent=self.agents[AgentRole.DOMAIN_EXPERT],
                context=[data_extraction_task, knowledge_research_task]
            )
            tasks.append(domain_task)
        
        # 6. 格式化輸出任務
        format_config = self.config.get_task_config(TaskType.FORMAT_OUTPUT)
        format_task = Task(
            description=f"{format_config.description}\n\n輸出格式: {output_format}",
            expected_output=f"{output_format}格式的{format_config.expected_output}",
            agent=self.agents[AgentRole.GPT_CREATIVE],
            context=tasks  # 依賴所有前面的任務
        )
        tasks.append(format_task)
        
        return tasks
    
    async def cleanup(self):
        """清理資源"""
        try:
            if self.mcp_client:
                await self.mcp_client.cleanup()
            
            self.agents.clear()
            self.tools.clear()
            self.crew = None
            self._initialized = False
            
            self.logger.info("✅ CrewAI 系統清理完成")
        except Exception as e:
            self.logger.error(f"❌ CrewAI 系統清理失敗: {str(e)}")

# 便捷函數
async def create_ziwei_crew_manager() -> ZiweiCrewManager:
    """創建並初始化紫微斗數 CrewAI 管理器"""
    manager = ZiweiCrewManager()
    await manager.initialize()
    return manager
