# -*- coding: utf-8 -*-

#
# Clase encargada de evaluar los resultados obtenidos y mostrarlos al usuario 
#

class Procesador():

    def __init__(self):
        
        self.diccResultados = {}
        self.scoreAcum = 0


    def addResultado(self, linkNoticia, score):

        self.diccResultados[linkNoticia] = score
        self.scoreAcum += score


    def sortResultados(self):

        self.diccResultados = {k: v for k, v in sorted(self.diccResultados.items(), key=lambda item: item[1], reverse=True)}

    
    def getTopResultados(self, noticiasEtiquetadas, top=10, flgAllRes=False):

        diccRes = {}
        strPrint = ""
        m_pred = [] # Array de predicciones

        if flgAllRes == True:
            numTop = 1
            for k, v in self.diccResultados.items():
                strPrint += "Top {}: {} \t{} ".format(  str(numTop),
                                                        k,
                                                        str(v))

                flg_noticiaEtiquetada = False
                for etiqueta, noticiasEtiqueta in noticiasEtiquetadas.items():
                    if k in noticiasEtiqueta:
                        strPrint += "\t{} ".format(etiqueta)
                        m_pred.append(etiqueta)
                        flg_noticiaEtiquetada = True
                        break
                if flg_noticiaEtiquetada == False:
                    m_pred.append("OTRO")

                strPrint += "\n"
                numTop += 1
                diccRes[k] = v

        else:
            for item, numTop in zip(self.diccResultados.items(), range(top)):

                strPrint += "Top {}: {} \t{} ".format(str(numTop+1),
                                                        item[0],
                                                        str(item[1])) 
                
                flg_noticiaEtiquetada = False
                for etiqueta, noticiasEtiqueta in noticiasEtiquetadas.items():
                    if item[0] in noticiasEtiqueta:
                        strPrint += "\t{} ".format(etiqueta)
                        m_pred.append(etiqueta)
                        flg_noticiaEtiquetada = True
                        break
                if flg_noticiaEtiquetada == False:
                    m_pred.append("OTRO")

                strPrint += "\n"                   
                diccRes[item[0]] = item[1]

        return diccRes, strPrint, m_pred


    def __str__(self):

        strPrint = "Noticias evaluadas hasta el momento: {}\n"
        strPrint += "Score medio de las noticias es de: {}\n"
        strPrint = strPrint.format( str(len(self.diccResultados)),
                                    str(self.scoreAcum / len(self.diccResultados)))
        return strPrint