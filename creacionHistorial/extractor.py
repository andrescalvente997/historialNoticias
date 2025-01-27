# -*- coding: utf-8 -*-

#
# Clase encargada de extraer y tratar la información sacada de los periódicos
#

import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from datetime import datetime, timedelta
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

        try:
            strFechas = fileStr.split("/")[-1]
            strFechaIni, strFechaFin = strFechas.split("_")[0], strFechas.split("_")[1]
            strFechaIni = strFechaIni[0:4] + "-" + strFechaIni[4:6] + "-" + strFechaIni[6:]
            strFechaFin = strFechaFin[0:4] + "-" + strFechaFin[4:6] + "-" + strFechaFin[6:] 
            self.fechaIni = datetime.strptime(strFechaIni, '%Y-%m-%d')
            self.fechaFin = datetime.strptime(strFechaFin, '%Y-%m-%d')
        except:
            self.fechaIni = datetime.strptime("2019-01-30", '%Y-%m-%d')
            self.fechaFin = datetime.strptime("2020-03-20", '%Y-%m-%d')

        self.jsonFile, dataNoticias = self.openFile(fileStr)

        #
        # El diccionario de noticias etiquetadas tendrá la siguiente estructura
        #
        #   { 
        #       "TEMA_1": [noticia_1, noticia_2, ...],
        #       "TEMA_2": [noticia_4, noticia_7, ...]
        #   } 
        self.diccNoticiaEtiq = {}   

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
            
            if "temaNoticia" in noticia:
                if noticia["temaNoticia"] not in self.diccNoticiaEtiq:
                    self.diccNoticiaEtiq[noticia["temaNoticia"]] = []
                self.diccNoticiaEtiq[noticia["temaNoticia"]].append(linkNoticia)

        return diccs_DiccsNoticias


    def getDataNoticiaMaster(self):

        return self.dataNoticiaMaster


    def getLinkNoticiaMaster(self):

        return self.linkNoticiaMaster


    def getDiccNoticiaEtiqueta(self):

        return self.diccNoticiaEtiq


    def getEtiquetasTema(self):

        return list(self.diccNoticiaEtiq.keys())


    def getCountNoticiasConEtiqueta(self, tema):

        return len(self.diccNoticiaEtiq[tema])


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

        return atributoDoc.text


    def create_diccRangoFechaNoticas(self):

        dicc_rangoFecha_Noticias = {}

        acc_datetime = self.fechaFin
        acc_datetime = acc_datetime + timedelta(hours=23, minutes=59, seconds=59)
        while self.fechaIni <= acc_datetime:

            dupFecha = (acc_datetime - timedelta(hours=3, minutes=59, seconds=59), acc_datetime)
            dicc_rangoFecha_Noticias[dupFecha] = []
            acc_datetime -= timedelta(hours=4)

        for linkNoticia in self.dd_Noticias.keys():

            fechaNoticia = self.dd_Noticias[linkNoticia]['fechaPublicacionNoticia']
            fechaNoticia = datetime.strptime(fechaNoticia, '%Y-%m-%dT%H:%M:%SZ')
            for franjaHoraria in dicc_rangoFecha_Noticias.keys():

                if franjaHoraria[0] < fechaNoticia and fechaNoticia <= franjaHoraria[1]:
                    
                    dicc_rangoFecha_Noticias[franjaHoraria].append(linkNoticia)

        return dicc_rangoFecha_Noticias


    # Función que pasado la data de una noticia y un atributo, nos devuelve 
    # su vector de caracteristicas de Spacy
    def getVectorAtributo(self, data, atributo, flgTratar=True):

        atributoDoc = self.getAtributoNoticia(data, atributo, flgTratar=flgTratar)

        if atributoDoc != "":
            return atributoDoc.vector
        else:
            return self.nlp("").vector
    #
    # Procesamiento de textos
    #

    def getDoc(self, text):

        return self.nlp(text)


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