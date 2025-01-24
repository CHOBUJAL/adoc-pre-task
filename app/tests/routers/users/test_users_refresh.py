from datetime import timedelta

from fastapi import status
from freezegun import freeze_time

from app.core.utils import get_now_utc
from app.enums.security_enums import TokenAuth


# user_id 누락 토큰 재요청
def test_refresh_missing_userid(test_auth_client):
    response = test_auth_client.post(
        "/users/refresh",
        json={"refresht_token": "123213"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "user_id"


# refresh_token 누락 토큰 재요청
def test_refresh_missing_refreshtoken(test_auth_client):
    response = test_auth_client.post(
        "/users/refresh",
        json={"user_id": "1"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "refresh_token"


# 만료된 refresh token으로 요청
def test_expired_refresh_token(test_auth_client, login_data):
    # freeze_time으로 하여 강제로 시간을 앞당긴다
    with freeze_time(get_now_utc() + timedelta(days=10)):
        response = test_auth_client.post(
            "/users/refresh",
            json={
                "user_id": login_data["login_body"]["user_id"],
                "refresh_token": login_data["login_body"]["refresh_token"]
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        rst_body = response.json()
        assert rst_body["detail"] == TokenAuth.REFRESH_TOKEN_EXPIRED


# refresh token payload의 user_id와 다른 user_id 요청
def test_refresh_token_fail_user_id(test_auth_client, login_data):
    response = test_auth_client.post(
        "/users/refresh",
        json={
            "user_id": (login_data["login_body"]["user_id"]+10),
            "refresh_token": login_data["login_body"]["refresh_token"]
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    rst_body = response.json()
    assert rst_body["detail"] == TokenAuth.INVALID_TOKEN


# 만료된 access token으로 요청
def test_expired_access_token(test_client, login_data):
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


# 잘못된 형태의 refresh token으로 요청
def test_refresh_token_wrong_type(test_auth_client, login_data):
    replace_token = login_data["login_body"]["refresh_token"].replace(".", "")
    response = test_auth_client.post(
        "/users/refresh",
        json={
            "user_id": (login_data["login_body"]["user_id"]+10),
            "refresh_token": replace_token
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    rst_body = response.json()
    assert rst_body["detail"] == TokenAuth.INVALID_TOKEN


# 만료된 access token으로 요청
def test_access_token_wrong_type(test_client, login_data):
    replace_token = login_data["login_body"]["access_token"].replace(".", "")
    response = test_client.post(
        "/users/refresh",
        json={
            "user_id": login_data["login_body"]["user_id"],
            "refresh_token": login_data["login_body"]["refresh_token"]
        },
        headers={
            "Authorization": f"Bearer {replace_token}"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    rst_body = response.json()
    assert rst_body["detail"] == TokenAuth.INVALID_TOKEN
