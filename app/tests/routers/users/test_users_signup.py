from fastapi import status
from fastapi.testclient import TestClient

from app.enums.common_enums import ResultMessage
from app.enums.user_enums import UserAuth
from app.schemas.user_schemas import SignUpRequest


# 이메일 필드 누락 회원가입 요청
def test_signup_missing_email(test_client: TestClient):
    response = test_client.post(
        "/users/signup",
        json={"password": "test"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "email"


# 패스워드 필드 누락 회원가입 요청
def test_signup_missing_password(test_client: TestClient):
    response = test_client.post(
        "/users/signup",
        json={"email": "test@test.com"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "password"


# 이메일패스워드 필드 누락 회원가입 요청
def test_signup_missing_emailpassword(test_client: TestClient):
    response = test_client.post(
        "/users/signup",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "email"
    assert rst_body["detail"][1]["loc"][1] == "password"


# 이미 존재하는 이메일 회원가입 요청
def test_signup_already_user(test_client: TestClient, mock_user):
    signup_body = SignUpRequest(
        email=mock_user.email,
        password="mock",
    )
    response = test_client.post(
        "/users/signup",
        json=signup_body.model_dump(mode="json")
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    rst_body = response.json()
    assert rst_body["detail"] == UserAuth.ALREADY_USER


# 중복회원 가입
def test_duplicate_signup(test_client: TestClient):
    signup_body = SignUpRequest(
        email="test@test.com",
        password="123"
    )
    response = test_client.post(
        "/users/signup",
        json=signup_body.model_dump(mode="json")
    )
    assert response.status_code == status.HTTP_200_OK
    rst_body = response.json()
    assert rst_body["message"] == ResultMessage.SUCCESS

    signup_body = SignUpRequest(
        email="test@test.com",
        password="123"
    )
    response = test_client.post(
        "/users/signup",
        json=signup_body.model_dump(mode="json")
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    rst_body = response.json()
    assert rst_body["detail"] == UserAuth.ALREADY_USER


# 정싱적인 회원가입 요청
def test_signup_success(test_client: TestClient):
    signup_body = SignUpRequest(
        email="test@test.com",
        password="123"
    )
    response = test_client.post(
        "/users/signup",
        json=signup_body.model_dump(mode="json")
    )
    assert response.status_code == status.HTTP_200_OK
    rst_body = response.json()
    assert rst_body["message"] == ResultMessage.SUCCESS
    assert rst_body["status_code"] == 200
