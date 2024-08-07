#!/usr/bin/env python3

import os
import io
import signal
import sys
import requests
from mutagen import File
from mutagen.flac import FLAC, Picture
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
from plexapi.server import PlexServer
from PIL import Image


# Plex server details and authentication
plex_url = 'http://127.0.0.1:32400' # Change this to your Plex server URL
plex_token = 'sEcReTpLeXtOkEn' # Change this to your Plex token

try:
    server = PlexServer(plex_url, plex_token)
except requests.exceptions.ConnectionError:
    print(f"Connection failed, hostname '{plex_url}' not found.")
    sys.exit(1)

EXPORT_DIR = './export'
PLAYLIST_NAMES = ['All liked', '80s', 'Calm', 'Jazz', 'Hip-Hop & Downbeat', 'Favorite Albums']  # List of existing playlist names to process
BASE_PATH = '/share/Music/'  # Base path to your music files on the Plex server

# Setup graceful exit
def signal_handler(sig, frame):
    print('Ctrl+C pressed, exiting after current operation...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def convert_to_baseline_jpeg(image_data):
    # Load image from bytes
    image = Image.open(io.BytesIO(image_data))
    if image.format == 'JPEG' and image.info.get('progressive', False):
        # Convert progressive JPEG to baseline JPEG
        with io.BytesIO() as output:
            image.save(output, format='JPEG', progressive=False)
            print("JPG converted to baseline")
            return output.getvalue()
    return image_data  # Return original data if no conversion is necessary

def update_album_art(file_path):
    if file_path.endswith('.flac'):
        try:
            flac_file = FLAC(file_path)
            any_cover = None
            # Iterate over any pictures and use the first one found
            if flac_file.pictures:
                any_cover = flac_file.pictures[0]  # Use the first picture found

            if any_cover:
                converted_data = convert_to_baseline_jpeg(any_cover.data)
                back_cover = Picture()
                back_cover.data = converted_data
                back_cover.type = 4  # Set as back cover
                back_cover.mime = any_cover.mime
                back_cover.desc = 'Back Cover'
                flac_file.add_picture(back_cover)
                flac_file.save()
                print(f"Back cover added to {file_path}")
            else:
                print(f"No pictures found in {file_path}")

        except Exception as e:
            print(f"Error processing FLAC file {file_path}: {e}")
    elif file_path.endswith('.mp3'):
        try:
            mp3_file = MP3(file_path, ID3=ID3)
            any_cover = None
            if 'APIC:' in mp3_file.tags:
                any_cover = mp3_file.tags['APIC:']  # Use the first APIC found

            if any_cover:
                converted_data = convert_to_baseline_jpeg(any_cover.data)
                back_cover = APIC(
                    encoding=any_cover.encoding,
                    mime=any_cover.mime,
                    type=4,  # back cover
                    desc='Back Cover',
                    data=converted_data
                )
                mp3_file.tags.add(back_cover)
                mp3_file.save()
                print(f"Back cover added to {file_path}")
            else:
                print(f"No pictures found in {file_path}")

        except Exception as e:
            print(f"Error processing MP3 file {file_path}: {e}")

def main():
    # Ensure the export directory exists
    os.makedirs(EXPORT_DIR, exist_ok=True)

    for playlist_name in PLAYLIST_NAMES:
        playlist = server.playlist(playlist_name)
        print(f"Processing playlist: {playlist_name}")

        playlist_file_path = os.path.join(EXPORT_DIR, f"{playlist_name}.m3u")
        with open(playlist_file_path, 'w') as playlist_file:
            playlist_file.write('#EXTM3U\n')

            for item in playlist.items():
                if item.TYPE == 'track':
                    original_path = item.media[0].parts[0].file
                    # print(f"Original file path: {original_path}")

                    relative_path = os.path.relpath(original_path, start=BASE_PATH)
                    export_path = os.path.join(EXPORT_DIR, relative_path)
                    export_dir = os.path.dirname(export_path)

                    # Ensure the target directory exists
                    os.makedirs(export_dir, exist_ok=True)

                    # Download the file if it does not exist
                    if not os.path.exists(export_path):
                        print(f"Downloading: {os.path.basename(export_path)}")
                        item.download(savepath=export_dir, keep_original_name=True)

                    # Process album art update and playlist addition
                    if os.path.exists(export_path):
                        update_album_art(export_path)
                        # Get track metadata
                        try:
                            audio = File(export_path, easy=True)
                            duration = int(audio.info.length)
                            track_title = audio['title'][0] if 'title' in audio else 'Unknown Track'
                        except Exception as e:
                            print(f"Error reading tags from {os.path.basename(export_path)}: {e}")
                            track_title = 'Unknown Track'
                            duration = 0

                        # Correctly format the path for the M3U file
                        relative_export_path = os.path.relpath(export_path, start=EXPORT_DIR)
                        playlist_file.write(f'#EXTINF:{duration}, {track_title}\n')
                        playlist_file.write(f'{relative_export_path}\n')
                        print(f"Adding {os.path.basename(export_path)} to playlist.")

        print(f"All tasks completed for {playlist_name}. Playlist file created at: {playlist_file_path}")

if __name__ == "__main__":
    main()
