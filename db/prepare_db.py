import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CREDENTIALS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def create_db():
    with open("db/prepare_db.sql") as f:
        create_db_query = f.read()

    connection = psycopg2.connect(**DB_CREDENTIALS)
    cursor = connection.cursor()

    cursor.execute(create_db_query)
    connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_db()
