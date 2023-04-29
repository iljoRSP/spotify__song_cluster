import spcl_client_creds
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util


class ApiDataExtractor:

    def __init__(self):
        self.endpoint = None
        self.track_ids = []
        self.features_raw = []


    def login(self):
        _auth_manager = SpotifyOAuth(
            client_id     = spcl_client_creds.client_id,
            client_secret = spcl_client_creds.client_secret,
            redirect_uri  = spcl_client_creds.redirect_url,
            scope         = "user-library-read"
        )

        self.endpoint = spotipy.Spotify(auth_manager=_auth_manager)


    def get_track_ids(self):
        _batches_processed = 0
        _batch_size = 50

        while True:
            batch = self.endpoint.current_user_saved_tracks(
                        limit=_batch_size,
                        offset=_batch_size*_batches_processed
                    )['items']

            self.track_ids += list(map(
                lambda item: item['track']['id'],
                batch
            ))

            # check if last batch
            if len(batch) < _batch_size:
                break

            _batches_processed += 1


    def get_audio_features(self):
        _batches_processed = 0
        _batch_size = 100
        _max = len(self.track_ids)

        while True:
            batch = self.track_ids[(start := _batches_processed*_batch_size):(end := min(start+_batch_size, _max))]

            self.features_raw += self.endpoint.audio_features(batch)

            # check if done
            if end == _max:
                break

            _batches_processed += 1