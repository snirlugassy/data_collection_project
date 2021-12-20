import random
import pickle
import pandas as pd
import numpy as np
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


nltk.download('stopwords')

CHUNK_SIZE = 100000
STOPWORDS = nltk.corpus.stopwords.words('english')
VECTORIZER_PICKLE = 'vectorizer.pkl'

labeled_data = 'labeled.csv'

data_types = {
    'text': str,
    'industry': str,
}

print('Loading industries')
industries = [x.strip() for x in open('industries.txt','r').readlines()]

industry_mean = {}

data = pd.read_csv(labeled_data, usecols=['text', 'industry'], dtype=data_types, engine='c')

print(f'Chunk {iter}')

data.reset_index(drop=True, inplace=True)

print('Replacing NaN text')
data.text.replace(np.nan, "", inplace=True)
print(data.info(memory_usage='deep'))

corpus = data.text

vectorizer = TfidfVectorizer()

print('Training TF-IDF Vectorizer')
X = vectorizer.fit_transform(corpus)
print("X Shape: ", X.shape)

print('Saving vectorizer to vectorizer.pkl')
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print('Calculating industry means')
industry_mean = {}
for i in industries:
    X_ind = X[data[data['industry']==i].index]
    _mean = X_ind.mean(axis=0)
    industry_mean[i] = _mean

means = np.stack([industry_mean[i] for i in industries])

print('Clustering industry means with k=20')
clustering = KMeans(n_clusters=20)
clustering.fit(means)

print('Saving clustering to clustering.pkl')
with open("clustering.pkl", "wb") as f:
    pickle.dump(clustering, f)


# # print(f'Reading CSV file {labeled_data}')
# # data = pd.read_csv(
# #     labeled_data, 
# #     usecols=['text', 'industry'],
# #     dtype=data_types,
# #     engine='c',
# #     # skiprows=lambda i: i>0 and random.random() > p
# # )

# data.reset_index(drop=True, inplace=True)

# print('Replacing NaN text')
# data.text.replace(np.nan, "", inplace=True)
# print(data.info(memory_usage='deep'))

# industries = data.industry.unique()

# corpus = data.text

# vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
# X = vectorizer.transform(corpus)

# # vectorizer = TfidfVectorizer()

# # print('Training TF-IDF Vectorizer')
# # X = vectorizer.fit_transform(corpus)
# # print("X Shape: ", X.shape)

# # print('Saving vectorizer to vectorizer.pkl')
# # with open("vectorizer.pkl", "wb") as f:
# #     pickle.dump(vectorizer, f)

# print('Calculating industry means')
# means = []
# industry_mean = {}
# for i in industries:
#     X_ind = X[data[data['industry']==i].index]
#     _mean = X_ind.mean(axis=0)
#     means.append(_mean)
#     industry_mean[i] = _mean
# means = np.stack(means)


# print('Clustering industry means with k=20')
# clustering = KMeans(n_clusters=20).fit(means)

# print('Saving clustering to clustering.pkl')
# with open("clustering.pkl", "wb") as f:
#     pickle.dump(clustering, f)
