<div align="center">
<h1>MusicSnob</h1>
</div>

MusicSnob is an artist stats tracker for the hipsters who loves discovering new, up-and-coming bands. Currently, it is only capable of using YouTube's API to pull data daily.

> This project is very much still a WIP with many improvements to be made. But if you ever want to setup an instance for yourself, the app can be built using docker.

## Installation
1. Clone the repo.
2. `cp .env.example .env` 
3. In .env, fill in MUSICSNOB_USER, MUSICSNOB_PASS, and YOUTUBE_API_KEY.
4. Run `docker compose -f compose-prod up --build`
5. Access the website on localhost port 5000.