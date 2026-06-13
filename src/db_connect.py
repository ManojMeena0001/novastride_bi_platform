from sqlalchemy import create_engine
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
def get_db_connection():
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    DATABASE = os.getenv("DB_NAME")

    connection_string=f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    try:
        engine=create_engine(connection_string)
        with engine.connect() as connection:
            pass
        print("⚡ Success: Python connected to NovaStride Database smoothly!")
        return engine
    except Exception as e:
        print(f'Error: Could not connect to database .Details : {e}')
        return None
if __name__=="__main__":
    get_db_connection()

