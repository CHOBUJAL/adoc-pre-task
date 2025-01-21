from pydantic import BaseModel, ConfigDict
from app.models.user_model import UserOrm

class SignUpRequest(BaseModel):
    email: str
    password: str


class SignUpResponse(BaseModel):
    message: str
    status_code: int

    
class SignupResult(BaseModel):
    message: str
    user: UserOrm | None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    
class LoginRequest(SignUpRequest):
    pass


class LoginResponse(SignUpResponse):
    pass


class LoginResult(SignupResult):
    pass