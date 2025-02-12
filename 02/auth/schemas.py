from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str  # ✅ Expecting a string, but DB gives UUID

    @classmethod
    def from_orm(cls, obj):
        return cls(id=str(obj.id), email=obj.email)

    class Config:
        from_attributes = True  # Allow automatic conversion
