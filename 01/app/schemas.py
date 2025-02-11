from pydantic import BaseModel, validator
from typing import List


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class ProductInResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True


class CategoryInput(BaseModel):
    name: str
    @validator('name')
    def name_must_be_a_string(cls, name):
        if not name: 
            raise ValueError('Name cannot be empty')
        return name
    class Config:
        orm_mode = True


class CategoryView(CategoryInput):
    id: int
    slug: str

    class Config:
        orm_mode = True