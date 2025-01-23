from enum import StrEnum


class BoardAction(StrEnum):
    NO_POST_FOUND = "POST NOT FOUND"
    INVALID_ID_FORMAT = "INVALID ID FORMAT"
    POST_AUTH_FAIL = "POST AUTH FAIL"
