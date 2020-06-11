# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import sys
import time
import math
import extractor
import similitud
import procesador
from datetime import datetime
from sklearn.metrics import classification_report

LISTA_ATRIBUTOS = [ "titularNoticia",
                    "keywordsNoticia",
                    "resumenNoticia",
                    "autorNoticia",
                    "tagsNoticia",
                    "cuerpoNoticia"]  
                    
LISTA_SIMILITUDES = [   "SIMILITUD_COSENO_SPACY", 
                        "SIMILITUD_JACCARD",
                        "SIMILITUD_COSENO_TF-IDF",
                        "SIMILITUD_COSENO_BOW",
                        "SIMILITUD_COSENO_SPACY_FH",
                        "SIMILITUD_JACCARD_FH"]
                        
LISTA_SIMILITUDES_T1 = ["SIMILITUD_COSENO_SPACY",
                        "SIMILITUD_JACCARD"]
LISTA_SIMILITUDES_T2 = ["SIMILITUD_COSENO_TF-IDF",
                        "SIMILITUD_COSENO_BOW"]
LISTA_SIMILITUDES_T3 = ["SIMILITUD_COSENO_SPACY_FH",
                        "SIMILITUD_JACCARD_FH"]

URL_NOTICIA_ANALIZAR = "https://elpais.com/politica/2019/10/20/actualidad/1571575152_143333.html"
TEMA_NOTICIA = "ELECCIONES_GENERALES_NOV2019"
NUM_NOTICIAS_CON_TEMA = 41
TOP_RESULTS_1 = 75

NOTICIA_FILEPATH = dirname(abspath(__file__)) + "/" + "../creacionDataset/crawlerPeriodicos/dataset_pruebas_ficheros/dataset_pruebas_EL_PAIS.json"
STR_FICHERO_OUT = "../dataset_pruebas_EL_PAIS_scores.txt"
FILE_OUT_SCORES = open(STR_FICHERO_OUT, 'w')
FILE_OUT_SCORES.write("NOTICIA DE REFERENCIA: " + URL_NOTICIA_ANALIZAR + "\n")
STR_FICHERO_OUT = "../dataset_pruebas_EL_PAIS_historial.txt"
FILE_OUT_HIST = open(STR_FICHERO_OUT, 'w')
FILE_OUT_HIST.write("NOTICIA DE REFERENCIA: " + URL_NOTICIA_ANALIZAR + "\n")


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


def do_similitud_noVecs_franjasHorarias(obj_extractor, 
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

    if listLinksNoticias == None:
        listLinksNoticias = obj_extractor.getLinksNoticiasAnalizar()

    dicc_rangoFecha_noticias = obj_extractor.create_diccRangoFechaNoticas()

    for listLinksNoticias in dicc_rangoFecha_noticias.values():
        tuple_mejorNoticia = ("", 0)
        for linkNoticia in listLinksNoticias:

            dataNoticia_Analizar = obj_extractor.getDataNoticia(linkNoticia)
            if dataNoticia_Analizar == None:    # Noticia con fecha posterior a la Master
                continue
        
            texto_Analizar = ""
            for atributo in list_atributosEstudio:
                texto_Analizar += " " + obj_extractor.getAtributoNoticia(dataNoticia_Analizar, atributo)
            texto_Analizar = obj_extractor.getDoc(texto_Analizar)

            score = funct_similitud(texto_Master, texto_Analizar)
            if score > tuple_mejorNoticia[1]:
                tuple_mejorNoticia = (linkNoticia, score)
            
            obj_procesador.addResultado(linkNoticia, score)

        if tuple_mejorNoticia[0] != "" and tuple_mejorNoticia[1] >= 0.45:
            dataNoticia_Add = obj_extractor.getDataNoticia(tuple_mejorNoticia[0])
            txtAdd = ""
            for atributo in list_atributosEstudio:
                txtAdd += " " + obj_extractor.getAtributoNoticia(dataNoticia_Add, atributo)
            texto_Master = texto_Master.text + " " + txtAdd
            texto_Master = obj_extractor.getDoc(texto_Master)

    time_end = time.time()

    return obj_procesador, round(time_end - time_start)


def printResult(obj_procesador, 
                obj_extractor,
                similitudUtilizada,
                topResults,
                list_atrisUtilizados,
                executionTime):

    obj_procesador.sortResultados()

    noticiasEtiquetadas = obj_extractor.getDiccNoticiaEtiqueta()
    numNoticiasConEtiqueta_Esp = obj_extractor.getCountNoticiasConEtiqueta(TEMA_NOTICIA)

    diccResults, strResultTop, arrayEtiquetasPred = obj_procesador.getTopResultados(noticiasEtiquetadas, top=topResults)

    # Creacion de matriz de resultados por clases
    target_names = obj_extractor.getEtiquetasTema()
    target_names.append("OTRO")
    aux1_m_true = [target_names.index(TEMA_NOTICIA)] * numNoticiasConEtiqueta_Esp
    aux2_m_true = [target_names.index("OTRO")] * (len(arrayEtiquetasPred) - numNoticiasConEtiqueta_Esp)
    m_true = aux1_m_true + aux2_m_true
    m_pred = list(map(lambda x: target_names.index(x), arrayEtiquetasPred))

    mins = math.floor(executionTime / 60)
    segs = round((executionTime / 60 - mins) * 60)

    strPrint = "#########################################################\n"
    strPrint += ">> Resultados: \n"
    strPrint += "Algoritmo: {}\n"
    strPrint += "Estudiando los atributos: {}\n"
    strPrint += "{} \n"
    strPrint += ">> Top: \n"
    strPrint += "{} \n\n"
    strPrint += "{} \n\n"
    strPrint += "Tiempo empleado: {} minutos y {} segundos\n\n"
    strPrint = strPrint.format( similitudUtilizada,
                                " + ".join(list_atrisUtilizados),
                                obj_procesador,
                                strResultTop,
                                classification_report(m_true, m_pred, target_names=target_names, zero_division=0),
                                str(mins),
                                str(segs))
    FILE_OUT_SCORES.write(strPrint)

    strPrint = "Algoritmo: {}\t Atributos: {}\n"
    strPrint = strPrint.format( similitudUtilizada,
                                " + ".join(list_atrisUtilizados))
    FILE_OUT_HIST.write(strPrint)
    
    diccFechas = {}
    for linkNoticia in diccResults.keys():
        dataNoticia = obj_extractor.getDataNoticia(linkNoticia)
        fechaNoticia = obj_extractor.getAtributoNoticia(dataNoticia, "fechaPublicacionNoticia", flgTratar=False)
        diccFechas[linkNoticia] = fechaNoticia
    diccFechas = {k: v for k, v in sorted(diccFechas.items(), key=lambda item: datetime.strptime(item[1],"%Y-%m-%dT%H:%M:%SZ"), reverse=True)}
    
    for linkNoticia, fechaNoticia in diccFechas.items():
        strPrint = "{}\t{}\n"
        strPrint = strPrint.format( fechaNoticia,
                                    linkNoticia)
        FILE_OUT_HIST.write(strPrint)

    print("Terminado Similitud: " + similitudUtilizada + "\t para atributo: " + " + ".join(list_atrisUtilizados))

    return diccResults          
    

if __name__ == '__main__':
    
    obj_extractor = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)

    for tipoSimilitud in LISTA_SIMILITUDES:

        atributosVistos = []

        for atributo_1 in LISTA_ATRIBUTOS:

            for atributo_2 in LISTA_ATRIBUTOS:

                if atributo_2 in atributosVistos:
                    continue

                if atributo_1 != atributo_2:
                    list_atributosEstudio = [atributo_1, atributo_2]
                else:
                    list_atributosEstudio = [atributo_1]

                obj_similitud = similitud.Similitud(tipoSimilitud)

                if tipoSimilitud in LISTA_SIMILITUDES_T1:

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

                elif tipoSimilitud in LISTA_SIMILITUDES_T3:

                    obj_procesador, tiempoEjecucion = do_similitud_noVecs_franjasHorarias(  obj_extractor,
                                                                                            obj_similitud,
                                                                                            list_atributosEstudio)
                
                printResult(obj_procesador,
                            obj_extractor,
                            tipoSimilitud,
                            TOP_RESULTS_1,
                            list_atributosEstudio,
                            tiempoEjecucion)

            atributosVistos.append(atributo_1)

    obj_extractor.closeFile()
    FILE_OUT_SCORES.close()
    FILE_OUT_HIST.close()
