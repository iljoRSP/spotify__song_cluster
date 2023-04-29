'''
step 1: sign on /

step 2: extract liked songs & tags /

step 3: perform agglomerative clustering

step 4: create playlists
'''

from spcl_api_data_extractor import ApiDataExtractor
from spcl_data_processor import DataProcessor



if __name__ == '__main__':
    extract = ApiDataExtractor()

    extract.login()
    extract.get_track_ids()
    extract.get_audio_features()


    process = DataProcessor()
    process.import_features(extract.features_raw)
