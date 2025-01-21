from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "mysql+pymysql://adoc:adoc@mysql-container.docker/adoc"
    MONGODB_URI: str = "mongodb://mongodb-container.docker:27017"

    INIT_USER_EMAIL: str = "test@test.com"
    INIT_USER_PASSWORD: str = "test"
    
    JWT_SECRET_KEY: str = "SN7tHQSm9zmPUzU6X2dMWojt8zpV3D3pXoGPg8MV5b2xnHk"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECS: int = 900  # 15min
    REFRESH_TOKEN_EXPIRE_SECS: int = 604800  # 7day



settings = Settings()
