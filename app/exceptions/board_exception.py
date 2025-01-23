from fastapi import HTTPException, status

from app.enums.board_enums import BoardAction


def board_exception_handler(detail: str = None):

    if not detail:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

    if detail == BoardAction.NO_POST_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
    elif detail == BoardAction.INVALID_ID_FORMAT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
    elif detail == BoardAction.POST_AUTH_FAIL:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
