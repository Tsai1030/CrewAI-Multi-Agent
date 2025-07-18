"""
GPT Agent for CrewAI
專注於創意表達和人性化解釋的 GPT 智能體
"""

from crewai import Agent
from typing import Dict, Any, List
import logging

from ..tools.mcp_client import RAGKnowledgeTool, FormatOutputTool
from ...config.settings import get_settings

settings = get_settings()

class GPTZiweiAgent:
    """GPT 紫微斗數創意表達專家"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.tools = self._initialize_tools()
        self.agent = self._create_agent()
    
    def _initialize_tools(self) -> List:
        """初始化 GPT Agent 專用工具"""
        return [
            RAGKnowledgeTool(),
            FormatOutputTool()
        ]
    
    def _create_agent(self) -> Agent:
        """創建 GPT Agent"""
        return Agent(
            role="紫微斗數創意表達專家",
            goal="將命理分析轉化為生動、易懂、富有洞察力的人性化表達",
            backstory="""你是一位擅長創意表達的命理解讀專家，能夠將深奧的紫微斗數理論
轉化為生動有趣的人生指導。

你的專業特長包括：
🎨 **創意表達能力**：
- 富有想像力的表達方式
- 能夠用生動的語言描述抽象概念
- 善於運用比喻、故事和案例
- 讓複雜的理論變得親切易懂

💝 **人性化溝通**：
- 溫暖親切的語言風格
- 能夠感同身受地理解他人
- 善於從人性角度解讀命理
- 提供有溫度的人生建議

🌟 **洞察力深刻**：
- 能夠發現命盤中的獨特亮點
- 善於挖掘潛在的可能性
- 提供啟發性的人生視角
- 幫助人們看到希望和機會

📝 **多樣化表達**：
- 能夠適應不同的表達風格
- 支援多種輸出格式
- 根據受眾調整語言深度
- 創造引人入勝的內容

你的工作方式：
1. 深入理解邏輯分析的結果
2. 從知識庫中尋找相關的解釋和案例
3. 用創意和人性化的方式重新表達
4. 提供實用的人生建議和指導
5. 根據需求格式化最終輸出

你總是能讓複雜的命理分析變得親切易懂，給人啟發和希望。你相信每個人都有獨特的價值和潛力，
命理分析的目的是幫助人們更好地認識自己，發揮優勢，面對挑戰。""",
            
            tools=self.tools,
            verbose=True,
            memory=True,
            max_iter=3,
            max_execution_time=180,
            
            # GPT 特定配置
            llm_config={
                "model": settings.openai.model_gpt4o,
                "api_key": settings.openai.api_key,
                "base_url": settings.openai.base_url,
                "timeout": settings.openai.timeout,
                "max_retries": settings.openai.max_retries
            }
        )
    
    def get_agent(self) -> Agent:
        """獲取 Agent 實例"""
        return self.agent
    
    def get_interpretation_prompt(self, analysis_result: str, domain_type: str = "comprehensive") -> str:
        """獲取創意解釋提示詞"""
        base_prompt = f"""
請將以下邏輯嚴謹的紫微斗數分析結果，轉化為生動、易懂、富有洞察力的人性化表達：

原始分析結果：
{analysis_result}

創意表達要求：
1. 使用溫暖親切的語言風格
2. 運用生動的比喻和故事
3. 提供實用的人生建議
4. 突出個人的獨特價值和潛力
5. 給予正面的鼓勵和指導

請按照以下結構進行創意表達：

## 🌟 你的命運密碼
用生動的語言描述命盤的整體特質，就像在講述一個獨特的人生故事。

## 💎 你的天賦寶藏
- 發掘和讚美個人的優勢特質
- 用比喻的方式描述天賦能力
- 提供發揮優勢的具體建議

## 🌈 人生的色彩
- 描述性格的多面性和豐富性
- 用色彩、音樂或自然現象作比喻
- 幫助理解自己的複雜性

## 🚀 成長的方向
- 指出發展的機會和可能性
- 提供實用的成長建議
- 鼓勵積極面對挑戰
"""
        
        if domain_type != "comprehensive":
            domain_focus = {
                "love": "💕 愛情的花園",
                "wealth": "💰 財富的密碼",
                "future": "🔮 未來的藍圖"
            }
            
            domain_content = {
                "love": "在感情的世界裡，你就像...",
                "wealth": "在財富的道路上，你擁有...",
                "future": "展望未來，你的人生將..."
            }
            
            base_prompt += f"""

## {domain_focus.get(domain_type, domain_type)}
{domain_content.get(domain_type, "專注於這個領域的特殊洞察...")}
"""
        
        base_prompt += """

## ✨ 給你的話
用溫暖鼓勵的話語作為結尾，讓人感到被理解和支持。

創意表達風格：
- 語言要溫暖、正面、有希望
- 多用比喻、故事和具體例子
- 避免過於技術性的術語
- 讓每個人都能感受到自己的獨特價值
- 提供可行的人生建議

請讓這份分析成為一份充滿溫度和智慧的人生指南。
"""
        
        return base_prompt
    
    def get_creative_discussion_prompt(self, topic: str, other_viewpoints: List[str]) -> str:
        """獲取創意討論提示詞"""
        return f"""
針對以下紫微斗數分析主題，請提供創意和人性化的觀點：

主題：{topic}

其他專家的觀點：
{chr(10).join([f"- {viewpoint}" for viewpoint in other_viewpoints])}

請從創意表達的角度：
1. 用生動的比喻重新詮釋主題
2. 提供不同的人性化視角
3. 分享啟發性的故事或案例
4. 補充溫暖和正面的見解
5. 提供實用的人生建議

保持溫暖、正面、富有創意的表達風格。
"""
    
    def get_formatting_prompt(self, content: str, output_format: str, style: str = "professional") -> str:
        """獲取格式化提示詞"""
        return f"""
請將以下內容格式化為 {output_format} 格式，風格為 {style}：

原始內容：
{content}

格式化要求：
1. 保持內容的核心信息和洞察
2. 根據格式要求調整結構和表達
3. 確保可讀性和美觀性
4. 添加適當的標記和分段
5. 保持溫暖和正面的語調

請使用格式化工具完成這個任務。
"""

def create_gpt_agent(logger=None) -> Agent:
    """創建 GPT Agent 的便捷函數"""
    gpt_agent = GPTZiweiAgent(logger=logger)
    return gpt_agent.get_agent()
