from .database.connection import SessionLocal
from .database.queries import insert_category, insert_sub_category, insert_expense
from .excel.utils import get_category_sheet_data, get_sub_category_sheet_data, get_expense_sheet_data

def insert_categories():
    db = SessionLocal()
    categories = get_category_sheet_data()
    for category in categories:
        insert_category(db, category)
    db.close()


def insert_sub_categories():
    db = SessionLocal()
    sub_categories = get_sub_category_sheet_data()
    for sub_category in sub_categories:
        insert_sub_category(db, sub_category)    
    db.close()


def insert_expenses():
    db = SessionLocal()
    expenses = get_expense_sheet_data()
    for expense in expenses:
        insert_expense(db, expense)
    db.close()


def main():
    insert_categories()
    insert_sub_categories()
    insert_expenses()