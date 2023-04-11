import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import json
import random
import pickle

stemmer = LancasterStemmer()

with open("Python script/json file/intents.json") as file:
    data = json.load(file)

try:
    with open("Python script/list_data" , "rb") as f:
        words , labels , training , output = f
except:
    words = []
    labels = []
    document_tokens = []
    document_labels = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            document_tokens.append(wrds)
            document_labels.append(intent["tag"])


        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    empty_output_list = [0 for _ in range(len(labels))]

    for x, doc in enumerate(document_tokens):
        document_bag = []
        pattern_words = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in pattern_words:
                document_bag.append(1)
            else:
                document_bag.append(0)

        output_row = empty_output_list[:]
        output_row[labels.index(document_labels[x])] = 1

        training.append(document_bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("Python script/list_data" , "wb") as f:
        pickle.dump((words , labels , training , output) , f)


net = tflearn.input_data(shape = [None, len(training[0]) ])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("Python script/model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("Python script/model.tflearn")

def bag_of_words(input_sentence, words):
    bag = [0 for _ in range(len(words))]
    sen_words = nltk.word_tokenize(input_sentence)
    sen_words = [stemmer.stem(word.lower()) for word in sen_words]

    for i in sen_words:
        for j, w in enumerate(words):
            if w == i:
                bag[j] = 1
 
    return np.array(bag)

    

def getResponse(prompt):
    result = model.predict([bag_of_words(prompt, words)])
    print(np.max(result))
    if np.max(result) < 0.60:
        return "I'm sorry. I don't understand what you mean.<br> Can you please rephrase your sentence?"
    result_index = np.argmax(result)
    tag = labels[result_index]

    for tg in data['intents']:
        if tg['tag'] == tag:
            response = tg['responses']

    return random.choice(response)
        
    