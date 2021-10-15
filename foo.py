import numpy as np
import tensorflow as tf
import pandas as pd
from collections import Counter
import csv, re, pickle


import numpy as np
import sys
from sklearn.decomposition import PCA,KernelPCA
import gensim
import json
import re
import keras
import hazm



with open('./dataset.json') as f:
  data = f.read()
data = data.split("\n")
# data = json.loads(data[0])
print(len(data))
datas = [json.loads(obj) for obj in data[:100000]]
data_text = [data["Text"] for data in datas]


# TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub(r"[-()\"#/@;:<>{}=~|.?,a-z,A-Z,0-9]", ' ', str(text)).strip()
    tokens = []
    for token in text.split():
        tokens.append(token)
    return " ".join(tokens)

documents = [preprocess(_text).split() for _text in data_text] 


w2v_model = gensim.models.word2vec.Word2Vec(vector_size = 300, 
                                            window=7, 
                                            min_count=10, 
                                            workers=8)

w2v_model.build_vocab(documents)

words = w2v_model.wv.index_to_key
vocab_size = len(words)
print("Vocab size", vocab_size)


w2v_model.train(documents, total_examples=len(documents), epochs=8)
w2v_model.wv.most_similar("نفت")




model = keras.models.load_model("my.model")
_normalizer = hazm.Normalizer()


def amir(text):
    text_for_test = _normalizer.normalize(text)
    text_for_test_words = hazm.word_tokenize(text_for_test)
    x_text_for_test_words = np.zeros((1,20,300),dtype=keras.backend.floatx())
    for t in range(0,len(text_for_test_words)):
        if t >= 20:
            break
        if text_for_test_words[t] not in w2v_model.wv.index_to_key:
            continue
    
        x_text_for_test_words[0, t, :] = w2v_model.wv[text_for_test_words[t]]
        print(x_text_for_test_words.shape)
  # print(text_for_test_words)
    result = model.predict(x_text_for_test_words)
    pos_percent = str(int(result[0][1]*100))+" % "
    neg_percent = str(int(result[0][0]*100))+" % "
    return pos_percent,neg_percent


def print_amir():
    print("my name is amir")
    
    
def similar(text):
    return w2v_model.wv.most_similar(text)


# print(amir("امیر خوشحال است"))