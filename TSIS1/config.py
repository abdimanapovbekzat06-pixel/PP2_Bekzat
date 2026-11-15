import os

DB_CONFIG = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": os.environ["DB_PASSWORD"],
    "port": 5432
}