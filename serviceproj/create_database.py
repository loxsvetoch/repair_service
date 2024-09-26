#serviceproj/create_database.py
from serviceproj import app
import psycopg2
import serviceproj.models
from serviceproj import db


def update_database():
    db_name = "servicebase"
    conn = psycopg2.connect(dbname="postgres", user="admin_user", password="admin_password", host="localhost")
    conn.autocommit = True
    cursor = conn.cursor()
    
    cursor.execute(("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), [db_name])
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(("CREATE DATABASE {}").format((db_name)))
        print(f"База данных '{db_name}' создана.")
    else:
        print(f"База данных '{db_name}' уже существует.")
    
    cursor.close()
    conn.close()

with app.app_context():
    update_database()  # Проверка базы данных
    db.create_all()