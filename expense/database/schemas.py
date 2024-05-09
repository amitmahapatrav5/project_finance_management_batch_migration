from pydantic import BaseModel
from typing import Optional
from datetime import date as date_type


class CategoryBase(BaseModel):
    category_name: str

class CategoryCreateRequest(CategoryBase):
    pass


class SubCategoryBase(BaseModel):
    sub_category_name: str

class SubCategoryCreateRequest(SubCategoryBase):
    category_name: str


class ExpenseBase(BaseModel):
    date: date_type
    product_or_service: str
    product_or_service_name: str
    quantity_or_duration: str
    price: float
    need_or_want: str
    details: Optional[str]

class ExpenseCreateRequest(ExpenseBase):
    category_name: str
    sub_category_name: str