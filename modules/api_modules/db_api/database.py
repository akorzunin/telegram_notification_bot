from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

import os

PWD = os.path.abspath(os.getcwd())
import sys
sys.path.insert(1, PWD)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{PWD}/database/sql_app.db"
logging.info(f'Database connect: {SQLALCHEMY_DATABASE_URL}')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
