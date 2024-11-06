from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

URL_DATABASE = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@localhost:5432/ICB'

engine = create_engine(URL_DATABASE)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
