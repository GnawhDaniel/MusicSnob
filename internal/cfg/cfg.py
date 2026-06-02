from dotenv import load_dotenv
import os
import sqlite3

youtube_api_url = "https://www.googleapis.com/youtube/v3"
# youtube_api_key = os.getenv("YOUTUBE_API_KEY")
database_file = "db/data.db"
database_schema_file = "db/schema.sql"
YOUTUBE = dict()
cfg = dict()

def load_config():
    global YOUTUBE, cfg
    load_dotenv()
    
    # If database file doesn't exist, create it
    if not os.path.exists(database_file):
        open(database_file, "w").close()
    
    YOUTUBE["API_URL"] = youtube_api_url
    YOUTUBE["API_KEY"] = os.getenv("YOUTUBE_API_KEY")
    cfg["YOUTUBE"] = YOUTUBE

    c = sqlite3.connect(database_file, check_same_thread=False)
    c.execute("PRAGMA foreign_keys = ON")
    cfg["DB_CONN"] = c
    
    with open(database_schema_file, "r") as f:
        schema = f.read()
        cursor = cfg["DB_CONN"].cursor()
        cursor.executescript(schema)
    
    return cfg

