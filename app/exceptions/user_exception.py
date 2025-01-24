from fastapi import HTTPException, status

from app.enums.security_enums import TokenAuth
from app.enums.user_enums import UserAuth


def user_exception_handler(detail: str = None):

    if not detail:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

    if detail == UserAuth.ALREADY_USER:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
    elif detail == UserAuth.NO_USER_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
    elif (
        detail == UserAuth.INVALID_PASSWORD
        or TokenAuth.INVALID_TOKEN
        or TokenAuth.ACCESS_TOKEN_EXPIRED
        or TokenAuth.REFRESH_TOKEN_EXPIRED):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
