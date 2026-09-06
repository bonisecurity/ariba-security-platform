import os
from pathlib import Path
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Ariba Manager configuration settings."""
    
    # Server settings
    project_name: str = "Ariba Security Manager"
    api_v1_str: str = "/api/v1"
    secret_key: str = Field(default="change-this-secret", env="ARBA_SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Database settings
    database_url: str = Field(
        default="postgresql://postgres:password@localhost:5432/ariba",
        env="DATABASE_URL"
    )
    
    # OpenSearch settings
    opensearch_hosts: list = Field(
        default=["http://localhost:9200"],
        env="OPENSEARCH_HOSTS"
    )
    opensearch_user: str = Field(default="admin", env="OPENSEARCH_USER")
    opensearch_password: str = Field(default="admin123", env="OPENSEARCH_PASSWORD")
    
    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # CORS settings
    backend_cors_origins: list = ["*"]
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Paths
    base_dir: Path = Field(default=Path(__file__).parent.parent.parent)
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()