from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.user_model import UserOrm


class JwtPayLoad(BaseModel):
    user_id: int
    exp: datetime
    token_type: str

# 공통 응답 모델
class BaseResponse(BaseModel):
    message: str
    status_code: int | None = None

# 요청 및 결과 모델
class SignUpRequest(BaseModel):
    email: str
    password: str

class LoginRequest(SignUpRequest):
    pass

class RefreshRequest(BaseModel):
    user_id: int
    refresh_token: str

class LogoutRequest(BaseModel):
    user_id: int

# 결과 모델
class SignupResult(BaseModel):
    message: str
    user: UserOrm | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class LoginResult(BaseModel):
    message: str
    access_token: str | None = None
    refresh_token: str | None = None

class LogoutResult(BaseModel):
    message: str

# 응답 모델
class LoginResponse(BaseResponse):
    access_token: str | None = None
    refresh_token: str | None = None

class RefreshResponse(BaseResponse):
    access_token: str | None = None
