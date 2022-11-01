import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import __cred


def main():

    ########  establish connection to API  ######## 
    
    print('Establishing connection with Spotify API...\t', end = '')

    scope = "user-library-read"

    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=__cred.client_id, 
                client_secret=__cred.client_secret, 
                redirect_uri=__cred.redirect_url, 
                scope=scope
                )
            )
    except Exception as e:
        print(e)
        return

    print('Success.')




    ########  prep json for raw data  ######## 
    with open('..\spotify__song_cluster\src\data\output.json', 'w+') as f:
        print('Requesting Liked Songs list...')

        end_of_playlist = False
        running_offset = 0
        ctr = 1
        master = []
        batch_size = __cred.batch_size if __cred.batch_size else 20

        # continue requesting songs (at specified batch size) until all songs queried
        while not end_of_playlist:
            print(f'\tProcessing batch #{ctr}')

            print('\t\tQuerying tracks')
            src = sp.current_user_saved_tracks(limit=batch_size, offset=running_offset)['items']

            batch_ids = [song['track']['id'] for song in src]

            print("\t\tRequesting tracks' audio features...")
            features = sp.audio_features(batch_ids)

            # add name field
            for fe in features:
                master.append(fe)

            end_of_playlist = len(src) < batch_size  # check if last batch
            running_offset += batch_size
            ctr += 1

        print('\t\tWriting to file...')
        json.dump(master, f)

    print("All done.")




if __name__ == '__main__': 
    main()