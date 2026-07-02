from internal.youtube.artist import getArtistsByChannelId
import requests
import os

default_thumbnails_path = "assets/thumbnails"


def download_thumbnail(url: str, filename, path=default_thumbnails_path):
    res = requests.get(url, params={"downloadformat": "png"})
    with open(f"{path}/{filename}", mode="wb") as file:
        file.write(res.content)


def download_youtube_missing_thumbnails(conn):

    cursor = conn.cursor()

    res = cursor.execute("SELECT youtube_channel_id FROM youtube_artists").fetchall()

    set_1 = set(i[0] for i in res)
    set_2 = set(i.split(".")[0] for i in os.listdir(default_thumbnails_path))

    diff = set_1.difference(set_2)
    
    for artist_id in diff:
        artist = getArtistsByChannelId(artist_id)
        print(artist)
        thumbnail_url = artist["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        download_thumbnail(thumbnail_url, filename=f"{artist_id}.png")
    
    return diff


def sanitize_input(string: str) -> str:
    
    return
