from datetime import timedelta

from fastapi import status
from freezegun import freeze_time
from mongoengine.context_managers import switch_db

from app.core.settings import settings
from app.core.utils import get_now_utc
from app.enums.common_enums import ResultMessage
from app.enums.security_enums import TokenAuth
from app.models.board_model import Board


# auto header 미포함 요청
def test_board_create_not_auth_header(test_client):
    response = test_client.post(
        "/boards",
        json={"title": "test", "content": "test"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    rst_body = response.json()
    assert rst_body["detail"] == "Not authenticated"


# 제목 필드 누락 요청
def test_board_create_missing_title(test_auth_client):
    response = test_auth_client.post(
        "/boards",
        json={"content": "test"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "title"


# 내용 필드 누락 요청
def test_board_create_missing_content(test_auth_client):
    response = test_auth_client.post(
        "/boards",
        json={"title": "test"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "content"


# 만료된 access token으로 요청
def test_board_create_expired_token(test_client, login_data):
    # freeze_time으로 하여 강제로 시간을 앞당긴다
    with freeze_time(get_now_utc() + timedelta(hours=1)):
        response = test_client.post(
            "/boards",
            json={"title": "test", "content": "test"},
            headers={
                "Authorization": f"Bearer {login_data['login_body']['access_token']}"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        rst_body = response.json()
        assert rst_body["detail"] == TokenAuth.ACCESS_TOKEN_EXPIRED


# 정상 요청
def test_board_create_success(test_auth_client, test_mongo_connection):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_auth_client.post(
            "/boards",
            json={"title": "test", "content": "123test123"}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        created_post_id = rst_body["post_id"]
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert created_post_id
        assert rst_body["status_code"] == 200

        get_response = test_auth_client.get(
            f"/boards/{created_post_id}",
        )
        assert get_response.status_code == status.HTTP_200_OK
        rst_body = get_response.json()
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert rst_body["status_code"] == 200
        assert rst_body["post"]["post_id"] == created_post_id
        assert rst_body["post"]["author_id"] == 1
        assert rst_body["post"]["title"] == "test"
        assert rst_body["post"]["content"] == "123test123"
