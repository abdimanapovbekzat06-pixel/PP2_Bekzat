import psycopg2
import os

def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        port=5432
    )