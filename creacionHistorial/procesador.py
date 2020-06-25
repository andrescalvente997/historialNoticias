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

    
    def getTopResultados(self, noticiasEtiquetadas, tematicaEstudiada, top=None):

        diccRes = {}
        strPrint = ""
        m_pred = [] # Array de predicciones

        numTop = 1

        # Así podemos imprimir todos los resultados si queremos
        if top == None:
            top = len(self.diccResultados)

        for k, v in self.diccResultados.items():
            
            if numTop <= top:
                strPrint += "Top {}: {} \t{}\n".format(  str(numTop),
                                                        k,
                                                        str(v))

            flg_noticiaEtiquetada = False
            for etiqueta, noticiasEtiqueta in noticiasEtiquetadas.items():

                if k in noticiasEtiqueta:

                    if numTop <= top:
                        strPrint = strPrint[:-1] + "\t{}\n".format(etiqueta)

                    if etiqueta == tematicaEstudiada:
                        m_pred.append(etiqueta)
                    else:
                        m_pred.append("OTRO")

                    flg_noticiaEtiquetada = True

                    break

            if flg_noticiaEtiquetada == False:
                m_pred.append("OTRO")
                
            if numTop <= top:
                diccRes[k] = v
            numTop += 1

        return diccRes, strPrint, m_pred


    def __str__(self):

        strPrint = "Noticias evaluadas hasta el momento: {}\n"
        strPrint += "Score medio de las noticias es de: {}\n"
        strPrint = strPrint.format( str(len(self.diccResultados)),
                                    str(self.scoreAcum / len(self.diccResultados)))
        return strPrint