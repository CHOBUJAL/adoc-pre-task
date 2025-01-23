from enum import StrEnum


class UserAuth(StrEnum):
    ALREADY_USER = "ALREADY_USER"
    NO_USER_FOUND = "NO_USER_FOUND"
    INVALID_PASSWORD = "INVALID_PASSWORD"
