from .connection import engine
from . import models
import logging
import traceback

def create_database_tables():
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        logging.error("An error occurred while creating database tables:")
        logging.error(traceback.format_exc())
        raise e

create_database_tables()