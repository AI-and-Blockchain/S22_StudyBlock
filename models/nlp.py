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
        self.csv_name = csv

        docs = pd.read_csv(csv)
        self.title = docs['Study'].tolist()
        self.text = docs['Detailed Description'].tolist()
        self.text = [i.lower() for i in self.text]
        self.docs = pd.DataFrame({"Study": self.title, "Detailed Description": self.text})

    def train_model(self):
        nlp = spacy.load("en_core_sci_sm")

        tok_text = []
        for doc in nlp.pipe(self.text, disable=["tagger", "parser", "ner", "lemmatizer"]):
            tok = [t.text for t in doc if (t.is_ascii and not t.is_punct and not t.is_space)]
            tok_text.append(tok)

        bm25 = BM25Okapi(tok_text)
        with open('bm25result', 'wb') as bm25result_file:
            pickle.dump(bm25, bm25result_file)

    def add_trial(self, title, description):
        self.title.append(title)
        self.text.append(description.lower())

        self.docs = pd.DataFrame({"Study": self.title, "Detailed Description": self.text})

        self.docs.to_csv(self.csv_name)

        tok_text = []
        nlp = spacy.load("en_core_sci_sm")
        for doc in nlp.pipe(self.text, disable=["tagger", "parser", "ner", "lemmatizer"]):
            tok = [t.text for t in doc if (t.is_ascii and not t.is_punct and not t.is_space)]
            tok_text.append(tok)

        bm25 = BM25Okapi(tok_text)
        with open('bm25result', 'wb') as bm25result_file:
            pickle.dump(bm25, bm25result_file)

    def search(self, query):
        tokenized_query = query.lower().split(" ")

        with open('bm25result', 'rb') as bm25result_file:
            bm25result = pickle.load(bm25result_file)
            results = bm25result.get_top_n(tokenized_query, self.text, n=3)
            for i in results:
                print(self.title[self.text.index(i)])
                print(i)
                print('\n')
