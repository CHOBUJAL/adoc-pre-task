from typing import Any

import pytest
from fastapi.testclient import TestClient
from mongoengine import connect
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.core.security import get_current_user_info
from app.core.settings import settings
from app.main import app
from app.models.model import Base
from app.models.user_model import UserOrm
from app.schemas.user_schemas import JwtPayLoad

connect(db='adoc', host='mongodb://adoc:adoc@mongodb-container.docker:27017/adoc?authSource=admin')



@pytest.fixture()
def test_db():
    engine = create_engine(settings.TEST_DB_URL)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)

# 토큰 인증이 필요없는 경우와 access 토큰에 대한 검증이 필요한 경우
# 해당 cilent를 사용하면 된다
@pytest.fixture()
def test_client(test_db) -> TestClient:
    app.dependency_overrides[get_db_session] = lambda: test_db
    yield TestClient(app)
    app.dependency_overrides = {}


# 토큰 인증 디펜던시를 정상적으로 처리된 형태로 테스트를 원하는 경우
# 해당 client를 사용하면 된다
@pytest.fixture()
def test_auth_client(test_client):
    app.dependency_overrides[get_current_user_info] = lambda: JwtPayLoad(user_id=1)
    yield test_client
    app.dependency_overrides = {}


@pytest.fixture()
def mock_user(test_db) -> UserOrm:
    mock_user = UserOrm(
        email="test@test.com",
        hashed_password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash("mock_password")
    )
    test_db.add(mock_user)
    test_db.commit()
    test_db.refresh(mock_user)

    return mock_user


@pytest.fixture
def login_data(test_client: TestClient, mock_user) -> dict[str, Any]:
    response = test_client.post(
        "/users/login",
        json={"email": mock_user.email, "password": "mock_password"}
    )
    return {"login_body": response.json(), "mock_user": mock_user}
