import pandas as pd
import numpy as np
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

# Converts the CSV data into a dataframe
originalData = pd.read_csv('spotify_songs.csv')

# We get rid of the songs that are not in English, to make correct predictions based in the lyrics
englishSongs = originalData.query('language == "en"')
englishSongs = englishSongs.reset_index()
englishSongs['english_index'] = range(0,len(englishSongs))

useCachedData = True

preprocessedData = None
if not useCachedData :
  nltk.download('punkt')
  nltk.download('stopwords')
  ps = PorterStemmer()
  preprocessedText = []
  i = 0
  for row in englishSongs.itertuples():
    text = word_tokenize(row.lyrics) ## indice de la columna que contiene el texto
    ## Remove stop words
    stops = set(stopwords.words("english"))
    text = [ps.stem(w) for w in text if not w in stops and w.isalnum()]
    text = " ".join(text)

    preprocessedText.append(text)
    if i % 100 == 0:
      print(i)
    i += 1

  preprocessedData = englishSongs
  preprocessedData['processed_text'] = preprocessedText
else:
  preprocessedData = pd.read_pickle("data")

bagOfWordsModel = TfidfVectorizer()
bagOfWordsModel.fit(preprocessedData['processed_text'])
textsBoW= bagOfWordsModel.transform(preprocessedData['processed_text'])

def getLyrics(title,dataset):
  songIndex = dataset[dataset['track_name']==title].index.values[0]
  return dataset.loc[songIndex]['lyrics']

def getSong(title,dataset):
  songIndex = dataset[dataset['track_name']==title].index.values[0]
  return dataset.loc[songIndex]

def getSongByIndex(idx,dataset):
  return dataset.loc[idx]

def getColumnValues(column_name,dataset):
  return dataset[column_name].to_numpy().reshape(-1,1)

def makeColumnConf(column_name,metric,weight):
  return { 'value': getColumnValues(column_name,preprocessedData), 'metric': metric, 'weight': weight}

configuration = {
    "lyrics": { 'value': textsBoW
               , 'metric': 'cosine'
               , 'weight': 1},
    'valences': makeColumnConf('valence','l1',20),
    #'loudness': { 'value': getColumnValues('loudness',preprocessedData), 'metric': 'l1', 'weight': 20},
    'tempo': makeColumnConf('tempo','l1',20),
    'danceability': makeColumnConf('danceability','l1',20),
    'energy': makeColumnConf('energy','l1',20),
    'speechiness': makeColumnConf('speechiness','l1',20),
    'acousticness': makeColumnConf('acousticness','l1',20),
    'instrumentalness': makeColumnConf('instrumentalness','l1',20),
    #'key' : makeColumnConf('key','l1',20),
    #'mode' : makeColumnConf('mode','l1',20),
    }

useCachedMatrix = True
def getDistanceMatrix(configuration):
  if useCachedMatrix and os.path.exists("distanceMatrix.npy"):
    m = np.load("distanceMatrix.npy")
    return m
  else:
    accum = None
    total = 0
    for k,v in configuration.items():
      d = pairwise_distances(v['value'],v['value'],metric=v['metric'])*v['weight']
      if accum is None:
        accum = d
      else:
        accum = accum + d
      total = total + v['weight']
    m = accum/total
    np.save("distanceMatrix.npy", m)
    return m

def similar(searchTitle,distanceMatrix,dataset):
   songIndex = preprocessedData[dataset['track_name']==searchTitle].index.values[0]
   distance_scores = list(enumerate(distanceMatrix[songIndex]))
   ordered_scores = sorted(distance_scores, key=lambda x: x[1])
   top_scores = ordered_scores[1:11]
   top_indexes = [i[0] for i in top_scores]
   top_confidence = [i[1] for i in top_scores]
   d = dataset['track_name'].iloc[top_indexes].to_frame()

   d['confidence'] = pd.Series(top_confidence,index=top_indexes)
   return d

distanceConf = getDistanceMatrix(configuration)

#@title Sistema recomendador
#@markdown Inserte el título de la canción para obtener canciones similares.
searchTitle = "Op Opa"  #@param {type: "string"}
#@markdown ---
results = similar(searchTitle,distanceConf,preprocessedData)
print(results.head(10))
print(type(results))

song = getSong(searchTitle, preprocessedData)
searchString = song['track_name'] + ' ' + song['track_artist']
