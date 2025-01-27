# -*- coding: utf-8 -*-

#
# Clase encargada de ejecutar los algoritmos de similitud 
#

import spacy
import math
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

STR_SIMILITUD_COSENO_SPACY = "SIMILITUD_COSENO_SPACY"
STR_SIMILITUD_COSENO_SPACY_FRANJASHORARIAS = "SIMILITUD_COSENO_SPACY_FH"
STR_SIMILITUD_JACCARD = "SIMILITUD_JACCARD"
STR_SIMILITUD_JACCARD_FRANJASHORARIAS = "SIMILITUD_JACCARD_FH"
STR_SIMILITUD_COSENO_TFIFD = "SIMILITUD_COSENO_TF-IDF"
STR_SIMILITUD_COSENO_BOW = "SIMILITUD_COSENO_BOW"
LIST_SIMILITUDES_ACEPTADAS = [  STR_SIMILITUD_COSENO_SPACY,
                                STR_SIMILITUD_COSENO_SPACY_FRANJASHORARIAS,
                                STR_SIMILITUD_JACCARD,
                                STR_SIMILITUD_JACCARD_FRANJASHORARIAS,
                                STR_SIMILITUD_COSENO_TFIFD,
                                STR_SIMILITUD_COSENO_BOW]

class Similitud():

    def __init__(self, nombreSimilitud):

        if nombreSimilitud not in LIST_SIMILITUDES_ACEPTADAS:
            return None

        self.nombreSimilitud = nombreSimilitud

        if self.nombreSimilitud == STR_SIMILITUD_COSENO_SPACY or self.nombreSimilitud == STR_SIMILITUD_COSENO_SPACY_FRANJASHORARIAS:
            self.funcionSimilitud = self.similitud_coseno_spacy
        
        elif self.nombreSimilitud == STR_SIMILITUD_JACCARD or self.nombreSimilitud == STR_SIMILITUD_JACCARD_FRANJASHORARIAS:
            self.funcionSimilitud = self.similitud_jaccard

        elif self.nombreSimilitud == STR_SIMILITUD_COSENO_TFIFD:
            self.funcionSimilitud = self.similitud_coseno_links
            self.dicc_doc_wFrec = {}    # Diccionario => Documento: { Palabra_n: frecuencia en documento }
            self.dicc_w_docsConW = {}   # Diccionario => Palabra: frecuencia en el dataset 
            self.dicc_doc_vector = {}   # Diccionario => Documento: Matriz Numpy

        elif self.nombreSimilitud == STR_SIMILITUD_COSENO_BOW:
            self.funcionSimilitud = self.similitud_coseno_links
            self.dicc_doc_wFrec = {}
            self.list_words = []
            self.dicc_doc_vector = {}

    # Sección de cálculo de similitud coseno con representación vectorial de Spacy (Word2Vec)

    def similitud_coseno_spacy(self, doc1, doc2, redondeo=5):

        # Comprobamos que no haya vectores o estén a 0
        if doc1.has_vector == False or doc2.has_vector == False:
            return 0
        elif doc1.vector_norm == 0 or doc2.vector_norm == 0:
            return 0

        return round(doc1.similarity(doc2), redondeo)


    # Sección de cálculo de similitud Jaccard

    def similitud_jaccard(self, doc1, doc2, redondeo=5):
        
        s1 = self.getSetPalabras(doc1)
        s2 = self.getSetPalabras(doc2)

        elemsInterseccion = len(s1 & s2)
        elemsUnion = len(s1 | s2)

        return elemsInterseccion / elemsUnion

    
    # Sección de calculo de similitud coseno, para todas las similitudes que utilicen vectores

    def similitud_coseno_links(self, linkMaster, linkAnalizar, redondeo=5):
        
        vector_Master = self.dicc_doc_vector[linkMaster].reshape(1, -1)
        vector_Analizar = self.dicc_doc_vector[linkAnalizar].reshape(1, -1)

        return round(cosine_similarity(vector_Master, vector_Analizar)[0][0], redondeo)


    def similitud_coseno_vecs(self, vector_Master, vector_Analizar, redondeo=5):
        
        vector_Master = vector_Master.reshape(1, -1)
        vector_Analizar = vector_Analizar.reshape(1, -1)

        return round(cosine_similarity(vector_Master, vector_Analizar)[0][0], redondeo)


    # Sección de cálculo de similitud coseno con representación vectorial de tf-idf

    def add_doc_wFrec_entry(self, linkNoticia, doc):

        self.dicc_doc_wFrec[linkNoticia] = {}

        for word in doc:

            if word.text not in self.dicc_doc_wFrec[linkNoticia]:
                self.dicc_doc_wFrec[linkNoticia][word.text] = 0
                self.add_w_docsConW_entry(word.text)

            self.dicc_doc_wFrec[linkNoticia][word.text] += 1


    def add_w_docsConW_entry(self, word):

        if word not in self.dicc_w_docsConW:
            self.dicc_w_docsConW[word] = 0
        
        self.dicc_w_docsConW[word] += 1


    def create_dicc_doc_tfidf(self):

        numDocs = len(self.dicc_doc_wFrec)

        for linkNoticia in self.dicc_doc_wFrec:

            self.dicc_doc_vector[linkNoticia] = []
            for word in self.dicc_w_docsConW:

                if word not in self.dicc_doc_wFrec[linkNoticia]:
                    self.dicc_doc_vector[linkNoticia].append(0)
                    continue

                frecWordEnDoc = self.dicc_doc_wFrec[linkNoticia][word]
                frecWordEnDataset = self.dicc_w_docsConW[word]

                tf = 1 + math.log(frecWordEnDoc, 2)
                idf = (numDocs + 1) / (frecWordEnDataset + 0.5) 
                self.dicc_doc_vector[linkNoticia].append(tf * idf)

            self.dicc_doc_vector[linkNoticia] = np.array(self.dicc_doc_vector[linkNoticia])


    # Sección de cálculo de similitud coseno con representación vectorial creada por Bag of Words (BoW)

    # Función igual que "add_doc_wFrec_entry" pero sin la llamada a "add_w_docsConW_entry"
    # para evitar perder tiempo con condiciones a la hora de hacer las pruebas 
    # de velocidad
    def add_doc_wFrec_entry_BoW(self, linkNoticia, doc):

        self.dicc_doc_wFrec[linkNoticia] = {}

        for word in doc:

            if word.text not in self.list_words:
                self.list_words.append(word.text)

            if word.text not in self.dicc_doc_wFrec[linkNoticia]:
                self.dicc_doc_wFrec[linkNoticia][word.text] = 0

            self.dicc_doc_wFrec[linkNoticia][word.text] += 1


    def create_vec_doc_BoW(self):

        for linkNoticia in self.dicc_doc_wFrec:

            self.dicc_doc_vector[linkNoticia] = []
            for word in self.list_words:

                if word not in self.dicc_doc_wFrec[linkNoticia]:
                    self.dicc_doc_vector[linkNoticia].append(0)
                else:
                    self.dicc_doc_vector[linkNoticia].append(self.dicc_doc_wFrec[linkNoticia][word])

            self.dicc_doc_vector[linkNoticia] = np.array(self.dicc_doc_vector[linkNoticia])


    # Sección de acceso a variables de la clase

    def getNombreSimilitud(self):

        return self.nombreSimilitud


    def getFuncionSimilitud(self):

        return self.funcionSimilitud


    def getSetPalabras(self, doc):

        return set(map(lambda token: token.text, doc))


    def getLinksNoticias(self):

        return self.dicc_doc_wFrec.keys()


    def getDocVector(self, linkNoticia):

        return self.dicc_doc_vector[linkNoticia]