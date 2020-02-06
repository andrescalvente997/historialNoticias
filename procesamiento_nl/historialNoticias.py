# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import extractor
import similitud
import procesador

strFile = dirname(abspath(__file__)) + "/" + "../crawler/crawlerPeriodicos/datos_EL_PAIS/20200125_20200202_noticias.json"
extractor = extractor.Extractor(strFile, "https://elpais.com/sociedad/2020/02/01/actualidad/1580569994_549942.html")

# Resultados en diccionario : { LinkNoticia: Score }

procesador = procesador.Procesador()

similitud = similitud.Similitud()

dataNoticia_Master = extractor.getNoticiaMaster()

cuerpoNoticia_Master = extractor.getAtributoNoticia(dataNoticia_Master, "cuerpoNoticia")

dataNoticia_Analizar = extractor.getNextNoticia()

n=0

while dataNoticia_Analizar != -1:
    
    linkNoticia = extractor.getAtributoNoticia(dataNoticia_Analizar, "linkNoticia", flgTratar=False)
    cuerpoNoticia_Analizar = extractor.getAtributoNoticia(dataNoticia_Analizar, "cuerpoNoticia")

    if cuerpoNoticia_Analizar == None:
        print(">> Noticia Vacia: ", linkNoticia)
        dataNoticia_Analizar = extractor.getNextNoticia()
        continue

    score = similitud.similitud_spacy(cuerpoNoticia_Master, cuerpoNoticia_Analizar)
    procesador.addResultado(linkNoticia, score)

    dataNoticia_Analizar = extractor.getNextNoticia()

procesador.sortResultados()
_, strr = procesador.getTopResultados(flgAllRes=True, flgPrintTop=True)
print(strr)
print(procesador)