# -*- coding: utf-8 -*-

from os.path import abspath, dirname

class Periodico():

    def __init__(self, periodico, anio, mes, dia, fechaIni, fechaFin):
        
        self.nombre = periodico
        self.anio = anio
        self.mes = int(mes) if mes != None else mes
        self.dia = dia
        self.fechaIni = fechaIni
        self.fechaFin = fechaFin
        
        self.initVarsURLs()


    def crea_StartUrls(self):

        if self.nombre != "MARCA":
            if self.fechaIni != None and self.fechaFin != None:
                listURLs, strFile = self.crea_StartUrls_dateRange()
            elif self.dia != None:
                listURLs, strFile = self.crea_StartUrls_oneDay()
            else:
                listURLs, strFile = self.crea_StartUrls_oneMonth()
        else:
            listURLs, strFile = self.crea_StartUrls_Marca()

        strFile = dirname(abspath(__file__)) + "/" + strFile

        return listURLs, strFile


    def crea_StartUrls_dateRange(self):

        listURLs = []
        # Diccionario k(numero mes): v(numero de dias del mes)
        diccMeses = {   1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 
                        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        diaIni, mesIni, anioIni = self.fechaIni.split("-")
        diaFin, mesFin, anioFin = self.fechaFin.split("-")

        auxStr = "{}0{}" if int(mesIni) < 10 else "{}{}"
        auxStr += "0{}_" if int(diaIni) < 10 else "{}_"
        auxStr += "{}0{}" if int(mesFin) < 10 else "{}{}"
        auxStr += "0{}_" if int(diaFin) < 10 else "{}_"
        auxStr += "noticias.json"
        strFile = auxStr.format(    str(int(anioIni)),
                                    str(int(mesIni)),
                                    str(int(diaIni)),
                                    str(int(anioFin)),
                                    str(int(mesFin)),
                                    str(int(diaFin)))
        
        anioActual = int(anioIni)
        mesActual = int(mesIni)
        diaActual = int(diaIni)
        flgFin = False

        while flgFin == False:

            # Paso 1: Comprobamos si esta es la última iteración

            if anioActual == int(anioFin) and mesActual == int(mesFin) and diaActual == int(diaFin):
                flgFin = True

            # Paso 2: Creamos las URLs
            
            auxStr = "{0}/{1}{2}0{3}" if mesActual < 10 else "{0}/{1}{2}{3}"
            auxStr += "{2}0{4}/" if diaActual < 10 else "{2}0{4}/"
            # Sección unicamente para crear URLs del 20Minutos
            if not self.listado:
                auxStr += "{5}"
                url = auxStr.format(    self.directorio,
                                        str(anioActual),
                                        self.separadorFecha,
                                        str(self.mesActual),
                                        str(self.diaActual),
                                        self.archivo)
                listURLs.append(url)
            else:
                # Sección para crear URLs de ElPais, ElMundo y ElConfidecial
                if self.nombre != "MARCA":  
                    for edicion in self.ediciones:
                        auxStr += "{5}/{6}"
                        url = auxStr.format(    self.directorio,
                                                str(anioActual),
                                                self.separadorFecha,
                                                str(mesActual),
                                                str(diaActual),
                                                edicion,
                                                self.archivo)
                        listURLs.append(url)
                # Sección unicamente para crear URLs del Marca
                else:
                    for edicion in self.ediciones:
                        auxStr += "index_{5}.html"
                        url = auxStr.format(    self.directorio,
                                                str(self.anioActual),
                                                self.separadorFecha,
                                                str(self.mesActual),
                                                str(self.diaActual),
                                                edicion)
                        listURLs.append(url)

            # Paso 3: Avanzamos en un día 

            diaActual += 1

            if diaActual > diccMeses[mesActual]:
                diaActual = 1
                mesActual += 1
                
                if mesActual > 12:
                    mesActual = 1
                    anioActual +=1            

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

        edPeriodoDia = ['m', 't', 'n']
        edNumero = ['1', '2']

        # URLS => https://elpais.com/hemeroteca/elpais/YYYY/MM/dd/[m,t,n]/portada.html
        if self.nombre == "EL_PAIS":
            
            self.directorio = "datos_EL_PAIS"
            self.dominio = "https://elpais.com/hemeroteca/elpais"
            self.archivo = "portada.html"
            self.separadorFecha = "/"
            self.ediciones = edPeriodoDia

        # URLS => https://www.elmundo.es/elmundo/hemeroteca/YYYY/MM/dd/[m,t,n]/index.html
        elif self.nombre == "EL_MUNDO":
            
            self.directorio = "datos_EL_MUNDO"
            self.dominio = "https://www.elmundo.es/elmundo/hemeroteca"
            self.archivo = "index.html"
            self.separadorFecha = "/"
            self.ediciones = edPeriodoDia

        # URLS => https://www.20minutos.es/archivo/YYYY/MM/dd/
        elif self.nombre == "20_MINUTOS":
            
            self.directorio = "datos_20_MINUTOS"
            self.dominio = "https://www.20minutos.es/archivo"
            self.archivo = ""
            self.separadorFecha = "/"
            self.ediciones = []

        # URLS => https://www.elconfidencial.com/hemeroteca/YYYY-MM-dd/[1,2]/
        elif self.nombre == "EL_CONFIDENCIAL":
            
            self.directorio = "datos_EL_CONFIDENCIAL"
            self.dominio = "https://www.elconfidencial.com/hemeroteca"
            self.archivo = ""
            self.separadorFecha = "-"
            self.ediciones = edNumero

        # URLS => https://www.marca.com/hemeroteca/YYYY/MM/dd/index_[m,t,n].html
        elif self.nombre == "MARCA":
            
            self.directorio = "datos_MARCA"
            self.dominio = "https://www.marca.com/hemeroteca"
            self.archivo = ""
            self.separadorFecha = "/"
            self.ediciones = edPeriodoDia