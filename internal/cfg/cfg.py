from dotenv import load_dotenv
import os
load_dotenv()

youtube_api_url = "https://www.googleapis.com/youtube/v3"
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
