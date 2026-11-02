#!/usr/bin/env python3
"""Scan music/ and write music/library.json (+ cover.jpg per album).

Usage:  pip install mutagen && python3 tools/make-library.py
Layout: any folders under music/ containing .mp3 / .m4a / .aac / .flac / .ogg / .wav files.
Albums come from each file's tags; covers are extracted from embedded art.
"""
import json, re, sys
from pathlib import Path
from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp4 import MP4

ROOT = Path(__file__).resolve().parent.parent
MUSIC = ROOT / "music"
EXTS = {".mp3", ".m4a", ".aac", ".flac", ".ogg", ".wav"}

def first(v):
    return str(v[0]) if isinstance(v, (list, tuple)) and v else (str(v) if v else "")

def read(path):
    f = File(path, easy=True)
    t = f.tags if f and f.tags else {}
    title = first(t.get("title")) or path.stem
    artist = first(t.get("artist")) or first(t.get("albumartist")) or "Unknown artist"
    album = first(t.get("album")) or "Unknown album"
    try: no = int(first(t.get("tracknumber")).split("/")[0])
    except Exception: no = 999
    return title, artist, album, no

def cover_bytes(path):
    try:
        if path.suffix.lower() in (".m4a", ".aac"):
            c = MP4(path).tags.get("covr")
            return bytes(c[0]) if c else None
        if path.suffix.lower() == ".mp3":
            for k, v in ID3(path).items():
                if k.startswith("APIC"): return v.data
        f = File(path)
        pics = getattr(f, "pictures", None)
        return pics[0].data if pics else None
    except Exception:
        return None

def main():
    if not MUSIC.is_dir():
        sys.exit("No music/ folder found. Create it and add your files first.")
    albums = {}
    for p in sorted(MUSIC.rglob("*")):
        if p.suffix.lower() not in EXTS: continue
        title, artist, album, no = read(p)
        a = albums.setdefault(album.lower(), {"name": album, "artists": [], "tracks": [], "cover": None})
        a["artists"].append(artist)
        a["tracks"].append((no, title, artist, p))
        if not a["cover"]:
            data = cover_bytes(p)
            if data:
                out = p.parent / ("cover-" + re.sub(r"[^a-z0-9]+", "-", album.lower()).strip("-") + ".jpg")
                if not out.exists(): out.write_bytes(data)
                a["cover"] = out.relative_to(ROOT).as_posix()
    result = []
    for a in sorted(albums.values(), key=lambda x: x["name"].lower()):
        arts = a["artists"]; top = max(set(arts), key=arts.count)
        various = arts.count(top) < len(arts) * 0.6
        entry = {"name": a["name"], "artist": "Various artists" if various else top,
                 "tracks": [{"title": t, "artist": ar, "file": p.relative_to(ROOT).as_posix()}
                            for _, t, ar, p in sorted(a["tracks"], key=lambda x: (x[0], x[1]))]}
        if a["cover"]: entry["cover"] = a["cover"]
        result.append(entry)
    (MUSIC / "library.json").write_text(json.dumps({"albums": result}, indent=2, ensure_ascii=False))
    n = sum(len(x["tracks"]) for x in result)
    print(f"Wrote music/library.json: {len(result)} albums, {n} tracks")

if __name__ == "__main__":
    main()
