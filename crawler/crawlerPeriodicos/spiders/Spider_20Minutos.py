# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPeriodicos.items import item_Noticia
from scrapy.exceptions import CloseSpider
from crawlerPeriodicos.Periodico import Periodico
import re

TAG_RE = re.compile(r'<[^>]+>')

XPATH_NOTICIA_TITULO = '//h1[@class="article-title "]/text()'
XPATH_NOTICIA_KEYWORDS = '//head/meta[@name="keywords"]/@content'
XPATH_NOTICIA_RESUMEN = '//head/meta[@property="og:description"]/@content'
XPATH_NOTICIA_AUTORES = '//span[@class="article-author"]//text()'
XPATH_NOTICIA_LOCALIZACIONES = ''   # En este periódico no viene la localización de donde proviene la noticia
XPATH_NOTICIA_FECHA_PUBLICACION = '//span[@class="article-date"]/a/text()'
XPATH_NOTICIA_FOTO_PIE = '//figure[@class="image"]/div/figcaption/text()' 
XPATH_NOTICIA_FOTO_FIRMA = '//figure[@class="image"]/div/span[@class="author "]/text()'
XPATH_NOTICIA_CUERPO = '//div[@class="article-text"]/p'
XPATH_NOTICIA_TAGS = '//head/meta[@property="article:tag"]/@content'

class Spider_20Minutos(CrawlSpider):

    name = 'Spider_20Minutos'
    newsCount = 0
    allowed_domains = ['www.20minutos.es']
    rules = (
            Rule(
                LinkExtractor(  allow = (), 
                                restrict_xpaths = '//header/h1/a'), 
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
            self.periodico = Periodico( periodico = "20_MINUTOS", anio = anio, 
                                        mes = mes, dia = dia,
                                        fechaIni = fechaIni, fechaFin = fechaFin)

            if strFile == None:
                self.start_urls, self.strFile = self.periodico.crea_StartUrls()
            else:
                self.start_urls, _ = self.periodico.crea_StartUrl()
                self.strFile = strFile

        super(Spider_20Minutos, self).__init__(*args, **kwargs)
    
    
    def parse_item(self, response):

        # Ya que este periódico tiene noticias por cada autonomía, hemos restringi
        XPATH_NOTICIA_RESTRICCION_TEMA = '//ul[contains(@class,"section-menu-small")]/li[@itemprop="name"]/h1/a/text()'
        temasSeleccionados = ["Economía", "Internacional", "Nacional"]
        try:
            tema = response.xpath(XPATH_NOTICIA_RESTRICCION_TEMA).extract()[0].strip()
            if tema not in temasSeleccionados:
                return
        except:
            return

        item = item_Noticia()

        # TITULAR
        item['titularNotica'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]

        # LINK
        item['linkNoticia'] = response.url

        # KEYWORDS
        # Las keywords se ponen con el formato "A,B,C, D, E,"
        item['keywordsNoticia'] = []
        keywords = response.xpath(XPATH_NOTICIA_KEYWORDS).extract()[0].split(",")
        for keyword in keywords:
            if keyword != "":
                item['keywordsNoticia'].append(keyword.strip())

        # DESCRIPCIÓN
        listPartesResumen = response.xpath(XPATH_NOTICIA_RESUMEN).extract()
        strResumen = "".join(listPartesResumen)
        strResumen = TAG_RE.sub('', strResumen)
        item['resumenNoticia'] = strResumen

        # AUTORES
        # Los autores se muestran en tags diferentes
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        for autor in autores:
            autor = autor.strip()
            if autor != "" and autor != "\n":
                item['autorNoticia'].append(autor)

        # LOCALIZACIONES
        # En este periódico no se muestra de donde procede la noticia
        item['localizacionNoticia'] = []

        # FECHA
        # Se encuentra en el interior de la noticia como "dd.MM.YYYY - hh:mmh"
        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]
        
        # PIE DE FOTO
        # Algunas noticias no tienen foto        
        try:
            item['pieDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()[0]
        except:
            item['pieDeFotoNoticia'] = ""
        
        # FIRMA DE FOTO
        # Algunas fotos no tienen firma 
        try:
            item['firmaDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_FIRMA).extract()[0]
        except:
            item['firmaDeFotoNoticia'] = ""
        
        # CUERPO
        listPartesCuerpo = response.xpath(XPATH_NOTICIA_CUERPO).extract()
        cuerpoNoticia = "\r\n".join(listPartesCuerpo)
        cuerpoNoticia = TAG_RE.sub('', cuerpoNoticia)
        item['cuerpoNoticia'] = cuerpoNoticia

        # TAGS
        # Los tags se separan en etiquetas diferentes
        item['tagsNoticia'] = []
        tagsNoticia = response.xpath(XPATH_NOTICIA_TAGS).extract()
        for tag in tagsNoticia:
            item['tagsNoticia'].append(tag.strip())

        # ZONA DE TEST
        #self.newsCount+=1
        if self.newsCount > 10:
            raise CloseSpider("\x1b[1;33m" + "Noticias de test recogidas" + "\033[0;m")

        yield item

    