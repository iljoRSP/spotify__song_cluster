# import pickle

# RAW_FEATURES_CACHE = './data/raw_features.bin'
# CLUSTERED_IDS_CACHE = './data/clustered_ids.bin'

# def cache_raw_features(raw_features):
#     with open(RAW_FEATURES_CACHE, 'wb') as f:
#         pickle.dump(raw_features, f)


# def read_raw_features_cache():
#     with open(RAW_FEATURES_CACHE, 'rb') as f:
#         return pickle.load(f)


# def read_clustered_ids():
#     with open(CLUSTERED_IDS_CACHE, 'rb') as f:
#         return pickle.load(f)


from spcl_api_handler import ApiHandler
from spcl_data_processor import DataProcessor


if __name__ == '__main__':

    ### EXTRACT DATA ###
    api_communicator = ApiHandler()

    features_raw = api_communicator \
        .request_track_ids()        \
        .request_audio_features()   \
        .get_features_raw()


    ### PROCESS DATA ###
    data_processor = DataProcessor()

    id_cluster_map = data_processor     \
        .import_features(features_raw)  \
        .perform_clustering()           \
        .get_id_cluster_map()


    ### CREATE PLAYLISTS ###
    api_communicator.create_playlists(id_cluster_map)

    print('Success')