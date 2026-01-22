from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Industrial AI Platform"
    VERSION: str = "1.0.0"
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # ChromaDB Settings
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"
    COLLECTION_NAME: str = "industrial_docs"
    
    # Agent Settings
    MAX_AGENT_ITERATIONS: int = 5
    AGENT_TEMPERATURE: float = 0.7
    
    # Data Settings
    EQUIPMENT_DATA_PATH: str = "./data/equipment_data.json"
    MAINTENANCE_LOGS_PATH: str = "./data/maintenance_logs.json"
    SENSOR_DATA_PATH: str = "./data/sensor_data.json"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
