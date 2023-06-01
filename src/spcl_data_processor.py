import numpy as np
from sklearn.cluster import KMeans


from typing import Callable, Any

def chainable(func: Callable[..., Any]) -> Callable[..., 'DataProcessor']:
    """
    Decorates a class method to return its instance `self`, plus type hinting
    """
    def wrapped_func(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self

    return wrapped_func


class DataProcessor:

    def __init__(self):
        self.ids = None
        self.features = None
        self.cluster_labels = None
        self.targeted_n_clusters = None

    @chainable
    def import_features(self, features_raw: dict):
        self.ids = np.array([d['id'] for d in features_raw])

        RETAINED_FEATURES = ['energy', 'acousticness', 'valence']
        self.features = np.array([[d[key] for key in RETAINED_FEATURES] for d in features_raw])


    @chainable
    def perform_clustering(self, clusters=None):
        if clusters is None:
            self.targeted_n_clusters = 3 + (len(self.features) > 1000)  # for larger datasets, use 4 clusters

        clustering_model = KMeans(
            n_clusters=self.targeted_n_clusters,
            n_init='auto'
        )

        self.cluster_labels = clustering_model.fit_predict(self.features)


    @chainable
    def guess_clusters(self):
        # guess what kind of songs are in a given playlist
        pass


    def get_id_cluster_map(self):
        grouped_clusters = {}

        for cluster_num in range(self.targeted_n_clusters):
            indices = np.where(self.cluster_labels == cluster_num)[0]
            grouped_clusters[cluster_num+1] = self.ids[indices]

        return grouped_clusters