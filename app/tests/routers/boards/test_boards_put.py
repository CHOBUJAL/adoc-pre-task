from datetime import timedelta

from fastapi import status
from freezegun import freeze_time
from mongoengine.context_managers import switch_db

from app.core.settings import settings
from app.core.utils import get_now_utc
from app.enums.board_enums import BoardAction
from app.enums.common_enums import ResultMessage
from app.enums.security_enums import TokenAuth
from app.models.board_model import Board


# 잘못된 형식의 post_id 요청
def test_board_put_wrong_type(test_auth_client, mock_board):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        for board in TestBoard.objects:
            sample_id = f"{board.id} wrong type"
            response = test_auth_client.put(f"/boards/{sample_id}")
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            rst_body = response.json()
            assert rst_body["detail"] == BoardAction.INVALID_ID_FORMAT


# 존재하지않은 post_id 요청
def test_board_put_not_exist(test_auth_client, test_mongo_connection):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        sample_id = "9999999905875f110a8c9fdd"
        response = test_auth_client.put(
            f"/boards/{sample_id}",
            json={"title": "string", "content": "string"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        rst_body = response.json()
        assert rst_body["detail"] == BoardAction.NO_POST_FOUND


# 만료된 access token으로 요청
def test_board_put_expired_token(test_client, login_data):
    # freeze_time으로 하여 강제로 시간을 앞당긴다
    with freeze_time(get_now_utc() + timedelta(hours=1)):
        response = test_client.put(
            "/boards/6796044905875f110a8c9fdd",
            headers={
                "Authorization": f"Bearer {login_data['login_body']['access_token']}"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        rst_body = response.json()
        assert rst_body["detail"] == TokenAuth.ACCESS_TOKEN_EXPIRED


# 권한없는 게시글 수정 요청
def test_board_put_other_user_post(test_auth_client, mock_board):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        sample_post_id = TestBoard.objects().filter(author_id=2)[0].id
        response = test_auth_client.put(
            f"/boards/{sample_post_id}",
            json={"title": "string", "content": "string"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        rst_body = response.json()
        assert rst_body["detail"] == BoardAction.POST_AUTH_FAIL


# 수정내용 변경 없이 정상 요청
def test_board_put_post_no_param_success(test_auth_client, mock_board):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        sample_post = TestBoard.objects().filter(author_id=1)[0]
        sample_post_id = sample_post.id
        response = test_auth_client.put(
            f"/boards/{sample_post_id}",
            json={}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert rst_body["post_id"] == str(sample_post_id)
        assert rst_body["status_code"] == 200

        response = test_auth_client.get(f"/boards/{sample_post_id}")
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["post"]["post_id"] == str(sample_post_id)
        assert rst_body["post"]["title"] == sample_post.title
        assert rst_body["post"]["content"] == sample_post.content


# 하나의 파라미터씩 수정 변경 요청
def test_board_put_post_one_param_success(test_auth_client, mock_board):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        sample_post = TestBoard.objects().filter(author_id=1)[0]
        sample_post_id = sample_post.id
        response = test_auth_client.put(
            f"/boards/{sample_post_id}",
            json={"title": "change_title"}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert rst_body["post_id"] == str(sample_post_id)
        assert rst_body["status_code"] == 200

        response = test_auth_client.get(f"/boards/{sample_post_id}")
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["post"]["post_id"] == str(sample_post_id)
        assert rst_body["post"]["title"] == "change_title"
        assert rst_body["post"]["content"] == sample_post.content

        response = test_auth_client.put(
            f"/boards/{sample_post_id}",
            json={"content": "content change"}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert rst_body["post_id"] == str(sample_post_id)
        assert rst_body["status_code"] == 200

        response = test_auth_client.get(f"/boards/{sample_post_id}")
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["post"]["post_id"] == str(sample_post_id)
        assert rst_body["post"]["title"] == "change_title"
        assert rst_body["post"]["content"] == "content change"


# 모든 필드(제목, 내용) 변경 정상 요청
def test_board_put_post_success(test_auth_client, mock_board):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        sample_post = TestBoard.objects().filter(author_id=1)[0]
        sample_post_id = sample_post.id
        response = test_auth_client.put(
            f"/boards/{sample_post_id}",
            json={"title": "one", "content": "two content"}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert rst_body["post_id"] == str(sample_post_id)
        assert rst_body["status_code"] == 200

        response = test_auth_client.get(f"/boards/{sample_post_id}")
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["post"]["post_id"] == str(sample_post_id)
        assert rst_body["post"]["title"] == "one"
        assert rst_body["post"]["content"] == "two content"
