import numpy as np
from sklearn.cluster import KMeans



class DataProcessor:

    def __init__(self):
        self.ids = None
        self.features = None
        self.cluster_labels = None
        self.targeted_n_clusters = None


    def import_features(self, features_raw: dict):
        self.ids = np.array([d['id'] for d in features_raw])

        RETAINED_FEATURES = ['energy', 'acousticness', 'valence']
        self.features = np.array([[d[key] for key in RETAINED_FEATURES] for d in features_raw])


    def calculate_clusters(self, clusters=None):
        if clusters is None:
            self.targeted_n_clusters = 3 + (len(self.features) > 1000)  # for larger datasets, use 4 clusters

        clustering_model = KMeans(
            n_clusters=self.targeted_n_clusters,
            n_init='auto'
        )

        self.cluster_labels = clustering_model.fit_predict(self.features)

        return self.__get_id_cluster_map()


    def calculate_smooth_queue(self):
        from itertools import combinations
        from networkx import Graph
        from networkx.algorithms.approximation import christofides

        graph = Graph()

        for i_u, i_v in combinations(range(len(self.ids)), 2):
            id_u, id_v = self.ids[i_u], self.ids[i_v]
            u, v = self.features[i_u], self.features[i_v]

            weight = np.sqrt(np.sum(np.square(u - v)))

            graph.add_weighted_edges_from([(id_u, id_v, weight)])

        self.smooth_queue = christofides(graph)

        return self.smooth_queue


    def __guess_clusters(self):
        # guess what kind of songs are in a given playlist
        pass


    def __get_id_cluster_map(self):
        grouped_clusters = {}

        for cluster_num in range(self.targeted_n_clusters):
            indices = np.where(self.cluster_labels == cluster_num)[0]
            grouped_clusters[cluster_num+1] = self.ids[indices]

        return grouped_clusters
