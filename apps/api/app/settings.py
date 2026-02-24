from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str

    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()