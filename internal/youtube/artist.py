import requests
from internal.cfg.cfg import youtube_api_url, youtube_api_key

def getArtistsByChannelId(channel_ids):
    r = requests.get(f"{youtube_api_url}/channels?part=statistics,brandingSettings,snippet&id={channel_ids}&key={youtube_api_key}")
    return r.json()