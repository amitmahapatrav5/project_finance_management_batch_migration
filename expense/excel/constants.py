from enum import Enum
from pathlib import Path

class Constants(Enum):
    FILE_PATH = "./data/expense.xlsx"
    WORKBOOK_NAME = "expense"
    EXPENSE_SHEET_NAME = "expense"
    CATEGORY_SHEET_NAME = "category"
    SUB_CATEGORY_SHEET_NAME = "sub_category"