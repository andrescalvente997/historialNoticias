# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import time
import extractor
import similitud
import procesador

ATRIBUTO_ESTUDIO_1 = "cuerpoNoticia"
TOP_RESULTS = 100

def do_similitud(extractor, funct_similitud, nombreSimilitud):

    procesador_obj = procesador.Procesador(nombreSimilitud)

    time_start = time.time()

    dataNoticia_Master = extractor.getNoticiaMaster()
    atributoNoticia_Master = extractor.getAtributoNoticia(dataNoticia_Master, ATRIBUTO_ESTUDIO_1)
    dataNoticia_Analizar = extractor.getNextNoticia()
    while dataNoticia_Analizar != -1:
        
        linkNoticia = extractor.getAtributoNoticia(dataNoticia_Analizar, "linkNoticia", flgTratar=False)
        atributoNoticia_Analizar = extractor.getAtributoNoticia(dataNoticia_Analizar, ATRIBUTO_ESTUDIO_1)

        if atributoNoticia_Analizar == None:
            #print(">> Noticia sin Atributo - " + strAtributo + ": " + linkNoticia)
            dataNoticia_Analizar = extractor.getNextNoticia()
            continue

        score = funct_similitud(atributoNoticia_Master, atributoNoticia_Analizar)
        procesador_obj.addResultado(linkNoticia, score)

        dataNoticia_Analizar = extractor.getNextNoticia()

    time_end = time.time()
    
    printResult(procesador_obj, time_end - time_start)


def printResult(procesador_obj, executionTime):

    procesador_obj.sortResultados()
    _, strResultTop = procesador_obj.getTopResultados(top=TOP_RESULTS, flgPrintTop=True)

    print("#########################################################\n")
    print(">> Resumen:")
    print(procesador_obj)
    print(">> Top:")
    print(strResultTop)
    print(">> Tiempo de ejecución:")
    print(str(executionTime) + " segundos.\n")


if __name__ == '__main__':

    strFile = dirname(abspath(__file__)) + "/" + "../crawler/crawlerPeriodicos/datos_EL_PAIS/20200125_20200202_noticias.json"
    extractor = extractor.Extractor(strFile, "https://elpais.com/sociedad/2020/02/01/actualidad/1580569994_549942.html")
    
    similitud_obj = similitud.Similitud()
    do_similitud(extractor, similitud_obj.similitud_spacy, "Similitud_Coseno_Spacy")
    
    similitud_obj = similitud.Similitud()
    do_similitud(extractor, similitud_obj.similitud_jaccard, "Similitud_Jaccard")

