# -*- coding: utf-8 -*-

from os.path import abspath, dirname

class Periodico():

    def __init__(self, periodico, anio, mes, dia = None):
        
        self.nombre = periodico
        self.anio = anio
        self.mes = mes
        self.dia = dia
        
        self.initVarsURLs()


    def crea_StartUrls(self):

        if self.nombre != "MARCA":
            if self.dia != None:
                listURLs, strFile = self.crea_StartUrls_oneDay()
            else:
                listURLs, strFile = self.crea_StartUrls_oneMonth()
        else:
            listURLs, strFile = self.crea_StartUrls_Marca()

        strFile = dirname(abspath(__file__)) + "/" + strFile

        return listURLs, strFile


    def crea_StartUrls_oneDay(self):

        listURLs = []
        # Diccionario k(numero mes): v( set(dias del mes, str mes) )
        diccMeses = {   1: (31, "01"), 2: (28, "02"), 3: (31, "03"), 4: (30, "04"), 5: (31, "05"), 
                        6: (30, "06"), 7: (31, "07"), 8: (31, "08"), 9: (30, "09"), 10: (31, "10"), 
                        11: (30, "11"), 12: (31, "12")}

        if int(self.dia) < 10:
            strFile = "{}/{}_{}_0{}_noticias.json".format(  self.directorio,
                                                            self.anio,
                                                            diccMeses[self.mes][1],
                                                            str(int(self.dia)))
            if not self.listado: # Listado de periodos vacio
                url = "{0}/{1}{2}{3}{2}0{4}/{5}".format(    self.dominio,
                                                            self.anio,
                                                            self.separadorFecha,
                                                            diccMeses[self.mes][1],
                                                            str(int(self.dia)),
                                                            self.archivo)
                listURLs.append(url)
            else:
                for elemento in self.listado:
                    url = "{0}/{1}{2}{3}{2}0{4}/{5}/{6}".format(    self.dominio,
                                                                    self.anio,
                                                                    self.separadorFecha,
                                                                    diccMeses[self.mes][1],
                                                                    str(int(self.dia)),
                                                                    elemento,
                                                                    self.archivo)
                    listURLs.append(url)
            
        else:
            strFile = "{}/{}_{}_{}_noticias.json".format(   self.directorio,
                                                            self.anio,
                                                            diccMeses[self.mes][1],
                                                            self.dia)
            if not self.listado: # Listado de periodos vacio
                url = "{0}/{1}{2}{3}{2}{4}/{5}".format( self.dominio,
                                                        self.anio,
                                                        self.separadorFecha,
                                                        diccMeses[self.mes][1],
                                                        str(int(self.dia)),
                                                        self.archivo)
                listURLs.append(url)
            else:
                for elemento in self.listado:
                    url = "{0}/{1}{2}{3}{2}{4}/{5}/{6}".format( self.dominio,
                                                                self.anio,
                                                                self.separadorFecha,
                                                                diccMeses[self.mes][1],
                                                                str(int(self.dia)),
                                                                elemento,
                                                                self.archivo)
                    listURLs.append(url)
        
        return listURLs, strFile


    def crea_StartUrls_oneMonth(self):

        listURLs = []
        # Diccionario k(numero mes): v( set(dias del mes, str mes) )
        diccMeses = {   1: (31, "01"), 2: (28, "02"), 3: (31, "03"), 4: (30, "04"), 5: (31, "05"), 
                        6: (30, "06"), 7: (31, "07"), 8: (31, "08"), 9: (30, "09"), 10: (31, "10"), 
                        11: (30, "11"), 12: (31, "12")}

        strFile = "{}/{}_{}_noticias.json".format(  self.directorio,
                                                    self.anio,
                                                    diccMeses[self.mes][1])                

        for i in range(diccMeses[self.mes][0]):

            if not self.listado: # Listado de periodos vacio
                if i+1 < 10:
                    url = "{0}/{1}{2}{3}{2}0{4}/{5}".format(    self.dominio,
                                                                self.anio,
                                                                self.separadorFecha,
                                                                diccMeses[self.mes][1],
                                                                str(i+1),
                                                                self.archivo)
                else:
                    url = "{0}/{1}{2}{3}{2}{4}/{5}".format( self.dominio,
                                                            self.anio,
                                                            self.separadorFecha,
                                                            diccMeses[self.mes][1],
                                                            str(i+1),
                                                            self.archivo)
                listURLs.append(url)

            else:
                if i+1 < 10:
                    for elemento in self.listado:
                        url = "{0}/{1}{2}{3}{2}0{4}/{5}/{6}".format(    self.dominio,
                                                                        self.anio,
                                                                        self.separadorFecha,
                                                                        diccMeses[self.mes][1],
                                                                        str(i+1),
                                                                        elemento,
                                                                        self.archivo)
                        listURLs.append(url)
                else:
                    for elemento in self.listado:
                        url = "{0}/{1}{2}{3}{2}{4}/{5}/{6}".format( self.dominio,
                                                                    self.anio,
                                                                    self.separadorFecha,
                                                                    diccMeses[self.mes][1],
                                                                    str(i+1),
                                                                    elemento,
                                                                    self.archivo)
                        listURLs.append(url)
        
        return listURLs, strFile


    def crea_StartUrls_Marca(self):

        listURLs = []
        # Diccionario k(numero mes): v( set(dias del mes, str mes) )
        diccMeses = {   1: (31, "01"), 2: (28, "02"), 3: (31, "03"), 4: (30, "04"), 5: (31, "05"), 
                        6: (30, "06"), 7: (31, "07"), 8: (31, "08"), 9: (30, "09"), 10: (31, "10"), 
                        11: (30, "11"), 12: (31, "12")}

        if self.dia == None:

            strFile = "{}/{}_{}_noticias.json".format(  self.directorio,
                                                        self.anio,
                                                        diccMeses[self.mes][1])
            for i in range(diccMeses[self.mes][0]):
                for elemento in self.listado:
                    if int(self.dia) < 10:
                        url = "{0}/{1}{2}{3}{2}0{4}/index_{5}.html".format( self.dominio,
                                                                            self.anio,
                                                                            self.separadorFecha,
                                                                            diccMeses[self.mes][1],
                                                                            str(int(self.dia)),
                                                                            elemento,
                                                                            self.archivo)
                    else:
                        url = "{0}/{1}{2}{3}{2}{4}/index_{5}.html".format(  self.dominio,
                                                                            self.anio,
                                                                            self.separadorFecha,
                                                                            diccMeses[self.mes][1],
                                                                            str(int(self.dia)),
                                                                            elemento,
                                                                            self.archivo)
                    listURLs.append(url)                  

        else:
            if int(self.dia) < 10:
                strFile = "{}/{}_{}_0{}_noticias.json".format(  self.directorio,
                                                                self.anio,
                                                                diccMeses[self.mes][1],
                                                                str(int(self.dia)))
                for elemento in self.listado:
                    url = "{0}/{1}{2}{3}{2}0{4}/index_{5}.html".format( self.dominio,
                                                                self.anio,
                                                                self.separadorFecha,
                                                                diccMeses[self.mes][1],
                                                                str(int(self.dia)),
                                                                elemento,
                                                                self.archivo)
                    listURLs.append(url)
            else:
                strFile = "{}/{}_{}_{}_noticias.json".format(  self.directorio,
                                                                self.anio,
                                                                diccMeses[self.mes][1],
                                                                str(int(self.dia)))
                for elemento in self.listado:
                    url = "{0}/{1}{2}{3}{2}{4}/index_{5}.html".format( self.dominio,
                                                                self.anio,
                                                                self.separadorFecha,
                                                                diccMeses[self.mes][1],
                                                                str(int(self.dia)),
                                                                elemento,
                                                                self.archivo)
                    listURLs.append(url)
        
        return listURLs, strFile


    def initVarsURLs(self):

        periodos = ['m', 't', 'n']
        ediciones = ['1', '2']

        # URLS => https://elpais.com/hemeroteca/elpais/YYYY/MM/dd/[m,t,n]/portada.html
        if self.nombre == "EL_PAIS":
            
            self.directorio = "datos_EL_PAIS"
            self.dominio = "https://elpais.com/hemeroteca/elpais"
            self.archivo = "portada.html"
            self.separadorFecha = "/"
            self.listado = periodos

        # URLS => https://www.elmundo.es/elmundo/hemeroteca/YYYY/MM/dd/[m,t,n]/index.html
        elif self.nombre == "EL_MUNDO":
            
            self.directorio = "datos_EL_MUNDO"
            self.dominio = "https://www.elmundo.es/elmundo/hemeroteca"
            self.archivo = "index.html"
            self.separadorFecha = "/"
            self.listado = periodos

        # URLS => https://www.20minutos.es/archivo/YYYY/MM/dd/
        elif self.nombre == "20_MINUTOS":
            
            self.directorio = "datos_20_MINUTOS"
            self.dominio = "https://www.20minutos.es/archivo"
            self.archivo = ""
            self.separadorFecha = "/"
            self.listado = []

        # URLS => https://www.elconfidencial.com/hemeroteca/YYYY-MM-dd/[1,2]/
        elif self.nombre == "EL_CONFIDENCIAL":
            
            self.directorio = "datos_EL_CONFIDENCIAL"
            self.dominio = "https://www.elconfidencial.com/hemeroteca"
            self.archivo = ""
            self.separadorFecha = "-"
            self.listado = ediciones

        # URLS => https://www.marca.com/hemeroteca/YYYY/MM/dd/index_[m,t,n].html
        elif self.nombre == "MARCA":
            
            self.directorio = "datos_MARCA"
            self.dominio = "https://www.marca.com/hemeroteca"
            self.archivo = ""
            self.separadorFecha = "/"
            self.listado = periodos