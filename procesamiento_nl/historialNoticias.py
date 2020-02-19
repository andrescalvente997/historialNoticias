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

def do_similitud(funct_similitud, nombreSimilitud):

    extractor_obj = extractor.Extractor(NOTICIA_FILEPATH, URL_NOTICIA_ANALIZAR)

    procesador_obj = procesador.Procesador(nombreSimilitud)

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


def printResult(procesador_obj, executionTime):

    procesador_obj.sortResultados()
    _, strResultTop = procesador_obj.getTopResultados(top=TOP_RESULTS, flgPrintTop=True)
    mins = math.floor(executionTime / 60)
    segs = round((executionTime / 60 - mins) * 60)

    print("#########################################################\n")
    print(">> Resumen:")
    print(procesador_obj)
    print(">> Top:")
    print(strResultTop)
    print(">> Tiempo de ejecución:")
    print("{} minutos y {} segundos.\n".format(str(mins), str(segs)))

    return


if __name__ == '__main__':

    similitud_obj = similitud.Similitud()

    do_similitud(similitud_obj.similitud_spacy, "Similitud_Coseno_Spacy")
    do_similitud(similitud_obj.similitud_jaccard, "Similitud_Jaccard")

