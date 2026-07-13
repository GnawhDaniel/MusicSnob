from internal.utils.auth import hash_password
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

auth_conn = sqlite3.connect("./db/data.db", check_same_thread=False)
cursor = auth_conn.cursor()

user = os.environ["MUSICSNOB_USER"]
password = os.environ["MUSICSNOB_PASS"]

existing = cursor.execute(
    "SELECT 1 FROM users WHERE user_id = ?", (user,)
).fetchone()

if existing is None:
    hashed_password = hash_password(password)
    cursor.execute(
        "INSERT INTO users(user_id, hashed_pass) VALUES (?, ?)",
        (user, hashed_password),
    )
    auth_conn.commit()
    print(f"Seeded user '{user}'.")
else:
    print(f"User '{user}' already exists, skipping seed.")

auth_conn.close()