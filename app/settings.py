from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql://postgres:postgres@postgres:5432/postgres"

    INIT_USER_NAME: str = "test"
    INIT_USER_EMAIL: str = "test@test.com"
    INIT_USER_PHONE_NUM: str = "010-1111-2222"
    INIT_USER_PASSWORD: str = "test"
    INIT_USER_ADDR: str = "test"



settings = Settings()
