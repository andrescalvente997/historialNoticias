import spacy
from sklearn import metrics
import nltk
from nltk.corpus import stopwords as stopW
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def trataStrings(strr):

    stopwords = stopW.words('spanish')

    regex_pun = re.compile('[%s]' % re.escape(string.punctuation))
    regex_espacios = re.compile('\s\s+')

    strr = regex_pun.sub(' ', strr).strip()
    strr = regex_espacios.sub(' ', strr).strip()

    lst = strr.split(" ")
    lst = [word for word in lst if word.lower() not in stopwords]

    return " ".join(lst)

if __name__ == '__main__':

    # Definimos dos string de test
    strr1 = "Casi 20.000 euros al año. Esa el la cifra que el gobierno pide."
    strr2 = "El Gobierno de Pedro Sánchez y Pablo Iglesias quiere una cifra de muchos euros."
    strr3 = "El gato de San Roque no tiene nabo, porque Ramón Ramirez se lo ha depilado."
    strr4 = "La perra de San Pedro no tiene rabo, porque Iglesias Ramirez se lo ha cortado."

    # Eliminamos los signos de puntución de las dos cadenas
    strr1 = trataStrings(strr1)
    strr2 = trataStrings(strr2)
    strr3 = trataStrings(strr3)
    strr4 = trataStrings(strr4)
    corpus = []
    corpus.append(strr1)
    corpus.append(strr2)
    corpus.append(strr3)
    corpus.append(strr4)
    
    print(corpus)

    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(corpus)
    pairwise_similarity = tfidf * tfidf.T
    arr = pairwise_similarity.toarray()
    print(arr)
    np.fill_diagonal(arr, np.nan)

    for i in range(4):
        print("\nDocumento: '{}'".format(corpus[i]))
        mejor_doc = np.nanargmax(arr[i])
        print("Se parece al documento ({}): '{}'".format(mejor_doc, corpus[mejor_doc]))