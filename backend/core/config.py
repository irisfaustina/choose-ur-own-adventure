from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Setting(BaseSettings): #env variables config to be loaded
    
    API_PREFIX: str = "/api"
    
    DEBUG: bool = False

    DATABASE_URL: str

    ALLOWED_ORIGINS: List[str] = ""
    
    OPENAI_API_KEY: str
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            # Handles comma-separated or empty string
            return [o.strip() for o in v.split(',') if o.strip()]
        elif isinstance(v, list):
            # Already a list, just return as-is
            return v
        return []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Setting() #when we create the setting clas auto load env variables