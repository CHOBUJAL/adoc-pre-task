from enum import StrEnum


class UserAuth(StrEnum):
    ALREADY_USER = "ALREADY_USER"
    NO_USER_FOUND = "NO USER FOUND"
    INVALID_PASSWORD = "INVALID PASSWORD"
