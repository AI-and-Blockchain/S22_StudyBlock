import pandas as pd
import pickle
import spacy
import scispacy
from rank_bm25 import BM25Okapi


class Model:
    def __init__(self):
        self.csv_name = 'models/trialdata.csv'

        docs = pd.read_csv(self.csv_name)
        self.title = docs['Study'].tolist()
        self.text = docs['Detailed Description'].tolist()
        self.owner = docs['Owner'].tolist()
        self.text = [i.lower() for i in self.text]
        self.docs = pd.DataFrame({"Study": self.title, "Detailed Description": self.text})

    def train_model(self):
        nlp = spacy.load("en_core_sci_sm")

        tok_text = []
        for doc in nlp.pipe(self.text, disable=["tagger", "parser", "ner", "lemmatizer"]):
            tok = [t.text for t in doc if (t.is_ascii and not t.is_punct and not t.is_space)]
            tok_text.append(tok)

        bm25 = BM25Okapi(tok_text)
        with open('models/bm25result', 'wb') as bm25result_file:
            pickle.dump(bm25, bm25result_file)

    def add_trial(self, title, description, address):
        self.title.append(title)
        self.text.append(description.lower())
        self.owner.append(address)

        self.docs = pd.DataFrame({"Study": self.title, "Detailed Description": self.text, "Owner": self.owner})

        self.docs.to_csv(self.csv_name)

        tok_text = []
        nlp = spacy.load("en_core_sci_sm")
        for doc in nlp.pipe(self.text, disable=["tagger", "parser", "ner", "lemmatizer"]):
            tok = [t.text for t in doc if (t.is_ascii and not t.is_punct and not t.is_space)]
            tok_text.append(tok)

        bm25 = BM25Okapi(tok_text)
        with open('models/bm25result', 'wb') as bm25result_file:
            pickle.dump(bm25, bm25result_file)

    def search(self, query):
        search_results = []
        tokenized_query = query.lower().split(" ")

        with open('models/bm25result', 'rb') as bm25result_file:
            bm25result = pickle.load(bm25result_file)
            results = bm25result.get_top_n(tokenized_query, self.text, n=3)
            for i in results:
                sr = '%s, Owner Address: %s' % (self.title[self.text.index(i)], self.owner[self.text.index(i)])
                search_results.append(sr)

            return search_results
