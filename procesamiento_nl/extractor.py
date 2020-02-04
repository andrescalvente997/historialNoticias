# -*- coding: utf-8 -*-

#
# Clase encargada de extraer y tratar la información sacada de los periódicos
#

import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import re
import string
import json

REGEX_PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

class Extractor():

    def __init__(self, fileStr, linkNoticia):

        self.nlp = spacy.load("es_core_news_md")

        self.jsonFile, self.dataNoticias = self.openFile()

        aux_regex = r'\b'
        aux_regex += r'\b|\b'.join(STOP_WORDS)
        aux_regex += r'\b'
        self.regex_stopwords = re.compile('%s' % aux_regex)

        self.index = 0

        self.dataNoticiaMaster = self.searchNoticiaMaster(linkNoticia)


    def getNextNoticia(self):

        dataNextNoticia = self.dataNoticias[self.index]

        if dataNextNoticia['linkNoticia'] == self.linkNoticia:
            self.index += 1
            dataNextNoticia = self.dataNoticias[self.index]
        
        flgEnd = False
        while flgEnd != True:
            # Comparamos la fecha de las noticias
            if dataNextNoticia['fechaPublicacionNoticia'] > self.dataNoticiaMaster['fechaPublicacionNoticia'] 
                self.index += 1
                dataNextNoticia = self.dataNoticias[self.index]
            else:
                flgEnd = True

        self.index += 1

        return dataNextNoticia   

    def openFile(self, fileStr):

        file = open(fileStr, 'r')
        return file, json.loads(file)


    def closeFile(self):

        self.jsonFile.close()

    
    def searchNoticiaMaster(self, linkNoticia):

        for noticia in self.dataNoticias:
            if noticia['linkNoticia'] == linkNoticia:
                return noticia

    
    def rm_stopWords(self, doc):

        return nlp(self.regex_stopwords.sub('\b', doc.text).strip())


    def rm_punctuation(self, doc):

        return nlp(REGEX_PUNCTUATION.sub('\b', doc.text).strip())
