"""
系統配置管理
"""

import os
from typing import Optional, List, Dict, Any
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class OpenAISettings(BaseSettings):
    """OpenAI API 設定"""
    api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    base_url: str = Field("https://api.openai.com/v1", env="OPENAI_BASE_URL")
    model_gpt4o: str = Field("gpt-4o-mini", env="OPENAI_MODEL_GPT4O")
    model_gpt4: str = Field("gpt-4-turbo", env="OPENAI_MODEL_GPT4")
    timeout: int = Field(30, env="OPENAI_TIMEOUT")  # 減少OpenAI API超時
    max_retries: int = Field(3, env="OPENAI_MAX_RETRIES")

    model_config = {"protected_namespaces": ()}

class AnthropicSettings(BaseSettings):
    """Anthropic Claude API 設定"""
    api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    base_url: str = Field("https://api.anthropic.com", env="ANTHROPIC_BASE_URL")
    model: str = Field("claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")
    timeout: int = Field(35, env="ANTHROPIC_TIMEOUT")  # 減少Anthropic API超時
    max_retries: int = Field(3, env="ANTHROPIC_MAX_RETRIES")

class MCPSettings(BaseSettings):
    """MCP 設定 (支援統一 MCP 服務器)"""
    # 舊的 Claude MCP 設定 (保留兼容性)
    server_host: str = Field("localhost", env="MCP_SERVER_HOST")
    server_port: int = Field(3000, env="MCP_SERVER_PORT")
    server_name: str = Field("ziwei-mcp-server", env="MCP_SERVER_NAME")
    tools_enabled: str = Field(
        "ziwei_chart,web_scraper,data_parser",
        env="MCP_TOOLS_ENABLED"
    )
    timeout: int = Field(30, env="MCP_TIMEOUT")

    # 新的統一 MCP 服務器設定
    unified_server_enabled: bool = Field(True, env="MCP_UNIFIED_SERVER_ENABLED")
    unified_server_host: str = Field("localhost", env="MCP_UNIFIED_SERVER_HOST")
    unified_server_port: int = Field(8001, env="MCP_UNIFIED_SERVER_PORT")
    unified_server_timeout: int = Field(60, env="MCP_UNIFIED_SERVER_TIMEOUT")
    max_retries: int = Field(3, env="MCP_MAX_RETRIES")
    enable_logging: bool = Field(True, env="MCP_ENABLE_LOGGING")

    # 工具配置
    tools_config: Dict[str, Any] = {
        "ziwei_scraper": {
            "enabled": True,
            "timeout": 60,
            "max_retries": 3
        },
        "rag_knowledge": {
            "enabled": True,
            "timeout": 30,
            "max_retries": 2
        },
        "format_output": {
            "enabled": True,
            "timeout": 20,
            "max_retries": 2
        },
        "data_validator": {
            "enabled": True,
            "timeout": 10,
            "max_retries": 1
        }
    }

    def get_tools_enabled_list(self) -> List[str]:
        """獲取啟用工具列表"""
        return [tool.strip() for tool in self.tools_enabled.split(",")]

    def get_unified_server_url(self) -> str:
        """獲取統一 MCP 服務器 URL"""
        return f"http://{self.unified_server_host}:{self.unified_server_port}"

class RAGSettings(BaseSettings):
    """RAG 系統設定"""
    vector_db_type: str = Field("chromadb", env="VECTOR_DB_TYPE")
    vector_db_path: str = Field("./data/vector_db", env="VECTOR_DB_PATH")
    vector_db_collection: str = Field("ziwei_knowledge", env="VECTOR_DB_COLLECTION")
    embedding_model: str = Field("text-embedding-ada-002", env="EMBEDDING_MODEL")
    embedding_provider: str = Field("openai", env="EMBEDDING_PROVIDER")
    chunk_size: int = Field(1000, env="RAG_CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="RAG_CHUNK_OVERLAP")
    top_k: int = Field(5, env="RAG_TOP_K")

class MultiAgentSettings(BaseSettings):
    """Multi-Agent 系統設定 (Legacy + CrewAI)"""
    # Legacy Multi-Agent 設定
    claude_agent_enabled: bool = Field(True, env="CLAUDE_AGENT_ENABLED")
    gpt_agent_enabled: bool = Field(True, env="GPT_AGENT_ENABLED")
    domain_agent_enabled: bool = Field(True, env="DOMAIN_AGENT_ENABLED")

    claude_agent_role: str = Field("reasoning_analysis", env="CLAUDE_AGENT_ROLE")
    gpt_agent_role: str = Field("creative_interpretation", env="GPT_AGENT_ROLE")
    domain_agent_role: str = Field("professional_expertise", env="DOMAIN_AGENT_ROLE")

    coordinator_max_iterations: int = Field(5, env="COORDINATOR_MAX_ITERATIONS")
    coordinator_timeout: int = Field(45, env="COORDINATOR_TIMEOUT")  # 減少協調器超時

class CrewAISettings(BaseSettings):
    """CrewAI 框架設定"""
    enabled: bool = Field(True, env="CREWAI_ENABLED")
    verbose: bool = Field(True, env="CREWAI_VERBOSE")
    memory_enabled: bool = Field(True, env="CREWAI_MEMORY_ENABLED")

    # Agent 設定
    max_iter: int = Field(5, env="CREWAI_MAX_ITER")
    max_execution_time: int = Field(300, env="CREWAI_MAX_EXECUTION_TIME")  # 5分鐘

    # 任務設定
    process_type: str = Field("sequential", env="CREWAI_PROCESS_TYPE")  # sequential, hierarchical

    # 工具設定
    tools_timeout: int = Field(60, env="CREWAI_TOOLS_TIMEOUT")
    tools_max_retries: int = Field(3, env="CREWAI_TOOLS_MAX_RETRIES")

    # 性能設定
    parallel_execution: bool = Field(False, env="CREWAI_PARALLEL_EXECUTION")
    cache_enabled: bool = Field(True, env="CREWAI_CACHE_ENABLED")

class AppSettings(BaseSettings):
    """應用程式設定"""
    host: str = Field("localhost", env="APP_HOST")
    port: int = Field(8000, env="APP_PORT")
    debug: bool = Field(True, env="APP_DEBUG")
    log_level: str = Field("INFO", env="APP_LOG_LEVEL")
    secret_key: Optional[str] = Field(None, env="SECRET_KEY")
    cors_origins: str = Field(
        "http://localhost:3000,http://localhost:8080",
        env="CORS_ORIGINS"
    )

    def get_cors_origins_list(self) -> List[str]:
        """獲取 CORS origins 列表"""
        return [origin.strip() for origin in self.cors_origins.split(",")]

class ZiweiWebsiteSettings(BaseSettings):
    """紫微斗數網站設定"""
    url: str = Field("https://fate.windada.com/cgi-bin/fate", env="ZIWEI_WEBSITE_URL")
    timeout: int = Field(30, env="ZIWEI_REQUEST_TIMEOUT")
    max_retries: int = Field(3, env="ZIWEI_MAX_RETRIES")
    user_agent: str = Field(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        env="ZIWEI_USER_AGENT"
    )

class LoggingSettings(BaseSettings):
    """日誌設定"""
    file_path: str = Field("./logs/app.log", env="LOG_FILE_PATH")
    max_size: str = Field("10MB", env="LOG_MAX_SIZE")
    backup_count: int = Field(5, env="LOG_BACKUP_COUNT")
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    metrics_port: int = Field(9090, env="METRICS_PORT")

class CacheSettings(BaseSettings):
    """快取設定"""
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")
    redis_password: Optional[str] = Field(None, env="REDIS_PASSWORD")
    
    ttl_ziwei_chart: int = Field(3600, env="CACHE_TTL_ZIWEI_CHART")
    ttl_rag_results: int = Field(1800, env="CACHE_TTL_RAG_RESULTS")

class Settings(BaseSettings):
    """主要設定類別"""

    # 子設定
    openai: OpenAISettings = OpenAISettings()
    anthropic: AnthropicSettings = AnthropicSettings()
    mcp: MCPSettings = MCPSettings()
    rag: RAGSettings = RAGSettings()
    multi_agent: MultiAgentSettings = MultiAgentSettings()
    crewai: CrewAISettings = CrewAISettings()
    app: AppSettings = AppSettings()
    ziwei_website: ZiweiWebsiteSettings = ZiweiWebsiteSettings()
    logging: LoggingSettings = LoggingSettings()
    cache: CacheSettings = CacheSettings()
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

# 全域設定實例
settings = Settings()

def get_settings() -> Settings:
    """獲取設定實例"""
    return settings

def validate_settings() -> bool:
    """驗證設定完整性"""
    try:
        # 檢查必要的API金鑰
        if not settings.openai.api_key or settings.openai.api_key == "your_openai_api_key_here":
            raise ValueError("OpenAI API key is required")
        
        if not settings.anthropic.api_key or settings.anthropic.api_key == "your_anthropic_api_key_here":
            raise ValueError("Anthropic API key is required")
        
        if not settings.app.secret_key or settings.app.secret_key == "your_secret_key_here":
            raise ValueError("Secret key is required")
        
        # 檢查目錄存在
        os.makedirs(os.path.dirname(settings.rag.vector_db_path), exist_ok=True)
        os.makedirs(os.path.dirname(settings.logging.file_path), exist_ok=True)
        
        return True
        
    except Exception as e:
        print(f"Settings validation failed: {e}")
        return False

# 在模組載入時驗證設定（暫時禁用以避免啟動問題）
# if __name__ != "__main__":
#     if not validate_settings():
#         print("Warning: Settings validation failed. Please check your .env file.")
