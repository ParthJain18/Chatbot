import nltk
from nltk.stem.lancaster import LancasterStemmer
Stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import json
import random


with open("json file/intents.json") as file:
    data = json.load(file)


words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(pattern)
        docs_y.append(intent["tag"])


    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [Stemmer.stem(w.lower()) for w in words]

