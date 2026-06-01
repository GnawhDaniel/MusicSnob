import requests

default_thumbnails_path = "assets/thumbnails"

def download_thumbnail(url: str, filename, path=default_thumbnails_path):
    res = requests.get(url, params={"downloadformat": "png"})
    with open(f"{default_thumbnails_path}/{filename}", mode="wb") as file:
        file.write(res.content)
        