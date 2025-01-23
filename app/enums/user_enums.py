from enum import StrEnum


class UserAuth(StrEnum):
    ALREADY_USER = "ALREADY USER"
    NO_USER_FOUND = "NO USER FOUND"
    INVALID_PASSWORD = "INVALID PASSWORD"
