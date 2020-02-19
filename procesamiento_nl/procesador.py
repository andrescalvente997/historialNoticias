# -*- coding: utf-8 -*-

#
# Clase encargada de evaluar los resultados obtenidos y mostrarlos al usuario 
#

class Procesador():

    def __init__(self, nombreSimilitud):
        
        self.diccResultados = {}
        self.scoreAcum = 0
        self.nombreSimilitud = nombreSimilitud


    def addResultado(self, linkNoticia, score):

        self.diccResultados[linkNoticia] = score
        self.scoreAcum += score


    def sortResultados(self):

        self.diccResultados = {k: v for k, v in sorted(self.diccResultados.items(), key=lambda item: item[1], reverse=True)}

    
    def getTopResultados(self, top=10, flgAllRes=False, flgPrintTop=False):

        listRes = []
        strPrint = ""

        if flgAllRes == True:
            numTop = 1
            for k, v in self.diccResultados.items():
                if flgPrintTop == True:
                    strPrint += "Top " + str(numTop) + ": " + k + "\t" + str(v) + "\n"
                    numTop += 1
                else:
                    listRes.append((k,v))

        else:
            for item, numTop in zip(self.diccResultados.items(), range(top)):
                if flgPrintTop == True:
                    strPrint += "Top " + str(numTop+1) + ": " + item[0] + "\t" + str(item[1]) + "\n"
                else:
                    listRes.append(item)

        return listRes, strPrint


    def __str__(self):

        strPrint = "Para la similitud: " + self.nombreSimilitud + "\n"
        strPrint += "Noticias evaluadas hasta el momento: " + str(len(self.diccResultados)) + "\n"
        strPrint += "Score medio de las noticias es de: " + str(self.scoreAcum / len(self.diccResultados)) + "\n"
        return strPrint