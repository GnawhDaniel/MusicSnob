import requests

def getArtistsByChannelId(channel_ids, api_url, api_key):
    r = requests.get(f"{api_url}/channels?part=statistics,brandingSettings,snippet&id={channel_ids}&key={api_key}")
    return r.json()