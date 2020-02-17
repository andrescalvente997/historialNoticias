# -*- coding: utf-8 -*-

#
# Clase encargada de ejecutar los algoritmos de similitud 
#

import spacy

class Similitud():

    def __init__(self):
        pass

    
    def similitud_spacy(self, doc1, doc2, redondeo=5):

        return round(doc1.similarity(doc2), redondeo)


    def similitud_jaccard(self, doc1, doc2, redondeo=5):
        
        s1 = set(map(lambda token: token.text, doc1))
        s2 = set(map(lambda token: token.text, doc2))

        elemsInterseccion = len(s1 & s2)
        elemsUnion = len(s1 | s2)

        return elemsInterseccion / elemsUnion