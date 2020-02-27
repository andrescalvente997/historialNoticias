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

    
    def getTopResultados(self, noticiasEtiquetadas, top=10, flgAllRes=False):

        diccRes = {}
        strPrint = ""

        if flgAllRes == True:
            numTop = 1
            for k, v in self.diccResultados.items():
                strPrint += "Top {}: {} \t{} ".format(  str(numTop),
                                                        k,
                                                        str(v))
                if k in noticiasEtiquetadas:
                    strPrint += "\t{} ".format( noticiasEtiquetadas[k])
                strPrint += "\n"
                numTop += 1
                diccRes[k] = v

        else:
            for item, numTop in zip(self.diccResultados.items(), range(top)):

                strPrint += "Top {}: {} \t{} ".format(str(numTop+1),
                                                        item[0],
                                                        str(item[1])) 
                if item[0] in noticiasEtiquetadas:
                    strPrint += "\t{} ".format( noticiasEtiquetadas[item[0]])
                strPrint += "\n"                   
                diccRes[item[0]] = item[1]

        return diccRes, strPrint


    def __str__(self):

        strPrint = "Para la similitud: {}\n"
        strPrint += "Noticias evaluadas hasta el momento: {}\n"
        strPrint += "Score medio de las noticias es de: {}\n"
        strPrint = strPrint.format( self.nombreSimilitud,
                                    str(len(self.diccResultados)),
                                    str(self.scoreAcum / len(self.diccResultados)))
        return strPrint