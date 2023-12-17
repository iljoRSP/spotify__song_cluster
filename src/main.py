from spcl_api_handler import ApiHandler
from spcl_data_processor import DataProcessor



class AppWrapper:

    def __init__(self, credentials_location: str) -> None:
        self.handler = ApiHandler(credentials_location)
        self.handler.get_playlist_features()

        self.processor = DataProcessor()


    def __import_features_to_processor(self, debug=False):
        raw_feature_data = self.handler.features_raw
        self.processor.import_features(raw_feature_data)

        if debug:
            from pickle import dump
            with open("../temp/raw_features.bin", 'wb') as f:
                dump(raw_feature_data, f)


    def make_mood_playlists(self, num_playlists=None):
        self.__import_features_to_processor()
        playlist_data = self.processor.calculate_clusters()

        self.handler.create_playlists(playlist_data)


    def make_smooth_queue(self):
        self.__import_features_to_processor()
        queue_data = self.processor.calculate_smooth_queue()

        self.handler.create_smooth_queue(queue_data)



if __name__ == '__main__':
    print('This is MoodMixer. Start by logging into your Spotify account - or try \'help\'')
    while True:

        cmd = input('(mM) ')

        match cmd:
            case 'help':
                print('!help goes here!')


            case 'login':
                loc = input("\tCredentials location (leave empty for default): ")
                if loc == '':
                    loc = './config/spotify_client_credentials.json'

                print("\tConnecting to Spotify... ", end='')
                app = AppWrapper(loc)
                print('Success')


            case 'playlist':
                print('bet ... ', end='')
                app.make_mood_playlists()
                print('issa forst')


            case 'queue':
                print('aight sec ... ', end='')
                app.make_smooth_queue()
                print('pog')


            case 'exit':
                exit()


            case _:
                print("unknown command!")

        print()
