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
                    "tagsNoticia",
                    "cuerpoNoticia"]
LISTA_SIMILITUDES = [   "SIMILITUD_COSENO_SPACY",
                        "SIMILITUD_JACCARD",
                        "SIMILITUD_COSENO_TF-IDF",
                        "SIMILITUD_COSENO_BOW"]
LISTA_SIMILITUDES_t1 = ["SIMILITUD_COSENO_SPACY",
                        "SIMILITUD_JACCARD"]
LISTA_SIMILITUDES_t2 = ["SIMILITUD_COSENO_TF-IDF",
                        "SIMILITUD_COSENO_BOW"]
TOP_RESULTS_1 = 100
TOP_RESULTS_2 = 50
URL_NOTICIA_ANALIZAR = "https://elpais.com/sociedad/2020/02/01/actualidad/1580569994_549942.html"
NOTICIA_FILEPATH = dirname(abspath(__file__)) + "/" + "../crawler/crawlerPeriodicos/datos_EL_PAIS/20200125_20200202_noticias_etiquetadas.json"


def do_similitud(extractor_obj, similitud_obj, atributoEstudio, topResults, listLinksNoticias=None):

    procesador_obj = procesador.Procesador(similitud_obj.getNombreSimilitud())
    funct_similitud = similitud_obj.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = extractor_obj.getDataNoticiaMaster()
    atributoNoticia_Master = extractor_obj.getAtributoNoticia(dataNoticia_Master, atributoEstudio)

    if listLinksNoticias == None:
        listLinksNoticias = extractor_obj.getLinksNoticiasAnalizar()
    for linkNoticia in listLinksNoticias:
        
        dataNoticia_Analizar = extractor_obj.getDataNoticia(linkNoticia)
        if dataNoticia_Analizar == None:    # Noticia con fecha posterior a la Master
            continue
        
        atributoNoticia_Analizar = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, atributoEstudio)
        if atributoNoticia_Analizar == None:    # Atributo vacio
            continue

        score = funct_similitud(atributoNoticia_Master, atributoNoticia_Analizar)
        procesador_obj.addResultado(linkNoticia, score)

    time_end = time.time()

    noticiasEtiquetadas = extractor_obj.getDiccNoticiaEtiqueta()
    
    diccResults = printResult(procesador_obj, round(time_end - time_start), atributoEstudio, topResults, noticiasEtiquetadas)

    return diccResults


def do_similitud_creacionVectores(  extractor_obj, 
                                    similitud_obj, 
                                    atributoEstudio,
                                    topResults, 
                                    funct_addEntry, 
                                    funct_createVecs, 
                                    listLinksNoticias=None):
    
    procesador_obj = procesador.Procesador(similitud_obj.getNombreSimilitud())
    funct_similitud = similitud_obj.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = extractor_obj.getDataNoticiaMaster()
    atributoNoticia_Master = extractor_obj.getAtributoNoticia(dataNoticia_Master, atributoEstudio)
    linkNoticia_Master = extractor_obj.getLinkNoticiaMaster()
    funct_addEntry(linkNoticia_Master, atributoNoticia_Master)

    if listLinksNoticias == None:
        listLinksNoticias = extractor_obj.getLinksNoticiasAnalizar()
    for linkNoticia in listLinksNoticias:
        
        dataNoticia_Analizar = extractor_obj.getDataNoticia(linkNoticia)
        if dataNoticia_Analizar == None:    # Noticia con fecha posterior a la Master
            continue

        atributoNoticia_Analizar = extractor_obj.getAtributoNoticia(dataNoticia_Analizar, atributoEstudio)
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

    noticiasEtiquetadas = extractor_obj.getDiccNoticiaEtiqueta()
    
    diccResults = printResult(procesador_obj, round(time_end - time_start), atributoEstudio, topResults, noticiasEtiquetadas)

    return diccResults


def printResult(procesador_obj, executionTime, atributoUtilizado, topResults, noticiasEtiquetadas):

    procesador_obj.sortResultados()
    diccResults, strResultTop = procesador_obj.getTopResultados(noticiasEtiquetadas, top=topResults)
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

    return diccResults


if __name__ == '__main__':

    '''
    extractor_obj = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)
    # Realizamos al primer filtrado de resultados
    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_SPACY")
    diccResults = do_similitud( extractor_obj, 
                                similitud_obj,
                                ATRIBUTO_ESTUDIO_1,
                                TOP_RESULTS_1)
                                
    # Obtenemos los links que han quedado en el top, no nos importa su posición anterior
    linksTopAnalizar = diccResults.keys()
    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_SPACY")
    diccResults = do_similitud( extractor_obj, 
                                similitud_obj,
                                ATRIBUTO_ESTUDIO_2,
                                TOP_RESULTS_1,
                                listLinksNoticias=linksTopAnalizar)


    similitud_obj = similitud.Similitud("SIMILITUD_JACCARD")
    diccResults = do_similitud( extractor_obj, 
                                similitud_obj,
                                ATRIBUTO_ESTUDIO_1,
                                TOP_RESULTS_1)


    similitud_obj = similitud.Similitud("SIMILITUD_JACCARD")
    diccResults = do_similitud( extractor_obj, 
                                similitud_obj,
                                ATRIBUTO_ESTUDIO_2,
                                TOP_RESULTS_1,
                                listLinksNoticias=linksTopAnalizar)
    
    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_TF-IDF")
    diccResults = do_similitud_creacionVectores(extractor_obj, 
                                                similitud_obj, 
                                                ATRIBUTO_ESTUDIO_1,
                                                TOP_RESULTS_1,
                                                similitud_obj.add_doc_wFrec_entry, 
                                                similitud_obj.create_dicc_doc_tfidf)
    
    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_TF-IDF")
    diccResults = do_similitud_creacionVectores(extractor_obj, 
                                                similitud_obj, 
                                                ATRIBUTO_ESTUDIO_2,
                                                TOP_RESULTS_1,
                                                similitud_obj.add_doc_wFrec_entry, 
                                                similitud_obj.create_dicc_doc_tfidf,
                                                listLinksNoticias=linksTopAnalizar)

    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_BOW")
    diccResults = do_similitud_creacionVectores(extractor_obj, 
                                                similitud_obj,  
                                                ATRIBUTO_ESTUDIO_1,
                                                TOP_RESULTS_1,
                                                similitud_obj.add_doc_wFrec_entry_BoW, 
                                                similitud_obj.create_vec_doc_BoW)

    similitud_obj = similitud.Similitud("SIMILITUD_COSENO_BOW")
    diccResults = do_similitud_creacionVectores(extractor_obj, 
                                                similitud_obj,  
                                                ATRIBUTO_ESTUDIO_2,
                                                TOP_RESULTS_1,
                                                similitud_obj.add_doc_wFrec_entry_BoW, 
                                                similitud_obj.create_vec_doc_BoW,
                                                listLinksNoticias=linksTopAnalizar)
    '''
    
    extractor_obj = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)

    for sim1 in LISTA_SIMILITUDES:
        similitud_obj = similitud.Similitud(sim1)

        for atri1 in LISTA_ATRIBUTOS:

            if sim1 in LISTA_SIMILITUDES_t1:
                diccResults = do_similitud( extractor_obj, 
                                            similitud_obj,
                                            atri1,
                                            TOP_RESULTS_1)
            else:

                if sim1 == "SIMILITUD_COSENO_TF-IDF":
                    fuctAddEntry = similitud_obj.add_doc_wFrec_entry
                    functCreateVecs = similitud_obj.create_dicc_doc_tfidf
                elif sim1 == "SIMILITUD_COSENO_BOW":
                    fuctAddEntry = similitud_obj.add_doc_wFrec_entry_BoW
                    functCreateVecs = similitud_obj.create_vec_doc_BoW

                diccResults = do_similitud_creacionVectores(extractor_obj, 
                                                            similitud_obj,  
                                                            atri1,
                                                            TOP_RESULTS_1,
                                                            fuctAddEntry, 
                                                            functCreateVecs)

                            
    extractor_obj.closeFile()