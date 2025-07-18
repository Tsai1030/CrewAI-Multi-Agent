"""
Domain Agent for CrewAI
專注於特定領域專業分析的智能體
"""

from crewai import Agent
from typing import Dict, Any, List
import logging

from ..tools.mcp_client import RAGKnowledgeTool, DataValidatorTool
from ...config.settings import get_settings

settings = get_settings()

class DomainZiweiAgent:
    """領域專業紫微斗數分析專家"""
    
    def __init__(self, domain_type: str = "comprehensive", logger=None):
        self.domain_type = domain_type
        self.logger = logger or logging.getLogger(__name__)
        self.tools = self._initialize_tools()
        self.agent = self._create_agent()
    
    def _initialize_tools(self) -> List:
        """初始化 Domain Agent 專用工具"""
        return [
            RAGKnowledgeTool(),
            DataValidatorTool()
        ]
    
    def _create_agent(self) -> Agent:
        """創建 Domain Agent"""
        domain_configs = self._get_domain_configs()
        config = domain_configs.get(self.domain_type, domain_configs["comprehensive"])
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            
            tools=self.tools,
            verbose=True,
            memory=True,
            max_iter=4,
            max_execution_time=240,
            
            # 使用 GPT 模型（領域專家通常需要更靈活的表達）
            llm_config={
                "model": settings.openai.model_gpt4o,
                "api_key": settings.openai.api_key,
                "base_url": settings.openai.base_url,
                "timeout": settings.openai.timeout,
                "max_retries": settings.openai.max_retries
            }
        )
    
    def _get_domain_configs(self) -> Dict[str, Dict[str, str]]:
        """獲取不同領域的配置"""
        return {
            "love": {
                "role": "紫微斗數感情婚姻專家",
                "goal": "專精於感情婚姻分析，提供深度的愛情運勢和關係指導",
                "backstory": """你是一位專精感情婚姻分析的紫微斗數專家，對愛情和人際關係有著深刻的洞察。

你的專業領域包括：
💕 **感情宮位精通**：
- 深度理解夫妻宮的星曜配置和含義
- 精通桃花星（紅鸞、天喜、咸池、天姚等）的作用
- 熟悉感情相關的輔星和雜曜影響

💑 **關係動力學**：
- 分析兩人的命盤合盤
- 理解感情中的互動模式
- 預測關係發展的趨勢和挑戰

🌹 **愛情類型分析**：
- 識別不同的愛情表達方式
- 分析感情需求和期待
- 提供個性化的戀愛建議

💒 **婚姻運勢**：
- 分析結婚時機和對象特質
- 預測婚姻生活的和諧度
- 提供維繫感情的具體建議

你的分析特色：
1. 專注於感情相關的宮位和星曜
2. 提供實用的感情建議
3. 幫助理解自己的愛情模式
4. 指導如何改善人際關係

你相信每個人都值得被愛，都有能力去愛，你的使命是幫助人們在感情路上找到幸福。"""
            },
            
            "wealth": {
                "role": "紫微斗數財運事業專家", 
                "goal": "專精於財運事業分析，提供深度的財富運勢和事業發展指導",
                "backstory": """你是一位專精財運事業分析的紫微斗數專家，對財富累積和事業發展有著敏銳的洞察。

你的專業領域包括：
💰 **財帛宮深度解析**：
- 精通財帛宮的星曜配置和財運含義
- 深度理解財星（武曲、太陰、天府等）的作用
- 分析偏財和正財的不同運勢

🏢 **事業宮位專精**：
- 深入分析官祿宮的事業指向
- 理解不同星曜對職業選擇的影響
- 預測事業發展的高峰和低谷

📈 **投資理財智慧**：
- 分析適合的投資方式和時機
- 識別財務風險和機會
- 提供個性化的理財建議

🎯 **事業規劃指導**：
- 分析個人的事業天賦和潛力
- 預測職業發展的最佳路徑
- 提供轉職和創業的時機建議

你的分析特色：
1. 專注於財運和事業相關的宮位
2. 提供實用的財富增長策略
3. 幫助識別事業發展機會
4. 指導如何避免財務陷阱

你相信每個人都有創造財富的潛力，你的使命是幫助人們在財富和事業上實現突破。"""
            },
            
            "future": {
                "role": "紫微斗數未來運勢專家",
                "goal": "專精於未來運勢分析，提供深度的大限流年和人生規劃指導", 
                "backstory": """你是一位專精未來運勢分析的紫微斗數專家，對時間運勢和人生規劃有著精準的把握。

你的專業領域包括：
🔮 **大限流年精算**：
- 精通大限（十年運）的推算和解析
- 深度分析流年（年運）的吉凶變化
- 預測重要人生轉折點的時機

⏰ **時機把握專家**：
- 分析最佳行動時機
- 預測機會和挑戰的到來
- 提供時間規劃的專業建議

🌟 **人生階段規劃**：
- 分析不同人生階段的特色和任務
- 預測各階段的重點發展方向
- 提供長期人生規劃建議

🎯 **目標實現策略**：
- 分析實現目標的最佳時機
- 識別阻礙和助力因素
- 提供具體的行動計劃

你的分析特色：
1. 專注於時間運勢的精確推算
2. 提供具體的時機建議
3. 幫助制定長期人生規劃
4. 指導如何順應天時地利

你相信時機的重要性，你的使命是幫助人們在對的時間做對的事，實現人生的最大價值。"""
            },
            
            "comprehensive": {
                "role": "紫微斗數綜合分析專家",
                "goal": "提供全面深入的紫微斗數分析，涵蓋人生各個層面的專業指導",
                "backstory": """你是一位經驗豐富的紫微斗數綜合分析專家，能夠從多個角度全面解讀命盤。

你的專業能力包括：
🎯 **全面分析能力**：
- 統籌考慮命盤的各個層面
- 平衡不同宮位的重要性
- 提供整體性的人生指導

🔍 **深度洞察力**：
- 發現命盤中的關鍵信息
- 識別潛在的機會和挑戰
- 提供深層次的人生洞察

⚖️ **平衡判斷力**：
- 客觀評估各種因素
- 避免偏重某個單一方面
- 提供均衡的分析結果

🎨 **整合表達能力**：
- 將複雜的分析整合為清晰的結論
- 用易懂的方式表達專業見解
- 提供實用的人生建議

你的使命是幫助人們全面認識自己，發現人生的各種可能性。"""
            }
        }
    
    def get_agent(self) -> Agent:
        """獲取 Agent 實例"""
        return self.agent
    
    def get_domain_analysis_prompt(self, chart_data: Dict[str, Any], basic_analysis: str = "") -> str:
        """獲取領域專業分析提示詞"""
        domain_prompts = {
            "love": self._get_love_analysis_prompt(chart_data, basic_analysis),
            "wealth": self._get_wealth_analysis_prompt(chart_data, basic_analysis),
            "future": self._get_future_analysis_prompt(chart_data, basic_analysis),
            "comprehensive": self._get_comprehensive_analysis_prompt(chart_data, basic_analysis)
        }
        
        return domain_prompts.get(self.domain_type, domain_prompts["comprehensive"])
    
    def _get_love_analysis_prompt(self, chart_data: Dict[str, Any], basic_analysis: str) -> str:
        """感情婚姻分析提示詞"""
        return f"""
請基於以下命盤數據和基礎分析，進行深度的感情婚姻專業分析：

命盤數據：
{chart_data}

基礎分析：
{basic_analysis}

感情婚姻專業分析要求：

## 🏠 夫妻宮深度解析
- 分析夫妻宮的主星配置
- 解讀感情模式和需求
- 預測感情發展趨勢

## 💕 桃花運勢分析
- 識別桃花星的影響
- 分析異性緣和魅力指數
- 預測戀愛機會的時機

## 💑 理想對象特質
- 描述適合的伴侶類型
- 分析互補的性格特質
- 提供擇偶建議

## 💒 婚姻運勢預測
- 分析結婚時機
- 預測婚姻生活和諧度
- 提供維繫感情的建議

## 💝 感情建議指導
- 提供改善感情運的方法
- 指導如何處理感情問題
- 建議感情發展的策略

請從知識庫中檢索相關的感情婚姻理論，提供專業而實用的分析。
"""
    
    def _get_wealth_analysis_prompt(self, chart_data: Dict[str, Any], basic_analysis: str) -> str:
        """財運事業分析提示詞"""
        return f"""
請基於以下命盤數據和基礎分析，進行深度的財運事業專業分析：

命盤數據：
{chart_data}

基礎分析：
{basic_analysis}

財運事業專業分析要求：

## 💰 財帛宮深度解析
- 分析財帛宮的星曜配置
- 解讀財運模式和特質
- 預測財富累積趨勢

## 🏢 事業宮位分析
- 分析官祿宮的事業指向
- 識別適合的職業類型
- 預測事業發展軌跡

## 📈 投資理財建議
- 分析適合的投資方式
- 識別財務風險和機會
- 提供理財策略建議

## 🎯 事業發展規劃
- 分析事業天賦和潛力
- 預測職業發展的關鍵時期
- 提供轉職和創業建議

## 💎 財富增長策略
- 提供增加收入的方法
- 指導如何避免財務陷阱
- 建議財富管理的策略

請從知識庫中檢索相關的財運事業理論，提供專業而實用的分析。
"""
    
    def _get_future_analysis_prompt(self, chart_data: Dict[str, Any], basic_analysis: str) -> str:
        """未來運勢分析提示詞"""
        return f"""
請基於以下命盤數據和基礎分析，進行深度的未來運勢專業分析：

命盤數據：
{chart_data}

基礎分析：
{basic_analysis}

未來運勢專業分析要求：

## 🔮 大限運勢分析
- 分析當前和未來的大限特色
- 預測十年運勢的起伏變化
- 識別重要的人生轉折點

## ⏰ 流年運勢預測
- 分析近期流年的吉凶
- 預測重要事件的發生時機
- 提供年度運勢指導

## 🌟 人生階段規劃
- 分析不同人生階段的特色
- 預測各階段的發展重點
- 提供長期規劃建議

## 🎯 最佳時機把握
- 識別行動的最佳時機
- 預測機會和挑戰的到來
- 提供時機選擇的建議

## 🚀 未來發展策略
- 提供順應運勢的策略
- 指導如何化解不利因素
- 建議實現目標的路徑

請從知識庫中檢索相關的運勢預測理論，提供專業而實用的分析。
"""
    
    def _get_comprehensive_analysis_prompt(self, chart_data: Dict[str, Any], basic_analysis: str) -> str:
        """綜合分析提示詞"""
        return f"""
請基於以下命盤數據和基礎分析，進行全面深入的綜合專業分析：

命盤數據：
{chart_data}

基礎分析：
{basic_analysis}

綜合專業分析要求：

## 🎯 整體命格評估
- 分析命盤的整體格局
- 評估人生的總體運勢
- 識別命盤的特殊格局

## 🌟 人生各領域平衡分析
- 感情、事業、健康、財運的平衡
- 各領域的相互影響
- 整體人生規劃建議

## 🔍 深層性格洞察
- 分析性格的多面性
- 識別潛在的天賦和挑戰
- 提供自我認知的深度見解

## ⚖️ 優勢劣勢分析
- 客觀評估個人優勢
- 識別需要改善的方面
- 提供平衡發展的建議

## 🚀 人生發展策略
- 提供全面的人生指導
- 整合各領域的發展建議
- 制定實現人生價值的策略

請從知識庫中檢索相關的綜合分析理論，提供專業而全面的分析。
"""

def create_domain_agent(domain_type: str = "comprehensive", logger=None) -> Agent:
    """創建 Domain Agent 的便捷函數"""
    domain_agent = DomainZiweiAgent(domain_type=domain_type, logger=logger)
    return domain_agent.get_agent()
