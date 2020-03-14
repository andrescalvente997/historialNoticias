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
                    "tagsNoticia"]  
'''

,"cuerpoNoticia"
''' 
LISTA_SIMILITUDES = [   "SIMILITUD_COSENO_TF-IDF",
                        "SIMILITUD_COSENO_BOW"]
'''
"SIMILITUD_COSENO_SPACY", 
                        "SIMILITUD_JACCARD",
'''
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


def do_similitud_noCreacionVecs(obj_extractor, 
                                obj_similitud,  
                                list_atributosEstudio,
                                listLinksNoticias=None):

    obj_procesador = procesador.Procesador()
    funct_similitud = obj_similitud.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = obj_extractor.getDataNoticiaMaster()
    texto_Master = ""
    for atributo in list_atributosEstudio:
        texto_Master += " " + obj_extractor.getAtributoNoticia(dataNoticia_Master, atributo)    
    texto_Master = obj_extractor.getDoc(texto_Master) 

    print(texto_Master)

    if listLinksNoticias == None:
        listLinksNoticias = obj_extractor.getLinksNoticiasAnalizar()
    for linkNoticia in listLinksNoticias:
        
        dataNoticia_Analizar = obj_extractor.getDataNoticia(linkNoticia)
        if dataNoticia_Analizar == None:    # Noticia con fecha posterior a la Master
            continue
        
        texto_Analizar = ""
        for atributo in list_atributosEstudio:
            texto_Analizar += " " + obj_extractor.getAtributoNoticia(dataNoticia_Analizar, atributo)
        texto_Analizar = obj_extractor.getDoc(texto_Analizar)

        score = funct_similitud(texto_Master, texto_Analizar)
        obj_procesador.addResultado(linkNoticia, score)

    time_end = time.time()

    return obj_procesador, round(time_end - time_start)


def do_similitud_creacionVectores(  obj_extractor, 
                                    obj_similitud, 
                                    list_atributosEstudio,
                                    funct_addEntry, 
                                    funct_createVecs, 
                                    listLinksNoticias=None):
    
    obj_procesador = procesador.Procesador()
    funct_similitud = obj_similitud.getFuncionSimilitud()

    time_start = time.time()

    dataNoticia_Master = obj_extractor.getDataNoticiaMaster()
    texto_Master = ""
    for atributo in list_atributosEstudio:
        texto_Master += " " + obj_extractor.getAtributoNoticia(dataNoticia_Master, atributo)    
    texto_Master = obj_extractor.getDoc(texto_Master) 
    linkNoticia_Master = obj_extractor.getLinkNoticiaMaster()
    funct_addEntry(linkNoticia_Master, texto_Master)

    if listLinksNoticias == None:
        listLinksNoticias = obj_extractor.getLinksNoticiasAnalizar()
    for linkNoticia in listLinksNoticias:
        
        dataNoticia_Analizar = obj_extractor.getDataNoticia(linkNoticia)
        if dataNoticia_Analizar == None:    # Noticia con fecha posterior a la Master
            continue

        texto_Analizar = ""
        for atributo in list_atributosEstudio:
            texto_Analizar += " " + obj_extractor.getAtributoNoticia(dataNoticia_Analizar, atributo)
        texto_Analizar = obj_extractor.getDoc(texto_Analizar)

        funct_addEntry(linkNoticia, texto_Analizar)

    funct_createVecs()

    list_linksNoticiasAnalizar = obj_similitud.getLinksNoticias()

    for linkNoticia_Analizar in list_linksNoticiasAnalizar:

        if linkNoticia_Master == linkNoticia_Analizar:  # Noticia a analizar es la noticia master
            continue

        score = funct_similitud(linkNoticia_Master, linkNoticia_Analizar)
        obj_procesador.addResultado(linkNoticia_Analizar, score)

    time_end = time.time()

    return obj_procesador, round(time_end - time_start)

def printResult(obj_procesador, 
                similitudUtilizada,
                noticiasEtiquetadas,
                topResults,
                list_atrisUtilizados,
                executionTime):

    obj_procesador.sortResultados()
    diccResults, strResultTop = obj_procesador.getTopResultados(noticiasEtiquetadas, top=topResults)
    mins = math.floor(executionTime / 60)
    segs = round((executionTime / 60 - mins) * 60)

    strPrint = "#########################################################\n"
    strPrint += ">> Resultados: \n"
    strPrint += "Algoritmo: {}\n"
    strPrint += "Estudiando los atributos: {}\n"
    strPrint += "{} \n"
    strPrint += ">> Top: \n"
    strPrint += "{} \n"
    strPrint += "Tiempo empleado: {} minutos y {} segundos\n"
    strPrint = strPrint.format( similitudUtilizada,
                                " + ".join(list_atrisUtilizados),
                                obj_procesador,
                                strResultTop,
                                str(mins),
                                str(segs))
    FILE_OUT.write(strPrint)
    
    print("Terminado Similitud: " + similitudUtilizada + "\t para atributo: " + " + ".join(list_atrisUtilizados))

    return diccResults            
    

if __name__ == '__main__':
    
    obj_extractor = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)
    noticiasEtiquetadas = obj_extractor.getDiccNoticiaEtiqueta()

    for tipoSimilitud in LISTA_SIMILITUDES:

        atributosVistos = []

        for atributo_1 in LISTA_ATRIBUTOS:

            list_atributosEstudio = [atributo_1]
            obj_similitud = similitud.Similitud(tipoSimilitud)

            for atributo_2 in LISTA_ATRIBUTOS:

                if atributo_2 in atributosVistos:
                    continue

                if atributo_1 != atributo_2:
                    list_atributosEstudio.append(atributo_2)

                print(list_atributosEstudio)

                if tipoSimilitud in LISTA_SIMILITUDES_T1 or tipoSimilitud in LISTA_SIMILITUDES_T3:

                    obj_procesador, tiempoEjecucion = do_similitud_noCreacionVecs(  obj_extractor,
                                                                                    obj_similitud,
                                                                                    list_atributosEstudio)
                
                elif tipoSimilitud in LISTA_SIMILITUDES_T2:

                    if tipoSimilitud == "SIMILITUD_COSENO_TF-IDF":
                        atributo_funct_addEntry = obj_similitud.add_doc_wFrec_entry
                        atributo_funct_createVecs = obj_similitud.create_dicc_doc_tfidf

                    elif tipoSimilitud == "SIMILITUD_COSENO_BOW":
                        atributo_funct_addEntry = obj_similitud.add_doc_wFrec_entry_BoW
                        atributo_funct_createVecs = obj_similitud.create_vec_doc_BoW

                    obj_procesador, tiempoEjecucion = do_similitud_creacionVectores(obj_extractor,
                                                                                    obj_similitud,
                                                                                    list_atributosEstudio,
                                                                                    atributo_funct_addEntry,
                                                                                    atributo_funct_createVecs)
                
                printResult(obj_procesador,
                            tipoSimilitud,
                            noticiasEtiquetadas,
                            TOP_RESULTS_1,
                            list_atributosEstudio,
                            tiempoEjecucion)

                if atributo_1 != atributo_2:
                    list_atributosEstudio.remove(atributo_2)

            atributosVistos.append(atributo_1)

    obj_extractor.closeFile()
    FILE_OUT.close()
