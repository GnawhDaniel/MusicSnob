import requests
from internal.cfg.cfg import youtube_api_url, cfg

def getArtistsByChannelId(channel_ids):
    r = requests.get(f"{youtube_api_url}/channels?part=statistics,brandingSettings,snippet&id={channel_ids}&key={cfg["YOUTUBE"]["API_KEY"]}")
    return r.json()