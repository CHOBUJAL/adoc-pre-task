from enum import StrEnum


class BoardAction(StrEnum):
    NO_POST_FOUND = "POST NOT FOUND"
    INVALID_ID_FORMAT = "INVALID ID FORMAT"
    POST_AUTH_FAIL = "POST AUTH FAIL"
    INVALID_PAGE = "INVALID PAGE"
    INVALID_PAGE_SIZE = "INVALID PAGE SIZE"



class BoardOrderType(StrEnum):
    CREATE_AT_LATEST = "-created_at"
    CREATE_AT_OLDEST = "created_at"
    TITLE_ASC = "title"
    TITLE_DESC = "-title"
