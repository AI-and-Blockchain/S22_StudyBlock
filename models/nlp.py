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
        self.title = self.docs['Study'].tolist()
        self.text = self.docs['Detailed Description'].tolist()
        self.text = [i.lower() for i in self.text]

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

        self.bm25 = BM25Okapi(tok_text)


    def search(self, query):
        tokenized_query = query.lower().split(" ")

        results = self.bm25.get_top_n(tokenized_query, self.text, n=3)
        for i in results:
            print(self.title[self.text.index(i)])
            print(i)
            print('\n')
