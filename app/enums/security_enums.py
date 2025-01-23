from enum import StrEnum


class TokenType(StrEnum):

    ACCESS = "ACCESS"
    REFRESH = "REFRESH"

class TokenAuth(StrEnum):

    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INVALID_TOKEN = "INVALID_TOKEN"
