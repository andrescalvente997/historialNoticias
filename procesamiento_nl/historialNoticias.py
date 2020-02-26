# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import time
import math
import extractor
import similitud
import procesador

ATRIBUTO_ESTUDIO_1 = "cuerpoNoticia"
ATRIBUTO_ESTUDIO_2 = "keywordsNoticia"
TOP_RESULTS_1 = 100
TOP_RESULTS_2 = 50
URL_NOTICIA_ANALIZAR = "https://elpais.com/sociedad/2020/02/01/actualidad/1580569994_549942.html"
NOTICIA_FILEPATH = dirname(abspath(__file__)) + "/" + "../crawler/crawlerPeriodicos/datos_EL_PAIS/20200125_20200202_noticias.json"


def do_similitud(extractor_obj, similitud_obj):

    procesador_obj = procesador.Procesador(similitud_obj.getNombreSimilitud())
    funct_similitud = similitud_obj.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = extractor_obj.getDataNoticiaMaster()
    atributoNoticia_Master = extractor_obj.getAtributoNoticia(dataNoticia_Master, ATRIBUTO_ESTUDIO_1)

    listLinksNoticias = extractor_obj.getLinksNoticiasAnalizar()
    for linkNoticia in listLinksNoticias:
        
        dataNoticia_Analizar = extractor_obj.getDataNoticia(linkNoticia)
        if dataNoticia_Analizar == None:    # Noticia con fecha posterior a la Master
            continue
        
        atributoNoticia_Analizar = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, ATRIBUTO_ESTUDIO_1)
        if atributoNoticia_Analizar == None:    # Atributo vacio
            continue

        score = funct_similitud(atributoNoticia_Master, atributoNoticia_Analizar)
        procesador_obj.addResultado(linkNoticia, score)

    time_end = time.time()
    
    listSetResults = printResult(procesador_obj, round(time_end - time_start), ATRIBUTO_ESTUDIO_1, TOP_RESULTS_1)

    return listSetResults


def do_similitud_creacionVectores(extractor_obj, similitud_obj, funct_addEntry, funct_createVecs):
    
    procesador_obj = procesador.Procesador(similitud_obj.getNombreSimilitud())
    funct_similitud = similitud_obj.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = extractor_obj.getDataNoticiaMaster()
    atributoNoticia_Master = extractor_obj.getAtributoNoticia(dataNoticia_Master, ATRIBUTO_ESTUDIO_1)
    linkNoticia_Master = extractor_obj.getLinkNoticiaMaster()
    funct_addEntry(linkNoticia_Master, atributoNoticia_Master)

    listLinksNoticias = extractor_obj.getLinksNoticiasAnalizar()
    for linkNoticia in listLinksNoticias:
        
        dataNoticia_Analizar = extractor_obj.getDataNoticia(linkNoticia)
        if dataNoticia_Analizar == None:    # Noticia con fecha posterior a la Master
            continue

        atributoNoticia_Analizar = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, ATRIBUTO_ESTUDIO_1)
        if atributoNoticia_Analizar == None:    # Atributo vacio
            continue

        funct_addEntry(linkNoticia, atributoNoticia_Analizar)

    funct_createVecs()

    list_linksNoticiasAnalizar = similitud_obj.getLinksNoticias()

    for linkNoticia_Analizar in list_linksNoticiasAnalizar:

        if linkNoticia_Master == linkNoticia_Analizar:  # Noticia a analizar es la noticia master
            continue

        score = funct_similitud(linkNoticia_Master, linkNoticia_Analizar)
        procesador_obj.addResultado(linkNoticia_Analizar, score)

    time_end = time.time()
    
    listSetResults = printResult(procesador_obj, round(time_end - time_start), ATRIBUTO_ESTUDIO_1, TOP_RESULTS_1)

    return listSetResults


def printResult(procesador_obj, executionTime, atributoUtilizado, topResults):

    procesador_obj.sortResultados()
    listSetResults, strResultTop = procesador_obj.getTopResultados(top=topResults)
    mins = math.floor(executionTime / 60)
    segs = round((executionTime / 60 - mins) * 60)

    strPrint = "#########################################################\n"
    strPrint += ">> Resumen: \n"
    strPrint += "Estudiando el atributo '{}' \n"
    strPrint += "{} \n"
    strPrint += ">> Top: \n"
    strPrint += "{} \n"
    strPrint += ">> Tiempo de ejecución: \n"
    strPrint += "{} minutos y {} segundos.\n"
    strPrint = strPrint.format( atributoUtilizado,
                                procesador_obj,
                                strResultTop,
                                str(mins),
                                str(segs))
    print(strPrint)

    return listSetResults


def do_similitud_2(similitud_obj, listSetTopResults):
    
    pass


if __name__ == '__main__':

    extractor_obj = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)

    # Realizamos al primer filtrado de resultados
    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_SPACY")
    listSetResults = do_similitud(  extractor_obj, 
                                    similitud_obj)


    # Con el top de resultados obtenido, aplicamos la similitud entre otro atributo

    similitud_obj = similitud.Similitud("SIMILITUD_JACCARD")
    do_similitud(   extractor_obj, 
                    similitud_obj)
    
    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_TF-IDF")
    do_similitud_creacionVectores(  extractor_obj, 
                                    similitud_obj, 
                                    similitud_obj.add_doc_wFrec_entry, 
                                    similitud_obj.create_dicc_doc_tfidf)

    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_BOW")
    do_similitud_creacionVectores(  extractor_obj, 
                                    similitud_obj, 
                                    similitud_obj.add_doc_wFrec_entry_BoW, 
                                    similitud_obj.create_vec_doc_BoW)

