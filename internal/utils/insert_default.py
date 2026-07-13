from internal.utils.auth import hash_password, verify_hash
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

auth_conn = sqlite3.connect("./db/data2.db", check_same_thread=False)
cursor = auth_conn.cursor()

user = os.environ["MUSICSNOB_USER"]
password = os.environ["MUSICSNOB_PASS"]
hashed_password = hash_password(password)

cursor.execute("INSERT INTO users(user_id, hashed_pass) VALUES (?, ?)", (user, hashed_password))

res = cursor.execute("SELECT hashed_pass FROM users WHERE user_id = ?", (user,)).fetchone()[0]

auth_conn.commit()
