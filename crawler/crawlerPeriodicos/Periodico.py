# -*- coding: utf-8 -*-

from os.path import abspath, dirname

class Periodico():

    def __init__(self, periodico, anio, mes, dia, fechaIni, fechaFin):
        
        self.nombre = periodico
        self.anio = anio if isinstance(anio, int) or anio==None else int(anio)
        self.mes = mes if isinstance(mes, int) or mes==None else int(mes)
        self.dia = dia if isinstance(dia, int) or dia==None else int(dia)
        self.fechaIni = fechaIni
        self.fechaFin = fechaFin
        
        self.initVarsURLs()


    def crea_StartUrls(self):

        diccMeses = {   1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 
                        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        # El rango de fechas NO ha sido introducido directamente
        if self.fechaIni == None and self.fechaFin == None:
            auxStr = "{0}{1}{2}{1}{3}"
            # Si el usuario ha intoducido el año, mes y dia a analizar,
            # inicializaremos los rangos con la misma fecha
            if self.dia != None:
                self.fechaIni = auxStr.format(  str(self.dia),
                                                "-",
                                                str(self.mes),
                                                str(self.anio))
                self.fechaFin = self.fechaIni
            # Si el usuario NO ha introducido el día, tenemos que coger
            # todo el mes de noticias de año especificado
            else:
                self.fechaIni = auxStr.format(  "01",
                                                "-",
                                                str(self.mes),
                                                str(self.anio))
                self.fechaFin = auxStr.format(  str(diccMeses[self.mes]),
                                                "-",
                                                str(self.mes),
                                                str(self.anio))
        
        listURLs, strFile = self.crea_StartUrls_dateRange()                

        strFile = dirname(abspath(__file__)) + "/" + strFile

        return listURLs, strFile


    def crea_StartUrls_dateRange(self):

        listURLs = []
        # Diccionario k(numero mes): v(numero de dias del mes)
        diccMeses = {   1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 
                        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        diaIni, mesIni, anioIni = self.fechaIni.split("-")
        diaFin, mesFin, anioFin = self.fechaFin.split("-")

        auxStr = "{}/{}0{}" if int(mesIni) < 10 else "{}/{}{}"
        auxStr += "0{}_" if int(diaIni) < 10 else "{}_"
        auxStr += "{}0{}" if int(mesFin) < 10 else "{}{}"
        auxStr += "0{}_" if int(diaFin) < 10 else "{}_"
        auxStr += "noticias.json"
        strFile = auxStr.format(    self.directorio,
                                    str(int(anioIni)),
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
            auxStr += "{2}0{4}/" if diaActual < 10 else "{2}{4}/"
            # Sección unicamente para crear URLs del 20Minutos
            if not self.ediciones:
                _auxStr = auxStr + "{5}"
                url = _auxStr.format(   self.dominio,
                                        str(anioActual),
                                        self.separadorFecha,
                                        str(mesActual),
                                        str(diaActual),
                                        self.archivo)
                listURLs.append(url)
            else:
                # Sección para crear URLs de ElPais, ElMundo y ElConfidecial
                if self.nombre != "MARCA":  
                    for edicion in self.ediciones:
                        _auxStr = auxStr + "{5}/{6}"
                        url = _auxStr.format(   self.dominio,
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
                        _auxStr = auxStr + "index_{5}.html"
                        url = _auxStr.format(   self.dominio,
                                                str(anioActual),
                                                self.separadorFecha,
                                                str(mesActual),
                                                str(diaActual),
                                                edicion)
                        listURLs.append(url)

            # Paso 3: Avanzamos en un día 

            # Así nos saltamos el último paso ya que no es necesario
            if flgFin == True:
                continue

            diaActual += 1

            if diaActual > diccMeses[mesActual]:
                diaActual = 1
                mesActual += 1
                
                if mesActual > 12:
                    mesActual = 1
                    anioActual += 1            

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