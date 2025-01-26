from datetime import datetime, timezone

from fastapi import status

from app.core.security import (
    decode_jwt,
)
from app.enums.common_enums import ResultMessage
from app.enums.security_enums import TokenType
from app.enums.user_enums import UserAuth


# 이메일 필드 누락 로그인 요청
def test_login_missing_email(test_client):
    response = test_client.post(
        "/users/login",
        json={"password": "test"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "email"


# 패스워드 필드 누락 로그인 요청
def test_login_missing_password(test_client):
    response = test_client.post(
        "/users/login",
        json={"email": "test@test.com"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "password"


# 이메일패스워드 필드 누락 로그인 요청
def test_login_missing_emailpassword(test_client):
    response = test_client.post(
        "/users/login",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "email"
    assert rst_body["detail"][1]["loc"][1] == "password"


# 존재하지않는 이메일로 로그인
def test_login_not_found_email(test_client, mock_user):
    response = test_client.post(
        "/users/login",
        json={"email": "not_found_email", "password": "test"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    rst_body = response.json()
    assert rst_body["detail"] == UserAuth.NO_USER_FOUND


# 잘못된 암호 로그인
def test_login_fail_password(test_client, mock_user):
    response = test_client.post(
        "/users/login",
        json={"email": mock_user.email, "password": "fail_password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    rst_body = response.json()
    assert rst_body["detail"] == UserAuth.INVALID_PASSWORD


# 정상적인 로그인 성공
def test_login_success(test_client, mock_user):
    response = test_client.post(
        "/users/login",
        json={"email": mock_user.email, "password": "mock_password"}
    )
    assert response.status_code == status.HTTP_200_OK
    rst_body = response.json()
    assert rst_body["message"] == ResultMessage.SUCCESS
    assert rst_body["status_code"] == 200
    assert rst_body["user_id"] == mock_user.id
    assert isinstance(str(rst_body["access_token"]), str)
    assert isinstance(str(rst_body["refresh_token"]), str)


# 로그인 후 리턴받은 토큰 검증
def test_login_token_check(login_data):
    now = datetime.now(tz=timezone.utc)
    login_body = login_data["login_body"]
    mock_user = login_data["mock_user"]

    access_payload = decode_jwt(jwt_token=login_body["access_token"])
    assert mock_user.id == access_payload["user_id"]
    assert TokenType.ACCESS == access_payload["token_type"]
    assert now.timestamp() < access_payload["exp"]

    refresh_payload = decode_jwt(jwt_token=login_body["refresh_token"])
    assert mock_user.id == refresh_payload["user_id"]
    assert TokenType.REFRESH == refresh_payload["token_type"]
    assert now.timestamp() < refresh_payload["exp"]

    assert access_payload["exp"] < refresh_payload["exp"]
