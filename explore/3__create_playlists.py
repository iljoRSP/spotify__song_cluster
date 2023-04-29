import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import spcl_client_creds


print('Establishing connection with Spotify API...\t', end = '')
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spcl_client_creds.client_id, client_secret=spcl_client_creds.client_secret, redirect_uri=spcl_client_creds.redirect_url, scope=scope))

print('Success.')

print('Creating playlists...')
for i, of in enumerate(os.listdir('.\data\plcodes')):
    if not of.endswith('.txt'): continue

    print(f'\tPlaylist {i+1}...')
    with open(f'.\data\plcodes\{of}') as f:
        items = f.read().splitlines()
        chunks = [items[100*i:100*(i+1)] for i in range(len(items)//100 + 1)]

        pl_id = sp.user_playlist_create(user=sp.me()['id'], name=f'Generated Playlist {i+1}', public=False, description='Auto generated playlist from Liked Songs.')['id']
        
        for chunk in chunks:
            sp.playlist_add_items(pl_id, chunk)
print('All Done.')