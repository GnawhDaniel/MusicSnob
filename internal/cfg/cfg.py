import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"
print(f"DEBUG: __file__ = {Path(__file__).resolve()}", flush=True)
print(f"DEBUG: env_path = {env_path}", flush=True)
print(f"DEBUG: env_path exists = {env_path.exists()}", flush=True)

found = load_dotenv(dotenv_path=env_path, verbose=True)
print(f"DEBUG: load_dotenv success = {found}", flush=True)

youtube_api_url = "https://www.googleapis.com/youtube/v3"
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
