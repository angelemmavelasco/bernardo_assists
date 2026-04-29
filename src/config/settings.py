from dotenv import load_dotenv
load_dotenv()

import os
import pathlib

import psycopg2


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if not db_host or not db_port or not db_name or not db_user or not db_password:
    raise ValueError("One or more database environment variables are not set")

try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    print("Connection to the database was successful!")

    conn.close()

except Exception as e:
    print(f"An error occurred while connecting to the database: {e}")

print(DEEPSEEK_API_KEY)
