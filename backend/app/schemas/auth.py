from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    email: str = Field(..., description="Accepts email, username, or register number")
    password: str

class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: str
    username: str
    role: str
    student_id: Optional[int] = None
    studentId: Optional[int] = None
    register_no: Optional[str] = None
    registerNo: Optional[str] = None
    profile_image: Optional[str] = None
    profileImage: Optional[str] = None

    class Config:
        from_attributes = True

# UserBase is kept as alias/reference for compatibility with other routers
class UserBase(UserAuthResponse):
    pass

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserAuthResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str
