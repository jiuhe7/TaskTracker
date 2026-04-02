from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    SECRET_KEY: str
    ALGORITHM:str='HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    model_config = SettingsConfigDict(
        env_file=".env",  # 指定环境变量文件路径
        env_file_encoding="utf-8",  # 环境变量文件编码
        extra="ignore"  # 忽略未定义的环境变量，避免加载错误
    )

settings=Settings()