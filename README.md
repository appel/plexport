# plexport.py
Plexport.py is a simple python script that connects to your Plex server, scans for predefined playlists, downloads referenced FLAC files whilst maintaining the original file and folder structure, creates Walkman compatible playlists and converts the album art so it shows up on my NW-A45 walkman.

Please note that I created this script with the help of ChatGPT. It's very much a work in progress and I'm farely new to Python, so please bear with me and [report any issues](https://github.com/appel/plexport/issues/new) you encounter. Forks and pull requests encouraged!

## How to install:

1. Make sure Python 3 is installed (I use WSL2 on Windows 11).
2. Install the excellent [PlexAPI](https://github.com/pkkid/python-plexapi) module with `pip install plexapi`. This facilitates the connection with Plex.
3. Also install the equally excellent [Mutagen](https://mutagen.readthedocs.io/) module with `pip install mutagen`. This module converts album art so that your Walkman can read it.
4. Download the plexport.py script to your home folder and change the `plex_url` and `plex_token` variables at the top. [This article](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) explains how you can obtain an API token for your Plex server.
5. Also change the `EXPORT_DIR`, `PLAYLIST_NAMES` and `BASE_PATH` variables to match your environment.
6. Make the script executable: `chmod +x plexport.py`.
7. Run the script with `./plexport.py`.

The script will run until it's done. If you need to abort the operation, use `CTRL + C`. It will gradefully exit after it is done processing the current FLAC.
