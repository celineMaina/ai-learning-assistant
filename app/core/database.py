import os
from dotenv import load_dotenv

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_URL = os.getenv('DB_URL')

engine = create_engine(
    DB_URL,
    connect_args=("sslmode":"require"),
    echo=True,
    pool_pre_ping=True
)

class Base(DeclarativeBase):
    pass

def create_tables():
    from app.core import schema
    
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("All tables created successfully.")