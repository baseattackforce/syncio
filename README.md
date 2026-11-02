# Syncio

Listen to your own music together, in sync. One static `index.html`, no backend. Works on GitHub Pages.

- **Stream mode**: the host's audio is sent live to listeners over WebRTC (via Web Audio, so it works on iOS WebKit). Listeners need no files.
- **Local files mode**: everyone picks the same files, and only play/pause/seek commands are synced. Best quality, and it keeps playing with the screen locked.

Deploy: push to GitHub, then Settings → Pages → deploy from branch `main` / root.
