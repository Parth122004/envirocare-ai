from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EnviroCare AI"
    mongodb_uri: str = "mongodb+srv://ingleparth2004_db_user:1234@envirocare-cluster.pwblje.mongodb.net/envirocare_db?retryWrites=true&w=majority"


    database_name: str = "envirocare_db"

    jwt_secret_key: str = "SUPER_SECRET_KEY_CHANGE_ME"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    iqair_api_key: str = "CHANGE_ME"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"   # <-- THIS FIXES YOUR ERROR
    )

settings = Settings()
