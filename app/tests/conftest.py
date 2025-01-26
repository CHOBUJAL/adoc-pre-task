from datetime import timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
from mongoengine.context_managers import switch_db
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.core.security import get_current_user_info
from app.core.settings import settings
from app.core.utils import get_now_utc
from app.main import app
from app.models.board_model import Board
from app.models.model import Base
from app.models.user_model import UserOrm
from app.schemas.user_schemas import JwtPayLoad


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


@pytest.fixture()
def test_mongo_connection():
    # MongoDB 연결
    connection = connect(
        db=settings.TEST_MONGO_DB_NAME,
        alias=settings.TEST_MONGO_DB_NAME,
        host=settings.TEST_MONGODB_URI
    )
    connection.drop_database(settings.TEST_MONGO_DB_NAME)
    yield connection
    disconnect(alias=settings.TEST_MONGO_DB_NAME)


@pytest.fixture()
def mock_board(test_mongo_connection) -> Board:
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        for i in range(2):
            for j in range(2):
                user_id = i+1
                temp_post = TestBoard(
                    author_id=user_id,
                    title=f"mock_{user_id}_{j}",
                    content=(
                                f"mock content from user {user_id} "
                                f"this is mock {j} * {j} content"
                            ),
                    created_at=get_now_utc()
                )
                temp_post.save()

# 게시판 리스트 관련 테스트를 위 총 3개의 유저 아이디
# 각 유저마다 10개의 게시글 작성하도록 구성
@pytest.fixture()
def mock_many_boards(test_mongo_connection) -> Board:
    sample_created_at = get_now_utc()
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        for i in range(3):
            for j in range(i+10):
                sample_created_at += timedelta(minutes=86)
                user_id = i+1
                temp_post = TestBoard(
                    author_id=user_id,
                    title=f"mock_{user_id}_{j}",
                    content=(
                                f"mock content from user {user_id} "
                                f"this is mock {j} * {j} content"
                            ),
                    created_at=sample_created_at
                )
                temp_post.save()
