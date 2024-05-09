from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from .connection import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255), unique=True, nullable=False)

    sub_categories = relationship("SubCategory", back_populates="category")
    expenses = relationship("Expense", back_populates="category")


class SubCategory(Base):
    __tablename__ = 'sub_category'

    id = Column(Integer, primary_key=True, index=True)
    sub_category_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship("Category", back_populates="sub_categories")
    expenses = relationship("Expense", back_populates="sub_category")

    __table_args__ = (UniqueConstraint('sub_category_name', 'category_id', name='_subcategory_category_uc'),)


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='SET NULL'))
    sub_category_id = Column(Integer, ForeignKey('sub_category.id', ondelete='SET NULL'))
    product_or_service = Column(String(50), nullable=False)
    product_or_service_name = Column(String(255), nullable=False)
    quantity_or_duration = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    need_or_want = Column(String(50), nullable=False)
    details = Column(Text)
    
    category = relationship("Category", back_populates="expenses")
    sub_category = relationship("SubCategory", back_populates="expenses")