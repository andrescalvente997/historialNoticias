# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPeriodicos.items import item_Noticia
from scrapy.exceptions import CloseSpider
from crawlerPeriodicos.Periodico import Periodico
import re

TAG_RE = re.compile(r'<[^>]+>')

XPATH_NOTICIA_TITULO = '//head/meta[@property="og:title"]/@content'
XPATH_NOTICIA_KEYWORDS = '//head/meta[@name="keywords"]/@content'
XPATH_NOTICIA_RESUMEN = '//span[@class="subsection-type"]/text()' 
XPATH_NOTICIA_AUTORES = '//ul[@class="author"]/li[@class="author-name" or @class="author-twitter"]//text()' 
XPATH_NOTICIA_LOCALIZACIONES = '//ul[@class="author"]/li[@class="author-city"]/text()'
XPATH_NOTICIA_FECHA_PUBLICACION = '//head/meta[@name="date"]/@content'
XPATH_NOTICIA_FOTO_PIE = '//figcaption/text()'
XPATH_NOTICIA_FOTO_FIRMA = '//figcaption/span[@data-ue-author]/text()'
XPATH_NOTICIA_CUERPO = '//article/div/p'
XPATH_NOTICIA_TAGS = '//head/meta[@property="article:tag"]/@content'

class Spider_Marca(CrawlSpider):

    name = 'Spider_Marca'
    newsCount = 0
    allowed_domains = ['marca.com']
    rules = (
            Rule(
                LinkExtractor(  allow = (), 
                                restrict_xpaths = '//h2/a',
                                deny_domains = ['videos.marca.com'],
                                deny = []), 
                callback='parse_item', 
                follow = False),
        )  

    def __init__(self, anio=None, mes=None, dia=None, strFile=None, *args, **kwargs):

        if anio == None or mes == None:
            self.logger.error(  "\x1b[1;31m" +
                                "\nError en los parámetros, pruebe: \n\t" + 
                                "scrapy crawl <SPIDER> -a anio=YYYY -a mes=MM [dia=dd strFile=str]" +
                                "\033[0;m")
            raise CloseSpider("\x1b[1;31m" + "Error de parámetros" + "\033[0;m")

        super(Spider_Marca, self).__init__(*args, **kwargs)

        self.periodico = Periodico("MARCA", anio, int(mes), dia)

        if strFile == None:
            self.start_urls, self.strFile = self.periodico.crea_StartUrls()
        else:
            self.start_urls, _ = self.periodico.crea_StartUrl()
            self.strFile = strFile
    
    
    def parse_item(self, response):

        item = item_Noticia()

        # TITULAR
        item['titularNotica'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]

        # LINK
        item['linkNoticia'] = response.url
        
        # KEYWORDS
        # Las keywords se ponen con el formato ",A,B,C"
        item['keywordsNoticia'] = []
        keywords = response.xpath(XPATH_NOTICIA_KEYWORDS).extract()[0].split(",")
        for keyword in keywords:
            item['keywordsNoticia'].append(keyword.strip()) if keyword != "" else None
        
        # DESCRIPCIÓN
        item['resumenNoticia'] = response.xpath(XPATH_NOTICIA_RESUMEN).extract()[0]

        # AUTORES
        # Los autores se muestran como "A, B, C"
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        if not autores:
            item['autorNoticia'] = []
        else:    
            for autor in autores:
                item['autorNoticia'].append(autor.strip())

        # LOCALIZACIONES
        # No siempre está la localización de la noticia
        try:
            item['localizacionNoticia'] = response.xpath(XPATH_NOTICIA_LOCALIZACIONES).extract()[0]
        except:
            item['localizacionNoticia'] = ""

        # FECHA
        # Se encuentra en el interior de la noticia como "YYYY-MM-ddThh:mm:ssZ"
        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]

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
        self.newsCount+=1
        if self.newsCount > 10:
            raise CloseSpider("\x1b[1;33m" + "Noticias de test recogidas" + "\033[0;m")

        yield item

    