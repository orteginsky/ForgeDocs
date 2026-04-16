import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ForgeDocs"
    
    # Auth settings
    # Prioridad 1: JSON completo del token (leído desde la env var FORGE_DOCS_TOKEN de GCP)
    FORGE_DOCS_TOKEN: Optional[str] = os.getenv("FORGE_DOCS_TOKEN")
    
    # Prioridad 2: Ruta al archivo local (para desarrollo)
    GOOGLE_TOKEN_FILE: str = os.getenv("GOOGLE_TOKEN_FILE", "/home/ortega/ForgeDocs/token.json")
    
    # Workspace settings
    WORKSPACE_DOMAIN: str = os.getenv("WORKSPACE_DOMAIN", "supportmendoza.com")
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "charming-sonar-489918-f3")

    class Config:
        env_file = ".env"
        extra = "ignore" # Ignorar variables extra en el .env (como GOOGLE_CREDENTIALS_PATH)

settings = Settings()
