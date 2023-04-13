import os
import pandas as pd
import numpy as np
import pickle
import spacy
import scispacy
from tqdm import tqdm
import matplotlib.pyplot as plt
from gensim.models.fasttext import FastText
from rank_bm25 import BM25Okapi
import nmslib
import time


class Model:
    def __init__(self, csv):
        self.docs = pd.read_csv(csv)
        self.title = docs['Study'].tolist()
        self.text = docs['Detailed Description'].tolist()
        self.text = [i.lower() for i in text]

    def train_model(self):
        nlp = spacy.load("en_core_sci_sm")
        tok_text = []

        for doc in nlp.pipe(self.text, disable=["tagger", "parser", "ner", "lemmatizer"]):
            tok = [t.text for t in doc if (t.is_ascii and not t.is_punct and not t.is_space)]
            tok_text.append(tok)

        ft_model = FastText(
            sg=1,  # use skip-gram: usually gives better results
            vector_size=100,  # embedding dimension (default)
            window=10,  # window size: 10 tokens before and 10 tokens after to get wider context
            min_count=1,  # only consider tokens with at least n occurrences in the corpus
            negative=15,  # negative subsampling: bigger than default to sample negative examples more
            min_n=2,  # min character n-gram
            max_n=5  # max character n-gram
        )

        ft_model.build_vocab(tok_text)

        ft_model.train(
            tok_text,
            epochs=6,
            total_examples=ft_model.corpus_count,
            total_words=ft_model.corpus_total_words)

        ft_model.save('_fasttext.model')

        data = pd.DataFrame(ft_model.wv.most_similar("anti-cancer", topn=10, restrict_vocab=5000),
                            columns=['Word', 'Score'])
        print(data)

        bm25 = BM25Okapi(tok_text)
        weighted_doc_vects = []

        for i, doc in enumerate(tok_text):
            doc_vector = []
            for word in doc:
                vector = ft_model.wv[word]
                # note for newer versions of fasttext you may need to replace ft_model[word] with ft_model.wv[word]
                weight = (bm25.idf[word] * ((bm25.k1 + 1.0) * bm25.doc_freqs[i][word])) / (
                        bm25.k1 * (1.0 - bm25.b + bm25.b * (bm25.doc_len[i] / bm25.avgdl)) + bm25.doc_freqs[i][word])
                weighted_vector = vector * weight
                doc_vector.append(weighted_vector)
            doc_vector_mean = np.mean(doc_vector, axis=0)
            weighted_doc_vects.append(doc_vector_mean)

        pickle.dump(weighted_doc_vects, open("weighted_doc_vects.p", "wb"))

    def search(self, query):
        tokenized_query = query.lower().split(" ")

        results = bm25.get_top_n(tokenized_query, self.text, n=3)
        for i in results:
            print(self.title[self.text.index(i)])
            print(i)
            print('\n')
