from enum import StrEnum


class TokenType(StrEnum):

    ACCESS = "ACCESS"
    REFRESH = "REFRESH"

class TokenAuth(StrEnum):

    TOKEN_EXPIRED = "TOKEN EXPIRED"
    INVALID_TOKEN = "INVALID TOKEN"
    INVALID_AUTH_SCHEME = "INVALID AUTH SCHEME"
