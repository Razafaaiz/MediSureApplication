import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "database.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def create_user_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = get_db()
    cursor = conn.cursor()
    hashed = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[3], password):
        return user
    return None

def update_password(email, new_password):
    conn = get_db()
    cursor = conn.cursor()
    hashed = generate_password_hash(new_password)
    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (hashed, email)
    )
    conn.commit()
    conn.close()

def email_exists(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    exists = cursor.fetchone()
    conn.close()
    return exists is not None

def generate_otp():
    return str(random.randint(100000, 999999))
