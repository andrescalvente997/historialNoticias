# -*- coding: utf-8 -*-

#
# Clase encargada de ejecutar los algoritmos de similitud 
#

import spacy


STR_SIMILITUD_COSENO_SPACY = "SIMILITUD_COSENO_SPACY"
STR_SIMILITUD_JACCARD = "SIMILITUD_JACCARD"
STR_SIMILITUD_COSENO_TFIFD = "SIMILITUD_COSENO_TF-IDF"
LIST_SIMILITUDES_ACEPTADAS = [  STR_SIMILITUD_COSENO_SPACY,
                                STR_SIMILITUD_JACCARD,
                                STR_SIMILITUD_COSENO_TFIFD]

class Similitud():

    def __init__(self, nombreSimilitud):

        if nombreSimilitud not in LIST_SIMILITUDES_ACEPTADAS:
            return None

        self.nombreSimilitud = nombreSimilitud

        if self.nombreSimilitud == STR_SIMILITUD_COSENO_SPACY:
            self.funcionSimilitud = self.similitud_spacy
        
        elif self.nombreSimilitud == STR_SIMILITUD_JACCARD:
            self.funcionSimilitud = self.similitud_jaccard

        elif self.nombreSimilitud == STR_SIMILITUD_COSENO_TFIFD:
            self.funcionSimilitud = self.similitud_tfidf
            self.dicc_doc_wFrec = {}    # Diccionario => Documento: { Palabra_n: frecuencia en documento }
            self.dicc_w_docsConW = {}   # Diccionario => Palabra: frecuencia en el dataset 
            self.dicc_doc_tfidf = {}    # Diccionario => Documento: { Palabra_n: tf-idf }


    def similitud_spacy(self, doc1, doc2, redondeo=5):

        return round(doc1.similarity(doc2), redondeo)


    def similitud_jaccard(self, doc1, doc2, redondeo=5):
        
        s1 = self.getSetPalabras(doc1)
        s2 = self.getSetPalabras(doc2)

        elemsInterseccion = len(s1 & s2)
        elemsUnion = len(s1 | s2)

        return elemsInterseccion / elemsUnion


    def similitud_tfidf(self, doc1, doc2, redondeo=5):
        pass


    def add_doc_wFrec_entry(self, linkNoticia, doc):

        self.dicc_doc_wFrec[linkNoticia] = {}

        for word in doc:

            if word not in self.dicc_doc_wFrec[linkNoticia]:
                self.dicc_doc_wFrec[linkNoticia][word] = 0
                self.add_w_docsConW_entry(word)

            self.dicc_doc_wFrec[linkNoticia][word] += 1


    def add_w_docsConW_entry(self, word):

        if word not in self.dicc_w_docsConW:
            self.dicc_w_docsConW[word] = 0
        
        self.dicc_w_docsConW[word] += 1


    def getNombreSimilitud(self):

        return self.nombreSimilitud


    def getFuncionSimilitud(self):

        return self.funcionSimilitud


    def getSetPalabras(self, doc):

        return set(map(lambda token: token.text, doc))