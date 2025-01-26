
from datetime import timedelta

from fastapi import status
from freezegun import freeze_time
from sqlalchemy import select

from app.core.utils import get_now_utc
from app.enums.security_enums import TokenAuth
from app.models.user_model import RefreshTokenOrm


# user_id 누락 토큰 재요청
def test_logout_missing_userid(test_auth_client):
    response = test_auth_client.post(
        "/users/logout",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "user_id"


# 만료된 access token으로 요청
def test_logout_expired_access_token(test_client, login_data):
    # freeze_time으로 하여 강제로 시간을 앞당긴다
    with freeze_time(get_now_utc() + timedelta(hours=1)):
        response = test_client.post(
            "/users/refresh",
            json={
                "user_id": login_data["login_body"]["user_id"],
                "refresh_token": login_data["login_body"]["refresh_token"]
            },
            headers={
                "Authorization": f"Bearer {login_data['login_body']['access_token']}"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        rst_body = response.json()
        assert rst_body["detail"] == TokenAuth.ACCESS_TOKEN_EXPIRED


# auto header 미포함 요청
def test_logout_not_auth_header(test_client):
    response = test_client.post(
        "/users/logout",
        json={"user_id": 1}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    rst_body = response.json()
    assert rst_body["detail"] == "Not authenticated"


# access token과 다른 정보의 user_id 요청
def test_logout_not_found_userid(test_auth_client):
    response = test_auth_client.post(
        "/users/logout",
        json={"user_id": -1}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    rst_body = response.json()
    assert rst_body["detail"] == TokenAuth.INVALID_TOKEN


# logout success
def test_logout_success(test_auth_client, test_db, login_data):
    user_id = login_data["login_body"]["user_id"]
    refresh_token = login_data["login_body"]["refresh_token"]
    response = test_auth_client.post(
        "/users/logout",
        json={
            "user_id": user_id,
        }
    )

    assert response.status_code == status.HTTP_200_OK
    user_refresh_query = select(RefreshTokenOrm).where(RefreshTokenOrm.user_id == user_id)
    user_refresh = test_db.scalar(user_refresh_query)
    assert user_refresh.refresh_token is None

    # 동일한 refresh token으로 토큰 재발급 시도 테스트
    retry_response = test_auth_client.post(
        "/users/refresh",
        json={
            "user_id": user_id,
            "refresh_token": refresh_token
        }
    )
    assert retry_response.status_code == status.HTTP_401_UNAUTHORIZED
    rst_body = retry_response.json()
    assert rst_body["detail"] == TokenAuth.INVALID_TOKEN


