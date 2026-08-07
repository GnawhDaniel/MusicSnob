import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

print(f"DEBUG: dotenv found at = {find_dotenv()}")
found = load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")
print(f"DEBUG: load_dotenv success = {found}")

youtube_api_url = "https://www.googleapis.com/youtube/v3"
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
