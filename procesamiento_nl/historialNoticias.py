# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import time
import math
import extractor
import similitud
import procesador

ATRIBUTO_ESTUDIO_1 = "cuerpoNoticia"
ATRIBUTO_ESTUDIO_2 = "keywordsNoticia"
LISTA_ATRIBUTOS = [ "titularNoticia",
                    "keywordsNoticia",
                    "resumenNoticia",
                    "autorNoticia",
                    "tagsNoticia"]  #,"cuerpoNoticia" 
LISTA_SIMILITUDES = [   "SIMILITUD_COSENO_SPACY", 
                        "SIMILITUD_JACCARD",
                        "SIMILITUD_COSENO_TF-IDF",
                        "SIMILITUD_COSENO_BOW"]
LISTA_SIMILITUDES_T1 = ["SIMILITUD_COSENO_SPACY"]
LISTA_SIMILITUDES_T2 = ["SIMILITUD_COSENO_TF-IDF",
                        "SIMILITUD_COSENO_BOW"]
LISTA_SIMILITUDES_T3 = ["SIMILITUD_JACCARD"]
TOP_RESULTS_1 = 100
TOP_RESULTS_2 = 50
URL_NOTICIA_ANALIZAR = "https://elpais.com/sociedad/2020/02/01/actualidad/1580569994_549942.html"
NOTICIA_FILEPATH = dirname(abspath(__file__)) + "/" + "../crawler/crawlerPeriodicos/datos_EL_PAIS/20200125_20200202_noticias_etiquetadas.json"

STR_FICHERO_OUT = "../res_historialNoticias_vectores_sumaSims.txt"
FILE_OUT = open(STR_FICHERO_OUT, 'w')


def do_results_unAtributo(  obj_extractor,
                            noticiasEtiquetadas):

    for sim in LISTA_SIMILITUDES:

        for atributo_1 in LISTA_ATRIBUTOS:

            obj_similitud_atri1 = similitud.Similitud(sim)

            
    

if __name__ == '__main__':
    
    obj_extractor = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)
    noticiasEtiquetadas = obj_extractor.getDiccNoticiaEtiqueta()

    do_results_unAtributo(  obj_extractor, 
                            noticiasEtiquetadas)

    

                
