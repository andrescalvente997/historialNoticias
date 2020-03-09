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


# Función que obtiene los vectores de los algoritmos de similitud (T1)
# Aquellos algoritmos de similitud donde los vectores son de características de documento
# y ya vienen previamente definidos
def get_vectores_algs_T1(   extractor_obj, 
                            similitud_obj, 
                            atributoEstudio, 
                            listLinksNoticias=None):
    
    dicc_noticiaVector = {}

    time_start = time.time()

    data_noticiaMaster = extractor_obj.getDataNoticiaMaster()
    vector_noticiaMaster = extractor_obj.getVectorAtributo(data_noticiaMaster, atributoEstudio)

    if listLinksNoticias == None:
        listLinksNoticias = extractor_obj.getLinksNoticiasAnalizar()

    for linkNoticia in listLinksNoticias:
        
        data_noticiaAnalizar = extractor_obj.getDataNoticia(linkNoticia)
        if data_noticiaAnalizar == None:    # Noticia con fecha posterior a la Master
            continue
        vector_noticiaAnalizar = extractor_obj.getVectorAtributo(data_noticiaAnalizar, atributoEstudio)

        dicc_noticiaVector[linkNoticia] = vector_noticiaAnalizar

    time_end = time.time()

    print_creacionVectores(similitud_obj.getNombreSimilitud(), len(dicc_noticiaVector), round(time_end - time_start))

    return vector_noticiaMaster, dicc_noticiaVector


# Función que obtiene los vectores de los algoritmos de similitud (T2)
# Aquellos algoritmos de similitud donde los vectores tienen que ser creados,
# ya sea calculando frecuencias u otras características
def get_vectores_algs_T2(   extractor_obj, 
                            similitud_obj, 
                            atributoEstudio, 
                            funct_addEntry, 
                            funct_createVecs, 
                            listLinksNoticias=None):
    
    dicc_noticiaVector = {}

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

    vector_noticiaMaster = similitud_obj.getDocVector(linkNoticia_Master)
    for linkNoticia_Analizar in list_linksNoticiasAnalizar:

        if linkNoticia_Master == linkNoticia_Analizar:  # Noticia a analizar es la noticia master
            continue

        dicc_noticiaVector[linkNoticia_Analizar] = similitud_obj.getDocVector(linkNoticia_Analizar)

    time_end = time.time()

    print_creacionVectores(similitud_obj.getNombreSimilitud(), len(dicc_noticiaVector), round(time_end - time_start))

    return vector_noticiaMaster, dicc_noticiaVector


# Función que obtiene los resultados de los algoritmos de similitud (T3)
# Aquellos algoritmos de similitud donde No utilizamos vectores, en este caso Jaccard,
# y podemos obtener resultados directamente.
def get_scores_T3(  extractor_obj, 
                    similitud_obj, 
                    atributoEstudio,
                    listLinksNoticias=None):

    procesador_obj = procesador.Procesador()
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

    return procesador_obj, round(time_end - time_start)


def get_Results_T1_T2(  vectorNoticiaMaster, 
                        dicc_noticiaVector_atributo1,
                        dicc_noticiaVector_atributo2=None,
                        peso_atributo1=1,
                        peso_atributo2=1):

    time_start = time.time()

    procesador_obj = procesador.Procesador()

    # Comprobamos si hay 1 o 2 atributos al principio para evitar comprobaciones en el bucle
    # Caso de SOLO 1 atributo
    if dicc_noticiaVector_atributo2 == None:

        for linkNoticia in dicc_noticiaVector_atributo1.keys():
            vectorNoticiaAnalizar = dicc_noticiaVector_atributo1[linkNoticia] * peso_atributo1
            score = similitud_obj.similitud_coseno_vecs(vectorNoticiaMaster, vectorNoticiaAnalizar)
            procesador_obj.addResultado(linkNoticia, score)
    
    else:

        for linkNoticia in dicc_noticiaVector_atributo1.keys():
            vectorNoticiaAnalizar_atributo1 = dicc_noticiaVector_atributo1[linkNoticia] * peso_atributo1
            vectorNoticiaAnalizar_atributo2 = dicc_noticiaVector_atributo2[linkNoticia] * peso_atributo2
            vectorNoticiaAnalizar = vectorNoticiaAnalizar_atributo1 + vectorNoticiaAnalizar_atributo2
            score = similitud_obj.similitud_coseno_vecs(vectorNoticiaMaster, vectorNoticiaAnalizar)
            procesador_obj.addResultado(linkNoticia, score)

    time_end = time.time()

    return procesador_obj, round(time_end - time_start)


def print_creacionVectores( algoritmoSimilitud, 
                            noticiasAnalizadas, 
                            tiempoEmpleado):
    
    mins = math.floor(tiempoEmpleado / 60)
    segs = round((tiempoEmpleado / 60 - mins) * 60)

    strPrint = "#########################################################\n"
    strPrint += ">> Creación de vectores: \n"
    strPrint += "Algoritmo: '{}'\n"
    strPrint += "Vectores creados: {}\n"
    strPrint += "Tiempo empleado: {} minutos y {} segundos\n"
    strPrint = strPrint.format( algoritmoSimilitud,
                                str(noticiasAnalizadas),
                                str(mins),
                                str(segs))
    print(strPrint)

    return


def print_results(  procesador_obj, 
                    list_simsUtilizadas,
                    noticiasEtiquetadas,
                    topResults,
                    list_atrisUtilizados,
                    executionTime):

    procesador_obj.sortResultados()
    diccResults, strResultTop = procesador_obj.getTopResultados(noticiasEtiquetadas, top=topResults)
    mins = math.floor(executionTime / 60)
    segs = round((executionTime / 60 - mins) * 60)

    strPrint = "#########################################################\n"
    strPrint += ">> Resultados: \n"
    strPrint += "Algoritmos: {}\n"
    strPrint += "Estudiando los atributos: {}\n"
    strPrint += "{} \n"
    strPrint += ">> Top: \n"
    strPrint += "{} \n"
    strPrint += "Tiempo empleado: {} minutos y {} segundos\n"
    strPrint = strPrint.format( " + ".join(list_simsUtilizadas),
                                " + ".join(list_atrisUtilizados),
                                procesador_obj,
                                strResultTop,
                                str(mins),
                                str(segs))
    print(strPrint)

    return diccResults


if __name__ == '__main__':
    
    extractor_obj = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)

    for sim1 in LISTA_SIMILITUDES:

        for atri1 in LISTA_ATRIBUTOS:
            similitud_obj = similitud.Similitud(sim1)

            if sim1 in LISTA_SIMILITUDES_T1 or sim1 in LISTA_SIMILITUDES_T2:

                if sim1 in LISTA_SIMILITUDES_T1:
                    vector_noticiaMaster, dicc_noticiaVector = get_vectores_algs_T1(extractor_obj,
                                                                                    similitud_obj,
                                                                                    atri1)

                elif sim1 in LISTA_SIMILITUDES_T2:

                    if sim1 == "SIMILITUD_COSENO_TF-IDF":
                        fuctAddEntry = similitud_obj.add_doc_wFrec_entry
                        functCreateVecs = similitud_obj.create_dicc_doc_tfidf
                    elif sim1 == "SIMILITUD_COSENO_BOW":
                        fuctAddEntry = similitud_obj.add_doc_wFrec_entry_BoW
                        functCreateVecs = similitud_obj.create_vec_doc_BoW

                    vector_noticiaMaster, dicc_noticiaVector = get_vectores_algs_T2(extractor_obj,
                                                                                    similitud_obj,
                                                                                    atri1,
                                                                                    fuctAddEntry,
                                                                                    functCreateVecs)

                # Realizamos 3 segundos de espera para poder hacer bien las mediciones de tiempo
                #time.sleep(3)
                procesador_obj, executionTime = get_Results_T1_T2(  vector_noticiaMaster,
                                                                    dicc_noticiaVector)
                                                                                
            elif sim1 in LISTA_SIMILITUDES_T3:
                procesador_obj, executionTime = get_scores_T3(  extractor_obj, 
                                                                similitud_obj,
                                                                atri1)
            
            noticiasEtiquetadas = extractor_obj.getDiccNoticiaEtiqueta()                                              
            diccResults = print_results(procesador_obj,
                                        [sim1],
                                        noticiasEtiquetadas,
                                        TOP_RESULTS_1,
                                        [atri1],
                                        executionTime)

    extractor_obj.closeFile()

'''
    COSAS QUE FALLAN:
        · En get_vectores_algs_T1():
            + No obtengo bien el vector de esta noticia: 
                keyWords - https://elpais.com/ccaa/2020/02/01/madrid/1580574138_819521.html
                autor - https://cincodias.elpais.com/cincodias/2020/01/24/mercados/1579868663_866345.html
'''