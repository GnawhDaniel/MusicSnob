<div align="center">
<h1>MusicSnob</h1>
</div>

MusicSnob is an artist stats tracker for the hipsters who loves discovering new, up-and-coming bands. Currently, it is only capable of using YouTube's API to pull data daily.

> This project is very much still a WIP with many improvements to be made. But if you ever want to setup an instance for yourself, the app can be built using docker.

## Installation
1. Copy and rename .env.example to .env
2. Fill in MUSICSNOB_USER, MUSICSNOB_PASS, and YOUTUBE_API_KEY in .env
3. Run `docker compose -f compose-prod up --build`
4. Navigate to http://localhost:5000 