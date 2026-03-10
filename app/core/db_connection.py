import os
from dotenv import load_dotenv
import asyncpg


load_dotenv('.env.app')

DB_URL = os.getenv('DB_URL')

if not DB_URL:
    raise ValueError("DB_URL environment variable not set")

async def connect():
    conn = await asyncpg.connect(DB_URL)
    print('Database successfully connected!')

    return conn

    

