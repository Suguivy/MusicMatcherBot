import pandas as pd
import numpy as np
import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

class MusicRecommender:
    def __init__(self):
      self.dataset = None
      self.distance_matrix = None

    def load_all_from_csv(self, csv_file, dataset_output, matrix_output):
        if (not os.path.exists(dataset_output)):
            self.load_dataset_from_csv(csv_file, save_file=dataset_output)
        else:
            self.load_dataset_from_file(dataset_output)
        if (not os.path.exists(matrix_output)):
            self.calculate_matrix_from_dataset(matrix_output)
        else:
            self.load_matrix_from_file(matrix_output)

    def load_dataset_from_file(self, filename):
        print(f"Loading dataset '{filename}'...")

        if os.path.exists(filename):
            self.dataset = pd.read_pickle(filename)
        else:
            raise Exception('dataset file not found')

    def load_dataset_from_csv(self, csv_file, save_file='dataset'):
        """
        Creates and loads the distance matrix from the CSV file
        """
        print(f"Loading and converting '{csv_file}' into a dataset...")

        df = pd.read_csv(csv_file)
        df = df.sample(n=15000)
        df = df.reset_index()
        self.dataset = df

        print(f"Saving dataset as '{save_file}'")
        self.dataset.to_pickle(save_file)

    def _get_column_values(self, column_name):
        return self.dataset[column_name].to_numpy().reshape(-1,1)

    def _make_column_conf(self, column_name,metric,weight):
        return { 'value': self._get_column_values(column_name), 'metric': metric, 'weight': weight}

    def calculate_matrix_from_dataset(self, save_file='distance_matrix.npy'):
        print("Calculating matrix from dataset...")

        # Creation of the bag of words
        bow_model = TfidfVectorizer(max_features=5000)
        bow_model.fit(self.dataset['lyrics'])
        texts_bow = bow_model.transform(self.dataset['lyrics'])

        configuration_params = [
                  [texts_bow,'cosine',1],
                  #[genreBoW,'cosine',8],
                  ['dating','l2',4],
                  #['violence','l2',4],
                  ['world/life','l2',4],
                  ['night/time','l2',4],
                  ['shake the audience','l2',4],
                  ['family/gospel','l2',4],
                  ['romantic','l2',4],
                  ['communication','l2',4],
                  ['obscene','l2',4],
                  ['music','l2',4],
                  ['movement/places','l2',4],
                  ['light/visual perceptions','l2',4],
                  ['family/spiritual','l2',4],
                  ['like/girls','l2',4],
                  ['sadness','l2',4],
                  ['feelings','l2',4],
                  ['danceability','l2',4],
                  ['loudness','l2',4],
                  ['acousticness','l2',4],
                  ['instrumentalness','l2',4],
                  ['valence','l2',4],
                  ['energy','l2',4],
                  ['age','l2',4]
                ]
        configuration = list(map(lambda v: [self.dataset[v[0]].to_numpy().reshape(-1,1),v[1],v[2]] if isinstance(v[0],str) else v, configuration_params))

        # Calculation of the distance matrix
        accum = None
        total = 0
        for v in configuration:
            d = pairwise_distances(v[0], metric=v[1]) * v[2]
            if accum is None:
                accum = d
            else:
                accum = accum + d
            total = total + v[2]
        self.distance_matrix = accum / total

        print(f"saving matrix as '{save_file}")
        np.save(save_file, self.distance_matrix)

    def load_matrix_from_file(self, matrix_file):
        print(f"Loading matrix '{matrix_file}'...")
        if os.path.exists(matrix_file):
            self.distance_matrix = np.load(matrix_file)
        else:
            raise Exception(f"distance matrix file '{matrix_file}' not found")

    def similar_by_exact_title(self, title, count=1):
        song_idx = self.dataset[self.dataset['track_name']==title ].index.values[0]
        ordered_scores = sorted(enumerate(self.distance_matrix[song_idx]), key=lambda x: x[1])
        top_scores = ordered_scores[0:count+1]
        top_idx = [i[0] for i in top_scores]
        top_confidence = [i[1] for i in top_scores]
        top_similar = pd.Series(top_confidence,index=top_idx)
        songs = [(self.dataset.iloc[i].track_name, self.dataset.iloc[i].artist_name) for i, _ in top_similar.iteritems()]
        return songs
