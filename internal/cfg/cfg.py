from dotenv import load_dotenv
import os
import sqlite3

youtube_api_url = "https://www.googleapis.com/youtube/v3"
# youtube_api_key = os.getenv("YOUTUBE_API_KEY")
database_file = "./db/data.db"
database_schema_file = "db/schema.sql"

auth_db_file = "./db/auth.db"
auth_schema_file = "db/auth_schema.sql"

YOUTUBE = dict()
cfg = dict()

def load_config():
    global YOUTUBE, cfg
    load_dotenv()
    
    # If database files don't exist, create them
    if not os.path.exists(database_file):
        open(database_file, "x").close()
    if not os.path.exists(auth_db_file):
        open(auth_db_file, "x").close()
    
    YOUTUBE["API_URL"] = youtube_api_url
    YOUTUBE["API_KEY"] = os.getenv("YOUTUBE_API_KEY")
    cfg["YOUTUBE"] = YOUTUBE

    data_conn = sqlite3.connect(database_file, check_same_thread=False)
    data_conn.execute("PRAGMA foreign_keys = ON")
    cfg["DB_CONN"] = data_conn

    auth_conn = sqlite3.connect(auth_db_file, check_same_thread=False)
    auth_conn.execute("PRAGMA foreign_keys = ON")
    cfg["AUTH_CONN"] = auth_conn

    
    with open(database_schema_file, "r") as f:
        schema = f.read()
        cursor = cfg["DB_CONN"].cursor()
        cursor.executescript(schema)

    with open(auth_schema_file, "r") as f:
        schema = f.read()
        cursor = cfg["AUTH_CONN"].cursor()
        cursor.executescript(schema)
    
    return cfg

