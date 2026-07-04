from hashlib import sha256
from datetime import datetime, timedelta

def get_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, hashed_pass FROM users WHERE user_id = ?", (username,))
    res = cursor.fetchone()
    return res

def insert_session(conn, session_id, username):
    cursor = conn.cursor()
    sha256_sessionid = sha256(session_id.encode('utf-8')).hexdigest()
    created_at = datetime.now()
    expiry = created_at + timedelta(days=1)

    cursor.execute("""
                   INSERT INTO auth_sessions(session_id, user_id, created_at, expiry)
                   VALUES (?, ?, ?, ?)
                   """, (sha256_sessionid, username, created_at, expiry,))
    conn.commit()

def remove_session_by_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM auth_sessions WHERE user_id = ?", (username,))
    conn.commit()

def is_session(conn, session_id) -> bool:
    cursor = conn.cursor()
    session_id = sha256(session_id.encode('utf-8')).hexdigest()
    res = cursor.execute("SELECT * FROM auth_sessions WHERE session_id = ?", (session_id,))
    if res.fetchone():
        return True
    return False
