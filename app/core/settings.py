from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "mysql+pymysql://adoc:adoc@mysql-container.docker/adoc"
    MONGODB_URI: str = "mongodb://adoc:adoc@mongodb-container.docker:27017/adoc?authSource=admin"
    MONGO_DB_NAME: str = "adoc"

    TEST_DB_URL: str = "mysql+pymysql://adoc:adoc@mysql-container.docker/test"
    TEST_MONGODB_URI: str = "mongodb://adoc:adoc@mongodb-container.docker:27017/test?authSource=admin"
    TEST_MONGO_DB_NAME: str = "test"

    INIT_USER_EMAIL: str = "test@test.com"
    INIT_USER_PASSWORD: str = "test"

    JWT_SECRET_KEY: str = "SN7tHQSm9zmPUzU6X2dMWojt8zpV3D3pXoGPg8MV5b2xnHk"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECS: int = 20 # 15분
    REFRESH_TOKEN_EXPIRE_SECS: int = 259200 # 3일



settings = Settings()
