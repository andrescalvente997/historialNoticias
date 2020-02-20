# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import time
import math
import extractor
import similitud
import procesador

ATRIBUTO_ESTUDIO_1 = "cuerpoNoticia"
TOP_RESULTS = 100
URL_NOTICIA_ANALIZAR = "https://elpais.com/sociedad/2020/02/01/actualidad/1580569994_549942.html"
NOTICIA_FILEPATH = dirname(abspath(__file__)) + "/" + "../crawler/crawlerPeriodicos/datos_EL_PAIS/20200125_20200202_noticias.json"

def do_similitud(similitud_obj):

    extractor_obj = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)
    procesador_obj = procesador.Procesador(similitud_obj.getNombreSimilitud())
    funct_similitud = similitud_obj.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = extractor_obj.getNoticiaMaster()
    atributoNoticia_Master = extractor_obj.getAtributoNoticia(dataNoticia_Master, ATRIBUTO_ESTUDIO_1)
    dataNoticia_Analizar = extractor_obj.getNextNoticia()

    while dataNoticia_Analizar != -1:
        
        linkNoticia = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, "linkNoticia", flgTratar=False)
        atributoNoticia_Analizar = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, ATRIBUTO_ESTUDIO_1)

        if atributoNoticia_Analizar == None:
            #print(">> Noticia sin Atributo - " + strAtributo + ": " + linkNoticia)
            dataNoticia_Analizar = extractor_obj.getNextNoticia()
            continue

        score = funct_similitud(atributoNoticia_Master, atributoNoticia_Analizar)
        procesador_obj.addResultado(linkNoticia, score)

        dataNoticia_Analizar = extractor_obj.getNextNoticia()

    time_end = time.time()
    
    printResult(procesador_obj, round(time_end - time_start))

    return


def do_similitud_tfidf(similitud_obj):

    extractor_obj = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)
    procesador_obj = procesador.Procesador(similitud_obj.getNombreSimilitud())
    funct_similitud = similitud_obj.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = extractor_obj.getNoticiaMaster()
    atributoNoticia_Master = extractor_obj.getAtributoNoticia(dataNoticia_Master, ATRIBUTO_ESTUDIO_1)
    linkNoticia_Master = extractor_obj.getAtributoNoticia(dataNoticia_Master, "linkNoticia", flgTratar=False)
    similitud_obj.add_doc_wFrec_entry(linkNoticia_Master, atributoNoticia_Master)

    list_linksNoticiasAnalizar = []
    dataNoticia_Analizar = extractor_obj.getNextNoticia()

    while dataNoticia_Analizar != -1:
        
        linkNoticia_Analizar = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, "linkNoticia", flgTratar=False)
        list_linksNoticiasAnalizar.append(linkNoticia_Analizar)
        atributoNoticia_Analizar = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, ATRIBUTO_ESTUDIO_1)

        if atributoNoticia_Analizar == None:
            #print(">> Noticia sin Atributo - " + strAtributo + ": " + linkNoticia)
            dataNoticia_Analizar = extractor_obj.getNextNoticia()
            continue

        similitud_obj.add_doc_wFrec_entry(linkNoticia_Analizar, dataNoticia_Analizar)

    similitud_obj.create_dicc_doc_tfidf()

    for linkNoticia_Analizar in list_linksNoticiasAnalizar:

        score = funct_similitud(linkNoticia_Master, linkNoticia_Analizar)
        procesador_obj.addResultado(linkNoticia_Analizar, score)

    time_end = time.time()
    
    printResult(procesador_obj, round(time_end - time_start))

    return


def printResult(procesador_obj, executionTime):

    procesador_obj.sortResultados()
    _, strResultTop = procesador_obj.getTopResultados(top=TOP_RESULTS, flgPrintTop=True)
    mins = math.floor(executionTime / 60)
    segs = round((executionTime / 60 - mins) * 60)

    print("#########################################################\n")
    print(">> Resumen:")
    print("Estudiando el atributo '{}'".format(ATRIBUTO_ESTUDIO_1))
    print(procesador_obj)
    print(">> Top:")
    print(strResultTop)
    print(">> Tiempo de ejecución:")
    print("{} minutos y {} segundos.\n".format(str(mins), str(segs)))

    return


if __name__ == '__main__':

    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_SPACY")
    do_similitud(similitud_obj)

    similitud_obj = similitud.Similitud("SIMILITUD_JACCARD")
    do_similitud(similitud_obj)

    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_TF-IDF")
    do_similitud_tfidf(similitud_obj)

