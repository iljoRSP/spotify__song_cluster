import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import __cred


# establish connection
print('Establishing connection with Spotify API...\t', end = '')
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=__cred.client_id, 
        client_secret=__cred.client_secret, 
        redirect_uri=__cred.redirect_url, 
        scope=scope
        )
    )
print('Success.')



with open('.\data\output.json', 'w+') as f:
    exit_flag = False
    running_offset = 0
    ctr = 1
    master = []

    # continue requesting songs (at specified batch size) until all songs queried
    print('Requesting Liked Songs list...')
    while not exit_flag:
        print(f'\tProcessing batch #{ctr}')

        print('\t\tQuerying tracks')
        src = sp.current_user_saved_tracks(limit=__cred.batch_size, offset=running_offset)['items']

        batch_ids = [song['track']['id'] for song in src]

        print("\t\tRequesting tracks' audio features...")
        features = sp.audio_features(batch_ids)

        # add name field
        for fe in features:
            master.append(fe)

        exit_flag = len(src) < __cred.batch_size  # check if last batch
        running_offset += __cred.batch_size
        ctr += 1

    print('\t\tWriting to file...')
    json.dump(master, f)


print("All done.")