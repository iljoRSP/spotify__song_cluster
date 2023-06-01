import spcl_client_creds

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from typing import Callable, Any


def chainable(func: Callable[..., Any]) -> Callable[..., 'ApiHandler']:
    """
    Decorates a class method to return its instance `self`, plus type hinting
    """
    def wrapped_func(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self

    return wrapped_func


class ApiHandler:

    def __init__(self):
        self.login()
        self.track_ids = []
        self.track_names = []
        self.features_raw = []


    @chainable
    def login(self):
        """
        Autheticate with Spotify API
        """
        _auth_manager = SpotifyOAuth(
            client_id     = spcl_client_creds.client_id,
            client_secret = spcl_client_creds.client_secret,
            redirect_uri  = spcl_client_creds.redirect_url,
            scope         = "user-library-read playlist-modify-private"
        )

        self.endpoint = Spotify(auth_manager=_auth_manager)


    @chainable
    def request_track_ids(self):
        """
        Retrieve track IDs from user's Liked Songs.
        """
        _batches_processed = 0
        _batch_size = 50

        while True:
            batch = self.endpoint.current_user_saved_tracks(
                        limit=_batch_size,
                        offset=_batch_size*_batches_processed
                    )['items']

            self.track_ids += [item['track']['id'] for item in batch]
            self.track_names += [item['track']['name'] for item in batch]

            # check if last batch
            if len(batch) < _batch_size:
                break

            _batches_processed += 1


    @chainable
    def request_audio_features(self):
        """
        Retrieve audio features for each track ID.
        """
        _batch_size = 100

        for i in range(0, len(self.track_ids), _batch_size):

            batch = self.track_ids[i:i+_batch_size]
            self.features_raw += self.endpoint.audio_features(batch)

        self.features_raw = [{**d1, **d2} for d1, d2 in zip(self.features_raw, [{'track_name': n} for n in self.track_names])]


    def get_features_raw(self):
        """
        Get method for features_raw
        """
        return self.features_raw


    def create_playlists(self, clustered_ids: dict):
        """
        Create playlists for each cluster
        """

        for cluster, id_list in clustered_ids.items():
            new_playlist = self.endpoint.user_playlist_create(
                user=self.endpoint.me()['id'],
                name=f'Generated Playlist {cluster}',
                public=False,
                description='Auto generated playlist from Liked Songs.'
            )

            _batch_size = 100
            for i in range(0, len(id_list), _batch_size):

                batch = id_list[i:i+_batch_size]
                self.endpoint.playlist_add_items(new_playlist['id'], batch)
