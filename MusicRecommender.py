import pandas as pd
import numpy as np
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
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
        df = df.query("language == 'en'") # We only want songs in english to get appropiate words to work with
        df = df.reset_index()
        df['english_index'] = range(0, len(df))

        # Tokenization of words
        nltk.download('punkt', download_dir='./nltk_data')
        nltk.download('stopwords', download_dir='./nltk_data')
        nltk.data.path.append('./nltk_data')
        ps = PorterStemmer()
        preprocessed_text = []
        i = 0
        for row in df.itertuples():
            tokenized_words = word_tokenize(row.lyrics)
            stops = set(stopwords.words("english"))
            words = [ps.stem(word) for word in tokenized_words if not word in stops and word.isalnum()]
            words = " ".join(words)
            preprocessed_text.append(words)

        self.dataset = df
        self.dataset['processed_text'] = preprocessed_text

        print(f"Saving dataset as '{save_file}'")
        self.dataset.to_pickle(save_file)

    def _get_column_values(self, column_name):
        return self.dataset[column_name].to_numpy().reshape(-1,1)

    def _make_column_conf(self, column_name,metric,weight):
        return { 'value': self._get_column_values(column_name), 'metric': metric, 'weight': weight}

    def calculate_matrix_from_dataset(self, save_file='distance_matrix.npy'):
        print("Calculating matrix from dataset...")

        # Creation of the bag of words
        bow_model = TfidfVectorizer()
        bow_model.fit(self.dataset['processed_text'])
        texts_bow = bow_model.transform(self.dataset['processed_text'])

        configuration = {
            'lyrics': { 'value': texts_bow,
                        'metric': 'cosine',
                        'weight': 1
                      },
            'valences': self._make_column_conf('valence','l1',20),
            #'loudness': { 'value': getColumnValues('loudness',preprocessedData), 'metric': 'l1', 'weight': 20},
            'tempo': self._make_column_conf('tempo','l1',20),
            'danceability': self._make_column_conf('danceability','l1',20),
            'energy': self._make_column_conf('energy','l1',20),
            'speechiness': self._make_column_conf('speechiness','l1',20),
            'acousticness': self._make_column_conf('acousticness','l1',20),
            'instrumentalness': self._make_column_conf('instrumentalness','l1',20),
            #'key' : self._make_column_conf('key','l1',20),
            #'mode' : self._make_column_conf('mode','l1',20),
        }

        # Calculation of the distance matrix
        accum = None
        total = 0
        for k, v in configuration.items():
            d = pairwise_distances(v['value'], v['value'], metric=v['metric']) * v['weight']
            if accum is None:
                accum = d
            else:
                accum = accum + d
            total = total + v['weight']
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
        song_index = self.dataset[self.dataset['track_name']==title].index.values[0]
        distance_scores = list(enumerate(self.distance_matrix[song_index]))
        ordered_scores = sorted(distance_scores, key=lambda x: x[1])
        top_scores = ordered_scores[1:count+1]
        top_indexes = [i[0] for i in top_scores]
        top_confidence = [i[1] for i in top_scores]
        d1 = self.dataset['track_name'].iloc[top_indexes].to_frame()
        d2 = self.dataset['track_artist'].iloc[top_indexes].to_frame()

        return list(zip(d1['track_name'].tolist(), d2['track_artist'].tolist()))
