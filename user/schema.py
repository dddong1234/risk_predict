from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserSignUpRequest(BaseModel):
    email: EmailStr = Field(..., examples=["alex@example.com"])
    password: str = Field(..., min_length=4, examples=["password123"])

class UserLogInRequest(BaseModel):
    email: EmailStr = Field(..., examples=["alex@example.com"])
    password: str = Field(..., min_length=4, examples=["password123"])


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
