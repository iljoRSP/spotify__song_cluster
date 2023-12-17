from json import loads

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth



class ApiHandler:

    def __init__(self, credentials_location):
        self.track_ids = []
        self.track_names = []
        self.features_raw = []

        self.endpoint = self.__auth_to_API(credentials_location)


    def __auth_to_API(self, path: str):
        """
        Autheticate with Spotify API using credentials at path
        """
        with open(path, 'r') as f:
            creds = loads(f.read())

        _auth_manager = SpotifyOAuth(
            client_id     = creds['client_id'],
            client_secret = creds['client_secret'],
            redirect_uri  = 'http://localhost:9000',
            scope         = "user-library-read playlist-modify-private"
        )

        return Spotify(auth_manager=_auth_manager)


    def get_playlist_features(self):
        self.__request_track_ids()
        self.__request_audio_features()


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


    def create_smooth_queue(self, sequence: list):
        """
        Creates a playlist where consecutive songs are very similar.
        """

        new_playlist = self.endpoint.user_playlist_create(
            user=self.endpoint.me()['id'],
            name=f'Smooth Queue',
            public=False,
            description='Auto generated playlist from Liked Songs.'
        )

        _batch_size = 100
        for i in range(0, len(sequence), _batch_size):

            batch = sequence[i:i+_batch_size]
            self.endpoint.playlist_add_items(new_playlist['id'], batch)


    def __request_track_ids(self):
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


    def __request_audio_features(self):
        """
        Retrieve audio features for each track ID.
        """
        _batch_size = 100

        for i in range(0, len(self.track_ids), _batch_size):

            batch = self.track_ids[i:i+_batch_size]
            self.features_raw += self.endpoint.audio_features(batch)

        self.features_raw = [{**d1, **d2} for d1, d2 in zip(self.features_raw, [{'track_name': n} for n in self.track_names])]
