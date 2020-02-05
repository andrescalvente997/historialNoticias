# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import extractor

import spacy


strFile = dirname(abspath(__file__)) + "/" + "../crawler/crawlerPeriodicos/datos_EL_PAIS/20200125_20200202_noticias.json"
extractor = extractor.Extractor(strFile, "https://elpais.com/sociedad/2020/02/01/actualidad/1580569994_549942.html")

# Resultados en diccionario : { LinkNoticia: Score }

diccResultados = {}

dataNoticia_Master = extractor.getNoticiaMaster()


cuerpoNoticia_Master = extractor.getAtributoNoticia(dataNoticia_Master, "cuerpoNoticia")

dataNoticia_Analizar = extractor.getNextNoticia()

while dataNoticia_Analizar != -1:
    
    urlNoticia_Analizar = extractor.getAtributoNoticia(dataNoticia_Analizar, "linkNoticia", flgTratar=False)
    cuerpoNoticia_Analizar = extractor.getAtributoNoticia(dataNoticia_Analizar, "cuerpoNoticia")

    if cuerpoNoticia_Analizar == None:
        print(">> Noticia Vacia: ", urlNoticia_Analizar)
        dataNoticia_Analizar = extractor.getNextNoticia()
        continue

    diccResultados[urlNoticia_Analizar] = round(cuerpoNoticia_Master.similarity(cuerpoNoticia_Analizar), 5)

    dataNoticia_Analizar = extractor.getNextNoticia()

diccResultados = {k: v for k, v in sorted(diccResultados.items(), key=lambda item: item[1], reverse=True)}

for k, v in diccResultados.items():
    print(k,"\t\t",v)