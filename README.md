# Syncio

Listen to your own music together, in sync. Static site, no backend, works on GitHub Pages and is built for iOS (Safari and Chrome).

## How it works
1. Tap **+ Add music** and pick songs **or a .zip of them** from your phone (zips are unzipped on the device, nothing is uploaded). Albums, titles, artists and cover art are read from each file's tags and saved on the device (IndexedDB).
2. Tap an album. That starts a party and gives you a 4-letter code (or tap **Invite** to share a link).
3. Friends type the code under **Join party**. The host's audio is streamed live to them over WebRTC (via Web Audio, since iOS has no `captureStream()`).
4. Everyone can pause, skip and go back. Only the host can shuffle or change album.

The lock screen / Dynamic Island show the song title, artist, album and cover through the Media Session API.

Add to Home Screen for a standalone app and so iOS doesn't clear the saved library after a week of non-use.

## Optional: albums hosted in this repo
Put files under `music/` and add `music/library.json`:

```json
{ "albums": [ {
  "name": "My Album", "artist": "Me", "cover": "music/my-album/cover.jpg",
  "tracks": [ { "title": "Intro", "file": "music/my-album/01.mp3" } ]
} ] }
```
Only do this with music you have the rights to publish: a public Pages site is public.

## Deploy
Settings → Pages → deploy from branch `master`, root folder.

## Building `library.json` automatically
Drop your files under `music/` (any folder layout), then:

```
pip install mutagen
python3 tools/make-library.py
```
It reads each file's tags, groups them into albums, extracts embedded cover art, and writes `music/library.json`.
