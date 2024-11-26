from pydantic import BaseModel, EmailStr, StringConstraints, field_validator
from typing import Optional,Annotated

class UserBase(BaseModel):
    email: EmailStr
    name: Annotated[str,StringConstraints(max_length=200)]
    address: str
    contact_number: Annotated[str,StringConstraints(max_length=15)]


class UserCreate(UserBase):
    password_hash: str
    is_nursery:bool = False

    @field_validator('password_hash')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserResponse(UserBase):
    user_id: int
    role: Optional[str] = "Customer"

    class Config:
        from_attributes = True