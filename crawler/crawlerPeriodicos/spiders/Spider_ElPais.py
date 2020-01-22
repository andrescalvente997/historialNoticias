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
XPATH_NOTICIA_RESUMEN = '//head/meta[@property="og:description"]/@content' 
XPATH_NOTICIA_AUTORES = '//head/meta[@name="author"]/@content' 
XPATH_NOTICIA_LOCALIZACIONES = '//span[@class="articulo-localizaciones"]/span[@class="articulo-localizacion"]/text()'
XPATH_NOTICIA_FECHA_PUBLICACION = '//head/meta[@name="date"]/@content'
XPATH_NOTICIA_FOTO_PIE = '//span[@class="foto-texto"]/text()'
XPATH_NOTICIA_FOTO_FIRMA = '//span[@class="foto-firma"]/span[@itemprop="author"][@class="foto-autor"]/text()'
XPATH_NOTICIA_CUERPO = '//div[@class="articulo-cuerpo"]/p'
XPATH_NOTICIA_TAGS = '//div[@class="articulo-tags__interior"]/ul/li[@itemprop="keywords"]/a/text()'

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
                                                'plus.elpais.com'],
                                deny = ["especiales", "tematicos"]), 
                callback='parse_item', 
                follow = False),
        )  

    def __init__(self, anio=None, mes=None, dia=None, strFile=None, fechaIni=None, fechaFin=None, *args, **kwargs):

        if anio == None or mes == None:
            self.logger.error(  "\x1b[1;31m" +
                                "\nError en los parámetros, pruebe: \n\t" + 
                                "scrapy crawl <SPIDER> -a anio=YYYY -a mes=MM [dia=dd strFile=str]" +
                                "\033[0;m")
            raise CloseSpider("\x1b[1;31m" + "Error de parámetros" + "\033[0;m")

        super(Spider_ElPais, self).__init__(*args, **kwargs)

        self.periodico = Periodico( periodico = "EL_PAIS", anio = anio, 
                                    mes = mes, dia = dia,
                                    fechaIni = fechaIni, fechaFin = fechaFin)

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
        #self.newsCount+=1
        if self.newsCount > 10:
            raise CloseSpider("\x1b[1;33m" + "Noticias de test recogidas" + "\033[0;m")

        yield item

    