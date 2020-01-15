# -*- coding: utf-8 -*-

class Periodico():

    def __init__(self, periodico, anio, mes, dia = None):
        
        self.nombre = periodico
        self.anio = anio
        self.mes = mes
        self.dia = dia
        
        self.initVarsURLs()


    def crea_StartUrls(self):

        listURLs = []
        periodos = ['m', 't', 'n']
        ediciones = ['1', '2']
        # Diccionario k(numero mes): v( set(dias del mes, str mes) )
        diccMeses = {   1: (31, "01"), 2: (28, "02"), 3: (31, "03"), 4: (30, "04"), 5: (31, "05"), 
                        6: (30, "06"), 7: (31, "07"), 8: (31, "08"), 9: (30, "09"), 10: (31, "10"), 
                        11: (30, "11"), 12: (31, "12")}

        if self.dia == None:                    

            rutaAnioMes = self.anio + self.separadorFecha + diccMeses[self.mes][1] + self.separadorFecha

            for i in range(diccMeses[self.mes][0]):
                if i+1 < 10:
                    rutaDia = "0" + str(i+1) + "/"
                else:
                    rutaDia = str(i+1) + "/" 

                if not self.listado: # Listado de periodos vacio
                    url = self.dominio + rutaAnioMes + rutaDia + self.archivo
                    listURLs.append(url)
                else:
                    for elemento in self.listado:
                        rutaElemento = elemento + "/"
                        url = self.dominio + rutaAnioMes + rutaDia + rutaElemento + self.archivo
                        listURLs.append(url)

            strFile = self.directorio + self.anio + "_" + diccMeses[self.mes][1] + "_noticias.json"


        else:

            if int(self.dia) < 10:
                rutaDia = self.anio + self.separadorFecha + diccMeses[self.mes][1] + self.separadorFecha + "0" + str(int(self.dia)) + "/"
                strFile = directorio + self.anio + "_" + diccMeses[self.mes][1] + "_0" + str(int(self.dia)) + "_noticias.json"
            else:
                rutaDia = self.anio + self.separadorFecha + diccMeses[self.mes][1] + self.separadorFecha + self.dia + "/"
                strFile = self.directorio + self.anio + "_" + diccMeses[self.mes][1] + "_" + self.dia + "_noticias.json"

            if not self.listado: # Listado de periodos vacio
                url = self.dominio + rutaDia + self.archivo
                listURLs.append(url)
            else:
                for elemento in self.listado:
                    rutaPeriodo = elemento + "/"
                    url = self.dominio + rutaDia + rutaPeriodo + self.archivo
                    listURLs.append(url)

        return listURLs, strFile


    def initVarsURLs(self):

        periodos = ['m', 't', 'n']
        ediciones = ['1', '2']

        # URLS => https://elpais.com/hemeroteca/elpais/YYYY/MM/dd/[m,t,n]/portada.html
        if self.nombre == "EL_PAIS":
            
            self.directorio = "datos_EL_PAIS/"
            self.dominio = "https://elpais.com/hemeroteca/elpais/"
            self.archivo = "portada.html"
            self.separadorFecha = "/"
            self.listado = periodos

        # URLS => https://www.elmundo.es/elmundo/hemeroteca/YYYY/MM/dd/[m,t,n]/index.html
        elif self.nombre == "EL_MUNDO":
            
            self.directorio = "datos_EL_MUNDO/"
            self.dominio = "https://www.elmundo.es/elmundo/hemeroteca/"
            self.archivo = "index.html"
            self.separadorFecha = "/"
            self.listado = periodos

        # URLS => https://www.20minutos.es/archivo/YYYY/MM/dd/
        elif self.nombre == "20_MINUTOS":
            
            self.directorio = "datos_20_MINUTOS/"
            self.dominio = "https://www.20minutos.es/archivo/"
            self.archivo = ""
            self.separadorFecha = "/"
            self.listado = []

        # URLS => https://www.elconfidencial.com/hemeroteca/YYYY-MM-dd/[1,2]/
        elif self.nombre == "EL_CONFIDENCIAL":
            
            self.directorio = "datos_EL_CONFIDENCIAL/"
            self.dominio = "https://www.elconfidencial.com/hemeroteca/"
            self.archivo = ""
            self.separadorFecha = "-"
            self.listado = ediciones