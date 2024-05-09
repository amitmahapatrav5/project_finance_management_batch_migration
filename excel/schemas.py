import logging
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from enum import Enum
from datetime import date as python_date_type
import re

logger = logging.getLogger(__name__)

class ProductOrService(str, Enum):
    Product = "Product"
    Service = "Service"

class NeedOrWant(str, Enum):
    Need = "Need"
    Want = "Want"

class Expense(BaseModel):
    date: python_date_type = Field(..., description="The date of the expense")
    category_name: str = Field(..., description="The name of the category")
    sub_category_name: str = Field(..., description="The name of the sub-category")
    product_or_service: ProductOrService = Field(..., description="The type of the product or service")
    product_or_service_name: str = Field(..., description="The name of the product or service")
    quantity_or_duration: str = Field(..., description="The quantity or duration of the product or service")
    price: float = Field(..., gt=0, description="The price of the product or service")
    need_or_want: NeedOrWant = Field(..., description="Whether the product or service is a need or a want")
    details: str = Field(..., description="The details of the expense")

    @field_validator('date')
    def date_cannot_be_in_future(cls, v, info: ValidationInfo):
        if v > python_date_type.today():
            logger.error(f'{v} cannot be a future date')
            return None
        return v

    @field_validator('category_name', 'sub_category_name', 'product_or_service_name')
    def elements_must_be_title_case(cls, v, info: ValidationInfo):
        if v != v.title():
            logger.error(f'{v} is not in Title Case')
            return None
        return v

    @field_validator('quantity_or_duration')
    def must_have_number_and_word(cls, v, info: ValidationInfo):
        pattern = re.compile(r'^\d+\s[A-Z][a-z]*(\s[A-Z][a-z]*)*$')
        if v == "Valid Data Missing" or pattern.match(v):
            return v
        else:
            logger.error(f'{v} does not start with a number followed by a word in Title Case or is not "Valid Data Missing"')
            return None

class Category(BaseModel):
    category_name: str = Field(..., description="The name of the category")

    @field_validator('category_name')
    def elements_must_be_title_case(cls, v, info: ValidationInfo):
        if v != v.title():
            logger.error(f'{v} is not in Title Case')
            return None
        return v

class SubCategory(BaseModel):
    category_name: str = Field(..., description="The name of the category")
    sub_category_name: str = Field(..., description="The name of the sub-category")

    @field_validator('category_name', 'sub_category_name')
    def elements_must_be_title_case(cls, v, info: ValidationInfo):
        if v != v.title():
            logger.error(f'{v} is not in Title Case')
            return None
        return v
