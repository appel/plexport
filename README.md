# plexport.py
Plexport.py is a simple python script which I cooked up with the help of ChatGPT, which connects to Plex, scans for predefined playlists, downloads associated FLAC files, populates the playlists in a Walkman compatible format and converts album art so it shows up on my NW-A45 walkman.

This is very much a work in progress and I can barely read Python, so please bear with me. Please report any issues you encounter. Forks and pull requests encouraged!

## How to install:

1. Make sure Python 3 is installed (I use WSL2 on Windows 11).
2. Install the excellent [PlexAPI]([url](https://github.com/pkkid/python-plexapi)) library with `pip install plexapi` (YMMV).
3. Download the plexport.py script to your home folder and change the `plex_url` and `plex_token` variables at the top.
4. Also change the `EXPORT_DIR`, `PLAYLIST_NAMES` and `BASE_PATH` variables to match your environment.
6. Make the script executable: `chmod +x plexport.py`.
7. Run the script with `./plexport.py`.

Use `CTRL + C` to abort the script after finishing the current operation.
