# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPeriodicos.items import item_Noticia
from scrapy.exceptions import CloseSpider
from crawlerPeriodicos.Periodico import Periodico
import re
import dateutil.parser
import pytz

TAG_RE = re.compile(r'<[^>]+>')

XPATH_NOTICIA_TITULO = '//head/meta[@property="og:title"]/@content'
XPATH_NOTICIA_KEYWORDS = '//head/meta[@name="keywords"]/@content'
XPATH_NOTICIA_RESUMEN = '//head/meta[@property="og:description"]/@content' 
XPATH_NOTICIA_AUTORES = '//head/meta[@name="author"]/@content' 
XPATH_NOTICIA_LOCALIZACIONES = '//span[@class="articulo-localizaciones"]/span[@class="articulo-localizacion"]/text()'
XPATH_NOTICIA_FECHA_PUBLICACION = '//head/meta[@name="date"]/@content'
XPATH_NOTICIA_FOTO_PIE = '//span[@class="foto-texto"]/text()'
XPATH_NOTICIA_FOTO_FIRMA = '//span[@class="foto-firma"]/span[@itemprop="author"][@class="foto-autor"]/text()'
XPATH_NOTICIA_CUERPO = '//div[@class="articulo-cuerpo"]/p'
XPATH_NOTICIA_TAGS = '//div[@class="articulo-tags__interior"]/ul/li[@itemprop="keywords"]/a/text()'

XPATH_NOTICIAS_REGISTRO = '//div[contains(@class,"test-registro")]'

class Spider_ElPais(CrawlSpider):

    name = 'Spider_ElPais'
    newsCount = 0
    allowed_domains = ['elpais.com']
    rules = (
            Rule(
                LinkExtractor(  allow = (), 
                                restrict_xpaths = '//h2[@class="articulo-titulo"]/a',
                                deny_domains = ['motor.elpais.com', 'verne.elpais.com', 'colecciones.elpais.com', 
                                                'aprendemosjuntos.elpais.com', 'librotea.elpais.com', 'descuentos.elpais.com',
                                                'elcomidista.elpais.com', 'smoda.elpais.com', 'suscripciones.elpais.com',
                                                'elfuturoesapasionante.elpais.com', 'escuela.elpais.com', 'cat.elpais.com',
                                                'plus.elpais.com', 'elviajero.elpais.com', 'retina.elpais.com', 'cincodias.elpais.com'],
                                deny = ["especiales", "tematicos"]), 
                callback='parse_item', 
                follow = False),
        )  

    def __init__(self, anio=None, mes=None, dia=None, strFile=None, fechaIni=None, fechaFin=None, *args, **kwargs):

        flgParametrosMal = True
        # Con esto nos aseguramos que estamos metiendo bien los parámetros y no los mezclamos 
        if ((anio!=None and mes!=None and fechaIni==None and fechaFin==None) or (anio==None and mes==None and dia==None and fechaIni!=None and fechaFin!=None)):
            flgParametrosMal = False

        if flgParametrosMal == True:
            self.logger.error(  "\x1b[1;31m" +
                                "\nError en los parámetros, pruebe: \n\t" + 
                                "scrapy crawl <SPIDER> -a anio=YYYY -a mes=MM [dia=dd strFile=str]\n" +
                                "o bien: \n\t" +
                                'scrapy crawl <SPIDER> -a fechaIni="dd-MM-YYYY" -a fechaFin="dd-MM-YYYY"' +
                                "\033[0;m")
            self.start_urls = []
            self.strFile = ""

        else:
            
            self.periodico = Periodico( periodico = "EL_PAIS", anio = anio, 
                                        mes = mes, dia = dia,
                                        fechaIni = fechaIni, fechaFin = fechaFin)

            if strFile == None:
                self.start_urls, self.strFile = self.periodico.crea_StartUrls()
            else:
                self.start_urls, _ = self.periodico.crea_StartUrls()
                self.strFile = strFile

        super(Spider_ElPais, self).__init__(*args, **kwargs)
    
    
    def parse_item(self, response):

        # Comprobamos que la noticia esté entera y no tengamos 
        # que estar registrados para verla completa
        if len(response.xpath(XPATH_NOTICIAS_REGISTRO).extract()) != 0:
            return

        item = item_Noticia()

        # TITULAR
        item['titularNoticia'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]

        # LINK
        item['linkNoticia'] = response.url

        # KEYWORDS
        # Las keywords se ponen con el formato "A, B, C"
        item['keywordsNoticia'] = []
        keywords = response.xpath(XPATH_NOTICIA_KEYWORDS).extract()[0].split(",")
        for keyword in keywords:
            item['keywordsNoticia'].append(keyword.strip())

        # DESCRIPCIÓN
        item['resumenNoticia'] = response.xpath(XPATH_NOTICIA_RESUMEN).extract()[0]

        # AUTORES
        # Los autores se muestran como "A, B, C"
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()[0].split(",")
        for autor in autores:
            item['autorNoticia'].append(autor.strip())

        # LOCALIZACIONES
        # Se muestran en el formato "Madrid\n/ \nFrancia"
        try:
            strLocalizacion = response.xpath(XPATH_NOTICIA_LOCALIZACIONES).extract()[0]
            strLocalizacion = strLocalizacion.replace("\n", "")
            localizaciones = strLocalizacion.split("/ ")
            item['localizacionNoticia'] = []
            for localizacion in localizaciones:
                item['localizacionNoticia'].append(localizacion)
        except:
            item['localizacionNoticia'] = []

        # FECHA
        # Se encuentra en el interior de la noticia como "YYYY-MM-ddThh:mm:ss+01:00"
        # Tenemos que pasar de la fecha en ISO 8601 a RFC 3339
        strFecha = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]
        datetime = dateutil.parser.parse(strFecha).astimezone(pytz.timezone('UTC'))
        item['fechaPublicacionNoticia'] = datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

        # PIE DE FOTO
        try:
            item['pieDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()[0]
        except:
            item['pieDeFotoNoticia'] = ""

        # FIRMA DE FOTO
        try:    
            item['firmaDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_FIRMA).extract()[0]
        except:
            item['firmaDeFotoNoticia'] = ""

        # CUERPO
        listPartesCuerpo = response.xpath(XPATH_NOTICIA_CUERPO).extract()
        cuerpoNoticia = "".join(listPartesCuerpo)
        cuerpoNoticia = TAG_RE.sub('', cuerpoNoticia)
        item['cuerpoNoticia'] = cuerpoNoticia

        # TAGS
        item['tagsNoticia'] = []
        tagsNoticia = response.xpath(XPATH_NOTICIA_TAGS).extract()
        for tag in tagsNoticia:
            item['tagsNoticia'].append(tag)

        # ZONA DE TEST
        #self.newsCount+=1
        if self.newsCount > 10:
            raise CloseSpider("\x1b[1;33m" + "Noticias de test recogidas" + "\033[0;m")

        yield item

    