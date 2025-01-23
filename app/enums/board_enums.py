from enum import StrEnum


class BoardAction(StrEnum):
    CREATE_FAIL = "CREATE FAIL"
    NO_USER_FOUND = "NO USER FOUND"
    INVALID_PASSWORD = "INVALID PASSWORD"
