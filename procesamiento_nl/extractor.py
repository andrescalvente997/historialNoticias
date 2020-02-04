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

    def __init__(self, fileStr):

        self.nlp = spacy.load("es_core_news_md")
    
        self.fileStr = fileStr
        self.jsonFile, self.data = self.openFile()

        aux_regex = r'\b'
        aux_regex += r'\b|\b'.join(STOP_WORDS)
        aux_regex += r'\b'
        self.regex_stopwords = re.compile('%s' % aux_regex)


    def openFile(self):

        file = open(self.fileStr, 'r')
        return file, json.loads(file)


    def closeFile(self):

        self.jsonFile.close()

    
    def rm_stopWords(self, doc):

        return nlp(self.regex_stopwords.sub('\b', doc.text).strip())


    def rm_punctuation(self, doc):

        return nlp(REGEX_PUNCTUATION.sub('\b', doc.text).strip())
