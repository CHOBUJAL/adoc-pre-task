
from fastapi import status
from mongoengine.context_managers import switch_db

from app.core.settings import settings
from app.enums.board_enums import BoardAction, BoardOrderType
from app.enums.common_enums import ResultMessage
from app.models.board_model import Board

# 테스트 데이터로 생성되는 모든 게시물의 제목 리스트
all_titles = []
for i in range(3):
    for j in range(i+10):
        all_titles.append(f"mock_{i+1}_{j}")


# 잘못된 페이지 번호 요청
def test_board_list_wrong_page_num(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get(
            "/boards",
            params={"page": 0}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        rst_body = response.json()
        assert rst_body["detail"] == BoardAction.INVALID_PAGE


# 너무 큰 페이지 번호 요청
def test_board_list_out_range_page_num(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get(
            "/boards",
            params={"page": 100}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["page"] == 100
        assert rst_body["page_size"] == 10
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert rst_body["post_list"] == []
        assert rst_body["total_count"] == 33
        assert rst_body["status_code"] == 200


# 잘못된 페이지 사이즈 요청
def test_board_list_wrong_page_size(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get(
            "/boards",
            params={"page_size": 0}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        rst_body = response.json()
        assert rst_body["detail"] == BoardAction.INVALID_PAGE_SIZE
        response = test_client.get(
            "/boards",
            params={"page_size": 100}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        rst_body = response.json()
        assert rst_body["detail"] == BoardAction.INVALID_PAGE_SIZE


# 정상적인 페이지 요청
def test_board_list_success_pagination(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME) as TestBoard:
        total_board = TestBoard.objects.count()
        page_size = 7
        page_num = 0
        for i in range(total_board // page_size):
            page_num = i+1
            response = test_client.get(
                "/boards",
                params={"page": page_num, "page_size": page_size}
            )
            assert response.status_code == status.HTTP_200_OK
            rst_body = response.json()
            assert rst_body["page"] == page_num # default value return
            assert rst_body["page_size"] == page_size # default value return
            assert rst_body["message"] == ResultMessage.SUCCESS
            assert len(rst_body["post_list"]) == page_size
            assert rst_body["total_count"] == total_board
            assert rst_body["status_code"] == 200
        # 33개의 데이터를 7개의 사이즈로 요청하면 마지막 페이지의 데이터는 2개가 되어야 한다.
        page_num += 1
        response = test_client.get(
            "/boards",
            params={"page": page_num, "page_size": page_size}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["page"] == page_num # default value return
        assert rst_body["page_size"] == page_size # default value return
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert len(rst_body["post_list"]) == 5
        assert rst_body["total_count"] == total_board
        assert rst_body["status_code"] == 200


# 존재하지 않은 유저 아이디 요청
def test_board_list_user_not_board(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get(
            "/boards",
            params={"user_id": 0}
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["page"] == 1 # default value return
        assert rst_body["page_size"] == 10 # default value return
        assert rst_body["message"] == ResultMessage.SUCCESS
        assert len(rst_body["post_list"]) == 0
        assert rst_body["total_count"] == 0
        assert rst_body["status_code"] == 200


# 정상적인 user_id filter 요청
def test_board_list_user_id_success(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        for i in range(3):
            response = test_client.get(
                "/boards",
                params={"user_id": i+1}
            )
            assert response.status_code == status.HTTP_200_OK
            rst_body = response.json()
            assert rst_body["page"] == 1 # default value return
            assert rst_body["page_size"] == 10 # default value return
            assert rst_body["message"] == ResultMessage.SUCCESS
            # page_size는 모두 10으로 요청하기 때문에 리턴되는 게시물의 수는 10개로 고정이다.
            assert len(rst_body["post_list"]) == 10
            assert rst_body["total_count"] == i+10
            assert rst_body["status_code"] == 200


# title 미전달
def test_board_list_not_title_field(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get("/boards")
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["page"] == 1 # default value return
        assert rst_body["page_size"] == 10 # default value return
        assert rst_body["message"] == ResultMessage.SUCCESS
        # page_size는 모두 10으로 요청하기 때문에 리턴되는 게시물의 수는 10개로 고정이다.
        assert len(rst_body["post_list"]) == 10
        assert rst_body["total_count"] == len(all_titles)
        assert rst_body["status_code"] == 200

"""
mock_1_1 mock_1_1 mock_1_2 mock_1_3 mock_1_4 mock_1_5 mock_1_6 mock_1_7 mock_1_8 mock_1_9
mock_2_0 mock_2_1 mock_2_2 mock_2_3 mock_2_4 mock_2_5 mock_2_6 mock_2_7 mock_2_8 mock_2_9 mock_2_10
mock_3_0 mock_3_1 mock_3_2 mock_3_3 mock_3_4 mock_3_5 mock_3_6 mock_3_7 mock_3_8 mock_3_9 mock_3_10 mock_3_11
"""
# title 전달 요청 (기본적으로 대소문자는 판단하지 않는다)
def test_board_list_title_field_success(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        # mock_2_10, mock_3_10
        response = test_client.get("/boards", params={"page_size": 50, "title": "10"})
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["total_count"] == 2
        assert rst_body["status_code"] == 200
        return_post_titles = [post["title"] for post in rst_body["post_list"]]
        for title in ["mock_2_10", "mock_3_10"]:
            assert title in return_post_titles

        # all : 33
        response = test_client.get("/boards", params={"page_size": 50, "title": "MoCk"})
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["total_count"] == 33
        assert rst_body["status_code"] == 200

        # mock_2_0 mock_2_1 mock_2_2 mock_2_3 mock_2_4 mock_2_5 mock_2_6 mock_2_7 mock_2_8 mock_2_9 mock_2_10
        response = test_client.get("/boards", params={"page_size": 50, "title": "MoCk_2"})
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["total_count"] == 11
        assert rst_body["status_code"] == 200
        return_post_titles = [post["title"] for post in rst_body["post_list"]]
        for title in ["mock_2_0", "mock_2_1", "mock_2_2", "mock_2_3", "mock_2_4", "mock_2_5",
                       "mock_2_6", "mock_2_7", "mock_2_8", "mock_2_9", "mock_2_10"]:
            assert title in return_post_titles


# order type을 보내지않을떄 기본값인 생성날짜 내림차순 테스트
def test_board_list_no_order_type(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get("/boards", params={"page_size": 50})
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        return_post_create_at = [post["created_at"] for post in rst_body["post_list"]]
        for current, next_create_at in zip(return_post_create_at, return_post_create_at[1:]):
            assert current > next_create_at


# 생성날짜 오름차순 요청 테스트
def test_board_list_asc_created_at_type(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get("/boards", params={"page_size": 50, "order_type": BoardOrderType.CREATE_AT_OLDEST})
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        return_post_create_at = [post["created_at"] for post in rst_body["post_list"]]
        for current, next_create_at in zip(return_post_create_at, return_post_create_at[1:]):
            assert current < next_create_at


# 제목 내림차순 요청 테스트
def test_board_list_desc_title_type(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get("/boards", params={"page_size": 50, "order_type": BoardOrderType.TITLE_DESC})
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        return_post_title = [post["title"] for post in rst_body["post_list"]]
        for current, next_title in zip(return_post_title, return_post_title[1:]):
            assert current > next_title


# 제목 오름차순 요청 테스트
def test_board_list_asc_title_type(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get("/boards", params={"page_size": 50, "order_type": BoardOrderType.TITLE_ASC})
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        return_post_title = [post["title"] for post in rst_body["post_list"]]
        for current, next_title in zip(return_post_title, return_post_title[1:]):
            assert current < next_title


# 복합 쿼리 파라미터 요청 테스트
def test_board_list_complex_params(test_client, mock_many_boards):
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        # mock_3_1 mock_3_10, mock_3_11 page_size 요청으로 인해
        response = test_client.get(
            "/boards",
            params={
                "page": 1,
                "page_size": 10,
                "order_type": BoardOrderType.TITLE_DESC,
                "user_id": 3,
                "title": "3_1"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        return_post = [post for post in rst_body["post_list"]]
        for current, next_title in zip(return_post, return_post[1:]):
            assert current["title"] > next_title["title"]
        return_post_titles = [post["title"] for post in rst_body["post_list"]]
        for title in ["mock_3_1", "mock_3_10", "mock_3_11"]:
            assert title in return_post_titles

        # mock_1_0 mock_1_1 mock_1_2 mock_1_3 mock_1_4 mock_1_5 mock_1_6 mock_1_7 mock_1_8 mock_1_9
        # mock_2_1 mock_2_10 mock_3_1 mock_3_10 mock_3_11
        response = test_client.get(
            "/boards",
            params={
                "page": 1,
                "page_size": 13,
                "order_type": BoardOrderType.CREATE_AT_OLDEST,
                "title": "_1"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        return_post = [post for post in rst_body["post_list"]]
        for current, next_title in zip(return_post, return_post[1:]):
            assert current["created_at"] < next_title["created_at"]
        return_post_titles = [post["title"] for post in rst_body["post_list"]]
        for title in [
            "mock_1_0", "mock_1_1", "mock_1_2", "mock_1_3", "mock_1_4", "mock_1_5", "mock_1_6",
            "mock_1_7", "mock_1_8", "mock_1_9", "mock_2_1", "mock_2_10", "mock_3_1"
            ]:
            assert title in return_post_titles


# 복합 쿼리 파라미터 요청 테스트
def test_board_list_complex_params_empty_return(test_client, mock_many_boards):
    # (mock_3_1) mock_3_10, mock_3_11 page_size 요청으로 인해
    with switch_db(Board, settings.TEST_MONGO_DB_NAME):
        response = test_client.get(
            "/boards",
            params={
                "page": 1,
                "page_size": 10,
                "order_type": BoardOrderType.TITLE_DESC,
                "user_id": 4,
                "title": "mock"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["total_count"] == 0

        response = test_client.get(
            "/boards",
            params={
                "page": 1,
                "page_size": 10,
                "order_type": BoardOrderType.TITLE_DESC,
                "user_id": 1,
                "title": "2_"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        rst_body = response.json()
        assert rst_body["total_count"] == 0
