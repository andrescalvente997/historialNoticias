# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPeriodicos.items import item_Noticia
from scrapy.exceptions import CloseSpider
from crawlerPeriodicos.Periodico import Periodico
import re
import sys

TAG_RE = re.compile(r'<[^>]+>')

XPATH_NOTICIA_TITULO = '//head/meta[@property="og:title"]/@content'
XPATH_NOTICIA_KEYWORDS = '//head/meta[@name="keywords"]/@content'
XPATH_NOTICIA_RESUMEN = '//head/meta[@property="og:description"]/@content'
XPATH_NOTICIA_AUTORES = '//a[@class="news-def-author"]/text()'
XPATH_NOTICIA_LOCALIZACIONES = '' # Este periódico no informa de donde procede la noticia, suelen estar en el autor.
XPATH_NOTICIA_FECHA_PUBLICACION = '//head/meta[@name="article:published_time"]/@content'
XPATH_NOTICIA_FOTO_PIE = '//figcaption[@class="news-header-img-caption"]/text()' # Aqui puede haber varias fotos a parte de la principal
XPATH_NOTICIA_FOTO_FIRMA = '' # En este periódico, la firma suele venir dentro del texto del pie de foto. 
XPATH_NOTICIA_CUERPO = '//div[contains(@class, "news-body-center")]//*[self::p or self::h4]'
XPATH_NOTICIA_TAGS = '//h3[@class="news-def-tags"]/a/text()' # Se podrían sacar más tags de la URL

class Spider_ElConfidencial(CrawlSpider):

    name = 'Spider_ElConfidencial'
    newsCount = 0
    allowed_domains = ['www.elconfidencial.com']
    rules = (
            Rule(
                LinkExtractor(  allow = (), 
                                restrict_xpaths = '//h3[@typetitle="tsmall" or @typetitle="tnormal"]/a',
                                deny=(["fichas"])), 
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
            
            self.periodico = Periodico( periodico = "EL_CONFIDENCIAL", anio = anio, 
                                        mes = mes, dia = dia,
                                        fechaIni = fechaIni, fechaFin = fechaFin)

            if strFile == None:
                self.start_urls, self.strFile = self.periodico.crea_StartUrls()
            else:
                self.start_urls, _ = self.periodico.crea_StartUrl()
                self.strFile = strFile

        super(Spider_ElConfidencial, self).__init__(*args, **kwargs)
    
    def parse_item(self, response):

        item = item_Noticia()

        # TITULAR
        item['titularNoticia'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]

        # LINK
        item['linkNoticia'] = response.url

        # KEYWORDS
        # Las keywords se ponen con el formato "A,B,C"
        item['keywordsNoticia'] = []
        keywords = response.xpath(XPATH_NOTICIA_KEYWORDS).extract()[0].split(",")
        for keyword in keywords:
            item['keywordsNoticia'].append(keyword.strip())   

        # DESCRIPCIÓN
        item['resumenNoticia'] = response.xpath(XPATH_NOTICIA_RESUMEN).extract()

        # AUTORES
        # Los autores, en el caso de haber más de uno, se posicionan en tags diferentes
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        for autor in autores:
                item['autorNoticia'].append(autor.strip())

        # LOCALIZACIONES
        # No se muestran en la noticia. Hay veces que aparece con el autor, pero aparecen de esta manera:
        # Juan Pérez. Barcelona
        # Lo cuál interfiere con los nombres de autores los cuales firmán con las iniciales de su nombre y apellidos.
        # Ejemplo: J. P.
        item['localizacionNoticia'] = []

        # FECHA
        # Se encuentra en el interior de la noticia como "YYYY-MM-ddThh:mm:ssZ"
        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]

        # PIE DE FOTO
        # 3 casos: 1) No foto.  2) Pie de foto pero NO firma.  3) Pie y firma de foto
        try:
            pieDeFoto = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()[0].strip()
            item['pieDeFotoNoticia'] = pieDeFoto.split("(")[0].strip()
        except:
            item['pieDeFotoNoticia'] = ""
            item['firmaDeFotoNoticia'] = ""

        # FIRMA DE FOTO
        try:            
            item['firmaDeFotoNoticia'] = pieDeFoto.split("(")[1].split(")")[0].strip()
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

    