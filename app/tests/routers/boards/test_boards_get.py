from datetime import datetime

from fastapi import status
from mongoengine.context_managers import switch_db

from app.core.settings import settings
from app.enums.board_enums import BoardAction
from app.enums.common_enums import ResultMessage
from app.models.board_model import Board


# 잘못된 형식의 post_id 요청
def test_board_get_wrong_type(test_client, mock_board):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        for board in TestBoard.objects:
            sample_id = f"{board.id} wrong type"
            response = test_client.get(f"/boards/{sample_id}")
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            rst_body = response.json()
            assert rst_body["detail"] == BoardAction.INVALID_ID_FORMAT


# 존재하지않은 post_id 요청
def test_board_get_not_exist(test_client, test_mongo_connection):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        sample_id = "6796044905875f110a8c9fdd"
        response = test_client.get(f"/boards/{sample_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        rst_body = response.json()
        assert rst_body["detail"] == BoardAction.NO_POST_FOUND


# 존재하는 post_id 요청
def test_board_get_success(test_client, mock_board):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        for board in TestBoard.objects:
            sample_id = f"{board.id}"
            response = test_client.get(f"/boards/{sample_id}")
            assert response.status_code == status.HTTP_200_OK
            rst_body = response.json()
            assert rst_body["message"] == ResultMessage.SUCCESS
            assert rst_body["status_code"] == 200
            assert rst_body["post"]["post_id"] == str(board.id)
            assert rst_body["post"]["author_id"] == board.author_id
            assert rst_body["post"]["title"] == board.title
            assert rst_body["post"]["content"] == board.content
            assert datetime.fromisoformat(rst_body["post"]["created_at"]) == board.created_at
