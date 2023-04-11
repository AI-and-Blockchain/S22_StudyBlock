from gensim.models.word2vec import Word2Vec as w2v

import pandas as pd
import re

from sklearn.decomposition import PCA

from matplotlib import pyplot as plt
import plotly.graph_objects as go

import numpy as np

import warnings

warnings.filterwarnings('ignore')

# Example sentences scraped from breast cancer clinical trial research

sentences = ['This clinical trial studies how well paclitaxel, trastuzumab, and pertuzumab work in eliminating further'
             ' chemotherapy after surgery in patients with HER2-positive stage II-IIIa breast cancer who have no cancer'
             ' remaining at surgery'.split(' '),
             'This phase III trial compares the effect of usual treatment with trastuzumab emtansine (T-DM1) alone vs. '
             'T-DM1 in combination with tucatinib. T-DM1 is a monoclonal antibody, called trastuzumab, linked to a '
             'chemotherapy drug, called DM'.split(' '),
             'This phase III trial compares the effect of radiation therapy combined with hormonal therapy versus '
             'hormonal therapy alone in treating patients with low risk, early stage breast cancer with Oncotype'
             ' Dx Recurrence =< 18'.split(' '),
             'This randomized phase III trial studies if not giving regional radiotherapy is just as good as using '
             'regional radiotherapy in keeping breast cancer from coming back in patients with estrogen receptor '
             '(ER) positive, HER2 negative node positive low risk breast cancer who have undergone breast '
             'conserving surgery or mastectomy'.split(' ')]

w2v = w2v(sentences, min_count=1)

print(w2v)

words = list(w2v.wv.key_to_index)
index = w2v.wv.get_vecattr('cancer', 'count')
print(words)
print(index)

# update from here below
X = w2v[w2v.wv.key_to_index]
pca = PCA(n_components=2)

result = pca.fit_transform(X)

# create a scatter plot of the projection
plt.scatter(result[:, 0], result[:, 1])
words = list(w2v.wv.key_to_index)

for i, word in enumerate(words):
    plt.annotate(word, xy=(result[i, 0], result[i, 1]))

plt.show()
