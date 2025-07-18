"""
紫微斗數AI系統 - 主程式 (CrewAI + MCP 架構)
整合 CrewAI Multi-Agent + 統一 MCP 服務器 + RAG + GPT-4o 的完整系統
"""

import asyncio
import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# 強制載入環境變數
from dotenv import load_dotenv
load_dotenv(override=True)

# 導入新的 CrewAI 系統組件
from src.crew.crew_manager import ZiweiCrewManager, create_ziwei_crew_manager
from src.config.settings import get_settings
from src.utils.cache_manager import get_cache_manager
from src.utils.error_handler import get_error_guidance
from performance_config import get_config_by_name, apply_config

# 保留舊系統組件作為備用
from src.agents.coordinator import MultiAgentCoordinator, CoordinationStrategy
from src.mcp.tools.ziwei_tool import ZiweiTool
from src.rag.rag_system import ZiweiRAGSystem
from src.output.gpt4o_formatter import GPT4oFormatter

# 載入設定
settings = get_settings()

class ZiweiAISystem:
    """紫微斗數AI系統主類"""

    def __init__(self, logger=None, performance_config='default', use_crewai=True):
        """
        初始化系統

        Args:
            logger: 日誌記錄器
            performance_config: 性能配置 ('default', 'fast', 'balanced', 'quality')
            use_crewai: 是否使用新的 CrewAI 架構 (默認: True)
        """
        self.logger = logger or self._setup_logger()
        self.performance_config = get_config_by_name(performance_config)
        self.use_crewai = use_crewai
        self.logger.info(f"使用性能配置: {performance_config}")

        # 新架構組件 (CrewAI + MCP)
        self.crew_manager = None

        # 舊架構組件 (備用)
        self.coordinator = None
        self.ziwei_tool = None
        self.rag_system = None
        self.formatter = None

        # 共用組件
        self.cache_manager = get_cache_manager()  # 初始化快取管理器

        # 系統狀態
        self.is_initialized = False
        self.initialization_time = None

        architecture = "CrewAI + MCP" if use_crewai else "Legacy Multi-Agent"
        self.logger.info(f"ZiweiAISystem initialized (架構: {architecture})")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌系統"""
        logger = logging.getLogger("ZiweiAI")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # 控制台處理器
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # 文件處理器
            log_file = Path("logs/ziwei_ai.log")
            log_file.parent.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    async def initialize(self):
        """初始化所有系統組件"""
        try:
            start_time = time.time()
            self.logger.info("開始初始化紫微斗數AI系統...")

            if self.use_crewai:
                # 使用新的 CrewAI + MCP 架構
                self.logger.info("初始化 CrewAI + MCP 架構...")
                self.crew_manager = ZiweiCrewManager(logger=self.logger)
                await self.crew_manager.initialize()
            else:
                # 使用舊的 Multi-Agent 架構
                self.logger.info("初始化 Legacy Multi-Agent 架構...")

                # 1. 初始化 Multi-Agent 協調器
                self.logger.info("初始化 Multi-Agent 協調器...")
                self.coordinator = MultiAgentCoordinator(logger=self.logger)

                # 2. 初始化紫微斗數工具
                self.logger.info("初始化紫微斗數工具...")
                self.ziwei_tool = ZiweiTool(logger=self.logger)

                # 3. 初始化 RAG 系統
                self.logger.info("初始化 RAG 系統...")
                self.rag_system = await self._initialize_rag_system()

                # 4. 初始化 GPT-4o 格式化器
                self.logger.info("初始化 GPT-4o 格式化器...")
                self.formatter = GPT4oFormatter(logger=self.logger)

                # 5. 載入紫微斗數知識庫
                await self._load_knowledge_base()

            self.initialization_time = time.time() - start_time
            self.is_initialized = True

            architecture = "CrewAI + MCP" if self.use_crewai else "Legacy Multi-Agent"
            self.logger.info(f"系統初始化完成 ({architecture})，耗時 {self.initialization_time:.2f} 秒")

        except Exception as e:
            self.logger.error(f"系統初始化失敗: {str(e)}")
            raise

    async def _initialize_rag_system(self) -> ZiweiRAGSystem:
        """初始化 RAG 系統，使用持久化向量庫 test1"""
        try:
            # 配置使用 test1 向量資料庫
            rag_config = {
                "vector_store": {
                    "persist_directory": "./vector_db_test1",
                    "collection_name": "ziwei_knowledge_test1",
                    "embedding_provider": "huggingface",
                    "embedding_model": "BAAI/bge-m3",
                    "embedding_config": {
                        "device": "cpu",
                        "max_length": 1024,
                        "batch_size": 8,
                        "use_fp16": False,
                        "openai_fallback": True,
                        "openai_model": "text-embedding-ada-002"
                    }
                },
                "generator": {
                    "model": "gpt-4o",
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                "rag": {
                    "top_k": 3,  # 減少檢索數量從5到3
                    "min_score": 0.7,  # 提高最小分數，獲得更精確結果
                    "max_context_length": 3000  # 減少上下文長度
                }
            }

            # 創建 RAG 系統實例，使用 test1 資料庫
            rag_system = ZiweiRAGSystem(config=rag_config, logger=self.logger)

            # 檢查 test1 向量庫狀態
            stats = rag_system.get_system_status()
            vector_stats = stats.get('vector_store_stats', {})
            total_docs = vector_stats.get('total_documents', 0)

            self.logger.info(f"使用持久化向量資料庫: test1")
            self.logger.info(f"資料庫位置: ./vector_db_test1")
            self.logger.info(f"集合名稱: ziwei_knowledge_test1")
            self.logger.info(f"包含文檔數: {total_docs}")

            if total_docs > 0:
                self.logger.info("✅ 成功連接到 test1 向量資料庫")
                return rag_system
            else:
                self.logger.warning("⚠️ test1 向量資料庫為空，請檢查資料庫是否正確建立")
                return rag_system

        except Exception as e:
            self.logger.error(f"RAG 系統初始化失敗: {str(e)}")
            raise

    # 移除基礎知識載入函數，因為使用 test1 持久化資料庫
    # test1 資料庫已包含完整的紫微斗數集成全書內容

    async def _load_knowledge_base(self):
        """檢查 test1 向量資料庫狀態"""
        try:
            # 顯示 test1 向量庫統計
            stats = self.rag_system.get_system_status()
            vector_stats = stats.get('vector_store_stats', {})
            total_docs = vector_stats.get('total_documents', 0)

            self.logger.info(f"📊 test1 向量資料庫統計:")
            self.logger.info(f"   總文檔數: {total_docs}")
            self.logger.info(f"   資料庫路徑: {vector_stats.get('persist_directory', 'unknown')}")
            self.logger.info(f"   集合名稱: {vector_stats.get('collection_name', 'unknown')}")

            if total_docs > 0:
                self.logger.info("✅ test1 向量資料庫已就緒，包含紫微斗數集成全書內容")

                # 測試搜索功能
                self.logger.info("🔍 測試向量資料庫搜索功能...")
                test_results = self.rag_system.search_knowledge("紫微星", top_k=2)
                self.logger.info(f"   搜索測試成功，找到 {len(test_results)} 條相關結果")
            else:
                self.logger.warning("⚠️ test1 向量資料庫為空，請重新建立資料庫")

        except Exception as e:
            self.logger.error(f"檢查向量資料庫時發生錯誤: {str(e)}")

    async def _coordinate_with_process_display(self,
                                             agent_input: Dict[str, Any],
                                             domain_type: str,
                                             show_process: bool = False) -> Any:
        """帶過程顯示的協調分析"""
        from src.agents.coordinator import CoordinationStrategy

        if show_process:
            print(f"📊 分析領域: {domain_type}")
            print(f"🎯 協調策略: 討論式協作")
            print(f"👥 參與 Agent: Claude Agent, GPT Agent")
            print("-" * 60)

        # 執行協調分析
        coordination_result = await self.coordinator.coordinate_analysis(
            input_data=agent_input,
            domain_type=domain_type,
            strategy=CoordinationStrategy.DISCUSSION
        )

        if show_process:
            self._display_coordination_process(coordination_result)

        return coordination_result

    def _display_coordination_process(self, coordination_result):
        """顯示協調過程詳情"""
        print("\n📋 協作分析結果:")
        print(f"✅ 協作狀態: {'成功' if coordination_result.success else '失敗'}")
        print(f"⏱️  協作耗時: {coordination_result.total_time:.2f} 秒")
        print(f"🤖 參與 Agent 數量: {len(coordination_result.responses)}")

        if coordination_result.discussion_result:
            discussion = coordination_result.discussion_result
            print(f"💬 討論輪次: {len(discussion.rounds)}")

            for i, round_info in enumerate(discussion.rounds, 1):
                print(f"\n🔄 第 {i} 輪討論 - {round_info.topic}")
                print(f"   參與者: {', '.join(round_info.participants)}")
                print(f"   共識程度: {round_info.consensus_level:.2f}")

                for response in round_info.responses:
                    print(f"\n   🤖 {response.agent_id}:")
                    print(f"      信心度: {response.confidence:.2f}")
                    print(f"      處理時間: {response.processing_time:.2f}s")
                    # 顯示回應內容的前100字
                    content_preview = response.content[:100] + "..." if len(response.content) > 100 else response.content
                    print(f"      回應預覽: {content_preview}")

        print("\n" + "="*60)

    # 移除目錄載入函數，因為使用 test1 持久化資料庫
    # 如需添加新知識，請使用 import_pdf_to_vector_db.py 或 manage_vector_db.py

    async def analyze_ziwei_chart(self,
                                 birth_data: Dict[str, Any],
                                 domain_type: str = "comprehensive",
                                 user_profile: Optional[Dict[str, Any]] = None,
                                 output_format: str = "json",
                                 show_agent_process: bool = False) -> Dict[str, Any]:
        """
        完整的紫微斗數分析流程 (支援 CrewAI + MCP 和 Legacy 架構)

        Args:
            birth_data: 出生資料 (gender, birth_year, birth_month, birth_day, birth_hour)
            domain_type: 分析領域 (love, wealth, future, comprehensive)
            user_profile: 用戶背景資料
            output_format: 輸出格式 (json, detailed, summary, etc.)
            show_agent_process: 是否顯示 Agent 處理過程

        Returns:
            完整的分析結果
        """
        if not self.is_initialized:
            await self.initialize()

        try:
            start_time = time.time()
            architecture = "CrewAI + MCP" if self.use_crewai else "Legacy Multi-Agent"
            self.logger.info(f"開始分析紫微斗數命盤 ({architecture})，領域: {domain_type}")

            if self.use_crewai:
                # 使用新的 CrewAI + MCP 架構
                return await self._analyze_with_crewai(
                    birth_data=birth_data,
                    domain_type=domain_type,
                    output_format=output_format,
                    show_process=show_agent_process,
                    start_time=start_time
                )
            else:
                # 使用舊的 Legacy 架構
                return await self._analyze_with_legacy(
                    birth_data=birth_data,
                    domain_type=domain_type,
                    user_profile=user_profile,
                    output_format=output_format,
                    show_agent_process=show_agent_process,
                    start_time=start_time
                )

        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"分析失敗: {str(e)} (耗時 {processing_time:.2f}s)")

            return {
                "success": False,
                "error": str(e),
                "processing_time": processing_time,
                "architecture": "CrewAI + MCP" if self.use_crewai else "Legacy Multi-Agent",
                "timestamp": datetime.now().isoformat()
            }

    async def _analyze_with_crewai(self, birth_data: Dict[str, Any], domain_type: str,
                                  output_format: str, show_process: bool, start_time: float) -> Dict[str, Any]:
        """使用 CrewAI + MCP 架構進行分析"""
        try:
            self.logger.info("🚀 使用 CrewAI + MCP 架構進行分析...")

            if show_process:
                print(f"🤖 架構: CrewAI + MCP")
                print(f"📊 分析領域: {domain_type}")
                print(f"📝 輸出格式: {output_format}")
                print("-" * 60)

            # 調用 CrewAI 管理器進行分析
            result = await self.crew_manager.analyze_ziwei_chart(
                birth_data=birth_data,
                domain_type=domain_type,
                output_format=output_format
            )

            if show_process and result.get("success", False):
                metadata = result.get("metadata", {})
                print(f"\n✅ CrewAI 分析完成:")
                print(f"   處理時間: {metadata.get('processing_time', 0):.2f}s")
                print(f"   使用的 Agents: {', '.join(metadata.get('agents_used', []))}")
                print(f"   完成的任務: {metadata.get('tasks_completed', 0)} 個")
                print("=" * 60)

            # 添加總處理時間
            total_time = time.time() - start_time
            if isinstance(result, dict):
                result["total_processing_time"] = total_time
                result["architecture"] = "CrewAI + MCP"

            return result

        except Exception as e:
            self.logger.error(f"CrewAI 分析失敗: {str(e)}")
            raise

    async def _analyze_with_legacy(self, birth_data: Dict[str, Any], domain_type: str,
                                  user_profile: Optional[Dict[str, Any]], output_format: str,
                                  show_agent_process: bool, start_time: float) -> Dict[str, Any]:
        """使用 Legacy Multi-Agent 架構進行分析"""
        try:
            self.logger.info("🔄 使用 Legacy Multi-Agent 架構進行分析...")

            # 1. 獲取紫微斗數命盤數據
            self.logger.info("步驟 1: 獲取命盤數據...")
            chart_data = self.ziwei_tool.get_ziwei_chart(birth_data)

            if not chart_data.get('success', False):
                error_msg = chart_data.get('error', '未知錯誤')
                self.logger.error(f"命盤獲取失敗: {error_msg}")

                # 使用智能錯誤處理器提供詳細指導
                if "輸入數據驗證失敗" in error_msg:
                    error_guidance = get_error_guidance("data_validation", {
                        "error_details": error_msg
                    })
                    detailed_error = error_guidance["message"]
                elif "網絡" in error_msg or "連接" in error_msg:
                    error_guidance = get_error_guidance("network_error", {
                        "error_details": error_msg
                    })
                    detailed_error = error_guidance["message"]
                else:
                    error_guidance = get_error_guidance("parsing_error", {
                        "error_details": error_msg
                    })
                    detailed_error = error_guidance["message"]

                raise ValueError(detailed_error)

            # 檢查數據質量
            data_quality = chart_data.get('data_quality', {})
            if data_quality and not data_quality.get('valid', True):
                self.logger.warning(f"命盤數據質量較低: {data_quality}")

                # 生成數據質量警告信息
                quality_guidance = get_error_guidance("data_quality", {
                    "quality_info": data_quality
                })
                self.logger.info(f"數據質量指導: {quality_guidance['message'][:200]}...")
                # 記錄警告但繼續處理
            
            # 2. RAG 知識檢索
            self.logger.info("步驟 2: 檢索相關知識...")
            knowledge_context = await self._retrieve_knowledge(chart_data, domain_type)
            
            # 3. Multi-Agent 協作分析
            self.logger.info("步驟 3: Multi-Agent 協作分析...")

            if show_agent_process:
                print("\n" + "="*60)
                print("🤖 Multi-Agent 協作分析過程")
                print("="*60)

            agent_input = {
                'chart_data': chart_data,
                'knowledge_context': knowledge_context,
                'birth_data': birth_data,
                'user_profile': user_profile or {}
            }

            coordination_result = await self._coordinate_with_process_display(
                agent_input=agent_input,
                domain_type=domain_type,
                show_process=show_agent_process
            )
            
            if not coordination_result.success:
                raise ValueError("Multi-Agent 協作分析失敗")
            
            # 4. GPT-4o 格式化輸出
            self.logger.info("步驟 4: 格式化最終輸出...")
            formatted_result = await self.formatter.format_coordination_result(
                coordination_result=coordination_result,
                domain_type=domain_type,
                user_profile={
                    'birth_data': birth_data,
                    'analysis_time': datetime.now().isoformat(),
                    'processing_time': time.time() - start_time,
                    'agent_responses': len(coordination_result.responses)
                },
                output_format=output_format
            )
            
            processing_time = time.time() - start_time
            self.logger.info(f"分析完成，總耗時: {processing_time:.2f} 秒")
            
            # 檢查格式化是否成功
            if formatted_result.success:
                return {
                    'success': True,
                    'result': formatted_result.formatted_content,
                    'metadata': {
                        'processing_time': processing_time,
                        'formatting_time': formatted_result.processing_time,
                        'validation_passed': formatted_result.validation_passed,
                        'chart_data': chart_data,
                        'domain_type': domain_type,
                        'timestamp': datetime.now().isoformat()
                    }
                }
            else:
                return {
                    'success': False,
                    'result': formatted_result.formatted_content,
                    'error': '格式化失敗',
                    'metadata': {
                        'processing_time': processing_time,
                        'chart_data': chart_data,
                        'domain_type': domain_type,
                        'timestamp': datetime.now().isoformat()
                    }
                }
            
        except Exception as e:
            self.logger.error(f"分析過程中發生錯誤: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _retrieve_knowledge(self, chart_data: Dict[str, Any], domain_type: str) -> str:
        """檢索相關知識（帶快取）"""
        try:
            # 檢查快取
            cache_key = {
                'chart_data': chart_data,
                'domain_type': domain_type,
                'operation': 'knowledge_retrieval'
            }

            cached_result = self.cache_manager.get(cache_key)
            if cached_result is not None:
                self.logger.info("使用快取的知識檢索結果")
                return cached_result
            # 構建查詢
            query_parts = []
            
            # 從命盤數據提取關鍵信息
            if 'data' in chart_data and 'palace' in chart_data['data']:
                palaces = chart_data['data']['palace']
                for palace_name, stars in palaces.items():
                    if isinstance(stars, list):
                        query_parts.extend(stars)
                    query_parts.append(palace_name)
            
            # 添加領域相關查詢
            domain_queries = {
                'love': ['愛情', '婚姻', '感情', '夫妻宮'],
                'wealth': ['財富', '財運', '財帛宮', '事業'],
                'future': ['未來', '運勢', '大運', '流年'],
                'comprehensive': ['命盤', '整體', '綜合']
            }
            
            query_parts.extend(domain_queries.get(domain_type, domain_queries['comprehensive']))
            
            # 執行知識檢索 - 優化檢索參數
            query = ' '.join(query_parts[:8])  # 進一步限制查詢長度
            knowledge_results = self.rag_system.search_knowledge(query, top_k=3, min_score=0.7)
            
            # 整合知識片段
            knowledge_texts = [result['content'] for result in knowledge_results]
            knowledge_context = '\n\n'.join(knowledge_texts)

            # 快取結果
            self.cache_manager.set(cache_key, knowledge_context)

            return knowledge_context
            
        except Exception as e:
            self.logger.error(f"知識檢索失敗: {str(e)}")
            return "無法檢索到相關知識"
    
    def get_system_status(self) -> Dict[str, Any]:
        """獲取系統狀態"""
        return {
            'initialized': self.is_initialized,
            'initialization_time': self.initialization_time,
            'components': {
                'coordinator': self.coordinator is not None,
                'ziwei_tool': self.ziwei_tool is not None,
                'rag_system': self.rag_system is not None,
                'formatter': self.formatter is not None
            },
            'rag_stats': self.rag_system.get_system_status() if self.rag_system else None,
            'timestamp': datetime.now().isoformat()
        }

    async def cleanup(self):
        """清理系統資源"""
        try:
            self.logger.info("開始清理系統資源...")

            # 清理各個組件
            if self.coordinator:
                # 如果協調器有清理方法，調用它
                if hasattr(self.coordinator, 'cleanup'):
                    await self.coordinator.cleanup()
                self.coordinator = None

            if self.ziwei_tool:
                # 如果工具有清理方法，調用它
                if hasattr(self.ziwei_tool, 'cleanup'):
                    await self.ziwei_tool.cleanup()
                self.ziwei_tool = None

            if self.rag_system:
                # 如果 RAG 系統有清理方法，調用它
                if hasattr(self.rag_system, 'cleanup'):
                    await self.rag_system.cleanup()
                self.rag_system = None

            if self.formatter:
                # 如果格式化器有清理方法，調用它
                if hasattr(self.formatter, 'cleanup'):
                    await self.formatter.cleanup()
                self.formatter = None

            self.is_initialized = False
            self.logger.info("✅ 系統資源清理完成")

        except Exception as e:
            self.logger.error(f"清理系統資源時發生錯誤: {str(e)}")


# 便捷函數
async def create_ziwei_ai_system() -> ZiweiAISystem:
    """創建並初始化紫微斗數AI系統"""
    system = ZiweiAISystem()
    await system.initialize()
    return system


async def quick_analysis(birth_data: Dict[str, Any], domain_type: str = "comprehensive") -> Dict[str, Any]:
    """快速分析函數"""
    system = await create_ziwei_ai_system()
    return await system.analyze_ziwei_chart(birth_data, domain_type)


# 主程式入口
async def main():
    """主程式入口"""
    print("🌟 紫微斗數AI系統")
    print("=" * 50)
    
    try:
        # 創建系統
        system = await create_ziwei_ai_system()
        
        # 顯示系統狀態
        status = system.get_system_status()
        print(f"✅ 系統初始化完成")
        print(f"⏱️  初始化時間: {status['initialization_time']:.2f} 秒")
        
        # 示例分析
        print("\n📊 執行示例分析...")
        
        sample_birth_data = {
            "gender": "男",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "birth_hour": "午"
        }
        
        # 測試 JSON 轉論述格式（使用 JSON prompt 但輸出論述）
        result = await system.analyze_ziwei_chart(
            birth_data=sample_birth_data,
            domain_type="comprehensive",  # 🎯 在這裡選擇領域：love, wealth, future, comprehensive
            output_format="json_to_narrative",  # 🎯 使用 JSON prompt 但輸出論述格式
            show_agent_process=True  # 🎯 顯示 Agent 協作過程（True=顯示, False=隱藏）
        )
        
        if result['success']:
            print("✅ 分析完成")
            print(f"⏱️  處理時間: {result['metadata']['processing_time']:.2f} 秒")
            print("\n📋 分析結果:")

            # 檢查輸出格式並相應處理
            formatted_result = result['result']

            # 檢查是否為論述格式（通常是純文本）
            if isinstance(formatted_result, str) and not formatted_result.strip().startswith('{'):
                # 論述格式，直接顯示
                print(formatted_result)
            elif isinstance(formatted_result, str):
                try:
                    # 嘗試解析 JSON 字符串
                    parsed_result = json.loads(formatted_result)
                    print(json.dumps(parsed_result, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    # 如果不是有效的 JSON，直接顯示字符串
                    print(formatted_result)
            else:
                # 如果已經是字典或其他對象，直接序列化
                print(json.dumps(formatted_result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 分析失敗: {result['error']}")

        # 清理系統資源
        await system.cleanup()

    except Exception as e:
        print(f"❌ 系統運行錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # 確保清理所有 asyncio 任務
        try:
            # 取消所有未完成的任務（排除當前任務）
            current_task = asyncio.current_task()
            tasks = [task for task in asyncio.all_tasks() if not task.done() and task != current_task]
            if tasks:
                print(f"🧹 清理 {len(tasks)} 個未完成的任務...")
                for task in tasks:
                    if not task.cancelled():
                        task.cancel()

                # 等待任務取消完成，但設置超時避免無限等待
                try:
                    await asyncio.wait_for(
                        asyncio.gather(*tasks, return_exceptions=True),
                        timeout=5.0
                    )
                except asyncio.TimeoutError:
                    print("⚠️ 任務清理超時，但程序將正常退出")
        except Exception as cleanup_error:
            print(f"⚠️ 清理過程中發生錯誤: {cleanup_error}")


if __name__ == "__main__":
    asyncio.run(main())
