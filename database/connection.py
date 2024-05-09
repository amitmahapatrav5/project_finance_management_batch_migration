from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/expense"

logger = logging.getLogger(__name__)

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    logger.error(f"Error occurred while creating database engine: {e}")

try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Error occurred while creating session maker: {e}")

try:
    Base = declarative_base()
except Exception as e:
    logger.error(f"Error occurred while creating declarative base: {e}")