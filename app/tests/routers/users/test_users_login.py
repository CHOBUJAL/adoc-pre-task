from fastapi import status
from fastapi.testclient import TestClient

from app.enums.user_enums import UserAuth

# from app.schemas.user_schemas import loginRequest
# from app.enums.common_enums import ResultMessage
# from app.enums.user_enums import UserAuth



# 이메일 필드 누락 로그인 요청
def test_login_missing_email(test_client: TestClient):
    response = test_client.post(
        "/users/login",
        json={"password": "test"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "email"


# 패스워드 필드 누락 로그인 요청
def test_login_missing_password(test_client: TestClient):
    response = test_client.post(
        "/users/login",
        json={"email": "test@test.com"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "password"


# 이메일패스워드 필드 누락 로그인 요청
def test_login_missing_emailpassword(test_client: TestClient):
    response = test_client.post(
        "/users/login",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    rst_body = response.json()
    assert rst_body["detail"][0]["loc"][1] == "email"
    assert rst_body["detail"][1]["loc"][1] == "password"


# 존재하지않는 이메일로 로그인
def test_login_not_found_email(test_client: TestClient, mock_user):
    response = test_client.post(
        "/users/login",
        json={"email": f"mock{mock_user.email}", "password": "test"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    rst_body = response.json()
    assert rst_body["detail"] == UserAuth.NO_USER_FOUND


# 잘못된 암호 로그인
def test_login_fail_password(test_client: TestClient, mock_user):
    response = test_client.post(
        "/users/login",
        json={"email": mock_user.email, "password": "fail_password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    rst_body = response.json()
    assert rst_body["detail"] == UserAuth.INVALID_PASSWORD
