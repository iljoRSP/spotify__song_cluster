from spcl_api_handler import ApiHandler
from spcl_data_processor import DataProcessor



if __name__ == '__main__':

    ### EXTRACT DATA ###
    api_communicator = ApiHandler()

    features_raw = api_communicator \
        .request_track_ids()        \
        .request_audio_features()   \
        .get_features_raw()

    # from pickle import dump
    # with open("../temp/raw_features.bin", 'wb') as f:
    #     dump(features_raw, f)
    # quit()

    ### CREATE PLAYLISTS ###
    data_processor = DataProcessor()

    id_cluster_map = data_processor     \
        .import_features(features_raw)  \
        .perform_clustering()           \
        .get_id_cluster_map()

    api_communicator.create_playlists(id_cluster_map)


    ### CREATE SMOOTH QUEUE ###
    id_smooth_queue = data_processor    \
        .perform_smooth_queue()

    api_communicator.create_smooth_queue(id_smooth_queue)


    print('Success')
