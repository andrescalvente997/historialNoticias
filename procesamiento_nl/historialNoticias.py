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

strAtributo = "cuerpoNoticia"

dataNoticia_Master = extractor.getNoticiaMaster()

atributoNoticia_Master = extractor.getAtributoNoticia(dataNoticia_Master, strAtributo)

print(atributoNoticia_Master)

dataNoticia_Analizar = extractor.getNextNoticia()

n=0

while dataNoticia_Analizar != -1:
    
    linkNoticia = extractor.getAtributoNoticia(dataNoticia_Analizar, "linkNoticia", flgTratar=False)
    atributoNoticia_Analizar = extractor.getAtributoNoticia(dataNoticia_Analizar, strAtributo)

    if atributoNoticia_Analizar == None:
        print(">> Noticia sin Atributo - " + strAtributo + ": " + linkNoticia)
        dataNoticia_Analizar = extractor.getNextNoticia()
        continue

    score = similitud.similitud_spacy(atributoNoticia_Master, atributoNoticia_Analizar)
    procesador.addResultado(linkNoticia, score)

    dataNoticia_Analizar = extractor.getNextNoticia()

procesador.sortResultados()
_, strr = procesador.getTopResultados(flgAllRes=True, flgPrintTop=True)
print(strr)
print(procesador)