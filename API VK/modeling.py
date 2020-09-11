from pprint import pprint

import re
import numpy as np
import pandas as pd

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pymorphy2
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
import pymorphy2
from nltk.corpus import stopwords
from typing import List

# возьмем стоп-слова из библиотеки для обработки языка
stop_words = stopwords.words('russian')
stop_words.extend(['это', 'этот', 'так', 'такой', 'такая'])
# Создадим морфологический анализатор
analiser = pymorphy2.MorphAnalyzer()


def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def sent_to_words(sentences): # перевод предложения в список слов
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def get_lemmas(text):
    masresult = []
    for sentences in text:
        sent = []
        for sentence in sentences:
            sent.append(analiser.parse(sentence)[0].normal_form) # прошлись по предложениям и закинули в массив нормальные формы слов
        masresult.append(sent)
    return masresult


stop_words = stopwords.words('russian')
df = pd.read_csv("data.csv") # читаем даннные
data = df["0"].values.tolist() # берём посты
data = [re.sub('\S*@\S*\s?', '', str(sent)) for sent in data] # удаляем ссылки, теги, адреса
data = [re.sub('\s+', ' ', str(sent)) for sent in data] # удаляем ссылки, теги, адреса
data = [re.sub("\'", "", str(sent)) for sent in data] # удаляем ссылки, теги, адреса
data_words = list(sent_to_words(data)) # переводим текст в массив массивов слов
data_words = remove_stopwords(data_words) # удаляем стоп-слова
data_words = get_lemmas(data_words) # формирует нормальные формы
id2word = corpora.Dictionary(data_words) # шифровка слов с помощью индексов
texts = data_words
corpus = [id2word.doc2bow(text) for text in texts] # создаётся корпус слов
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=20, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True) # создаём и обучаем модел, работающую по принципу латентного размещения Дирехле
pprint(lda_model.print_topics()) # вывод тем
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word) # данные для визуализации
pyLDAvis.save_html(data=vis, fileobj="vis.html") # сохранение визуализации в html
