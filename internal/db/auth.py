def get_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, hashed_pass FROM user")
    return cursor.fetchall()
