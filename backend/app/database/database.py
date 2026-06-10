import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ["DATABASE_HOST"]
DB_USER = os.environ["DATABASE_USER"]
DB_PASSWORD = os.environ["DATABASE_PASSWORD"]
DB_NAME = os.environ["DATABASE_NAME"]

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )