from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from . import models, schemas

import logging
import inspect


logger = logging.getLogger(__name__)


def insert_category(db: Session, category: schemas.CategoryCreateRequest):
    db_category = models.Category(**category.model_dump())
    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Probably Unique Constraint is violated for Category {category.category_name}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error while inserting category: {e}")
    except Exception as e:
        db.rollback()
        logger.exception(f"Unexpected error occurred in {inspect.currentframe().f_code.co_name} function.")


def insert_sub_category(db: Session, sub_category: schemas.SubCategoryCreateRequest):
    try:
        category_name = sub_category.category_name
        category = get_category_by_name(db, category_name)
        if category:            
            sub_category_data = sub_category.model_dump()
            sub_category_data["category_id"] = category.id
            del sub_category_data['category_name']
            db_sub_category = models.SubCategory(**sub_category_data)
            try:
                db.add(db_sub_category)
                db.commit()
                db.refresh(db_sub_category)
                return db_sub_category
            except IntegrityError as e:
                db.rollback()
                logger.error(f"Probably Combined Unique Constraint is violated for Category {sub_category.category_name} and Sub Category: {sub_category.sub_category_name}")
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error while inserting sub-category {sub_category.sub_category_name}")
                raise
            except Exception as e:
                db.rollback()
                logger.exception(f"Unexpected error occurred in {inspect.currentframe().f_code.co_name} function.")
        else:
            logger.warning(f"Category '{category_name}' does not exist.")
            return None
    except Exception as e:
        logger.exception(f"Unexpected error occurred in {inspect.currentframe().f_code.co_name} function.")
        raise


def insert_expense(db: Session, expense: schemas.ExpenseCreateRequest):
    category_name = expense.category_name
    sub_category_name = expense.sub_category_name
    category = get_category_by_name(db, category_name)
    sub_category = get_sub_category_by_name(db, sub_category_name, category_name)
    if(category and sub_category):
        if(category.id == sub_category.category_id):
            expense_data = expense.model_dump()
            expense_data['category_id'] = category.id
            expense_data['sub_category_id'] = sub_category.id
            del expense_data['category_name']
            del expense_data['sub_category_name']
            db_expense = models.Expense(**expense_data)
            try:
                db.add(db_expense)
                db.commit()
                db.refresh(db_expense)
                return db_expense
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error while inserting sub-category {sub_category.sub_category_name}")
            except Exception as e:
                db.rollback()
                logger.exception(f"Unexpected error occurred in {inspect.currentframe().f_code.co_name} function.")                
        else:
            logger.error(f"Sub Category '{sub_category_name}' does not belong to Category '{category_name}'.")
    else:
        if(category and not sub_category):
            logger.error(f"Sub Category '{sub_category_name}' does not exist.")
        elif(sub_category and not category):
            logger.error(f"Category '{category_name}' does not exist.")
        else:
            logger.error(f"Category '{category_name}' and Sub Category '{sub_category_name}' does not exist.")


def get_sub_category_by_name(db: Session, sub_category_name: str, category_name: str):
    try:
        return db.query(models.SubCategory).join(models.Category).filter(
            models.Category.category_name == category_name,
            models.SubCategory.sub_category_name == sub_category_name
        ).first()
    except Exception as e:
        logger.exception(f"Unexpected error occurred in {inspect.currentframe().f_code.co_name} function.")


def get_category_by_name(db: Session, category_name: str):
    try:
        return db.query(models.Category).filter(models.Category.category_name == category_name).first()
    except Exception as e:
        logger.exception(f"Unexpected error occurred in {inspect.currentframe().f_code.co_name} function.")