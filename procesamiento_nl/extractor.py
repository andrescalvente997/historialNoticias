# -*- coding: utf-8 -*-

#
# Clase encargada de extraer y tratar la información sacada de los periódicos
#

import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import nltk
from nltk.corpus import stopwords
import re
import string
import json

REGEX_PUNCTUATIONS = re.compile('[%s]' % re.escape(string.punctuation + "“”—"))
REGEX_STOPWORDS = re.compile('%s' % r'\b' + r'\b|\b'.join(STOP_WORDS | set(stopwords.words('spanish'))) + r'\b')
REGEX_BLANKS = re.compile(r'\s\s+')

class Extractor():

    def __init__(self, fileStr, linkNoticiaMaster):

        self.nlp = spacy.load("es_core_news_md")

        self.jsonFile, dataNoticias = self.openFile(fileStr)

        # Utilizaremos un diccionario de diccionarios con la estructura: 
        #   {
        #       linkNoticia: {
        #           atributoNoticia_1: valorNoticia_1
        #           atributoNoticia_2: valorNoticia_2
        #           (...)
        #       }
        #   }
        # De está manera la obtención de links será más optima
        #
        self.dd_Noticias = self.createDiccExtractor(dataNoticias)

        self.dataNoticiaMaster = self.dd_Noticias[linkNoticiaMaster]
        del self.dd_Noticias[linkNoticiaMaster]
        self.linkNoticiaMaster = linkNoticiaMaster
    
    #
    # Busqueda de noticias
    #

    # Función que creará el diccionario de diccionarios en la aplicación
    def createDiccExtractor(self, dataNoticias):

        diccs_DiccsNoticias = {}

        for noticia in dataNoticias:
            linkNoticia = noticia['linkNoticia']
            diccNoticia = noticia
            del noticia['linkNoticia']
            diccs_DiccsNoticias[linkNoticia] = diccNoticia

        return diccs_DiccsNoticias


    def getDataNoticiaMaster(self):

        return self.dataNoticiaMaster


    def getLinkNoticiaMaster(self):

        return self.linkNoticiaMaster


    def getLinksNoticiasAnalizar(self):

        return self.dd_Noticias.keys()


    def getNumNoticiasAnalizar(self):

        return len(self.dd_Noticias)


    def getDataNoticia(self, linkNoticia):

        if self.dd_Noticias[linkNoticia]['fechaPublicacionNoticia'] > self.dataNoticiaMaster['fechaPublicacionNoticia']:
            return None
        else:
            return self.dd_Noticias[linkNoticia]  


    def getAtributoNoticia(self, data, atributo, flgTratar=True):

        atributoNoticia = data[atributo]

        if type(atributoNoticia) is list:
            atributoNoticia = " ".join(atributoNoticia)
        
        if flgTratar == False:
            return atributoNoticia

        atributoDoc = self.nlp(atributoNoticia)
        atributoDoc = self.do_lemmatize(atributoDoc)
        atributoDoc = self.rm_stopWords(atributoDoc)
        atributoDoc = self.rm_punctuations(atributoDoc)
        atributoDoc = self.rm_blanks(atributoDoc)

        if atributoDoc.text == "":
            return None

        return atributoDoc
    
    #
    # Procesamiento de textos
    #

    def do_lemmatize(self, doc):

        return self.nlp(" ".join(list(map(lambda token: token.lemma_, doc))))

    def rm_stopWords(self, doc):

        return self.nlp(REGEX_STOPWORDS.sub(' ', doc.text.lower()).strip())


    def rm_punctuations(self, doc):

        return self.nlp(REGEX_PUNCTUATIONS.sub(' ', doc.text).strip())


    def rm_blanks(self, doc):

        return self.nlp(REGEX_BLANKS.sub(' ', doc.text).strip())
    
    #
    # Manejo de ficheros
    #

    def openFile(self, fileStr):

        file = open(fileStr, 'r')
        return file, json.load(file)


    def closeFile(self):

        self.jsonFile.close()