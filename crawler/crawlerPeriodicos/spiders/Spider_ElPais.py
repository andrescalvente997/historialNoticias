# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPeriodicos.items import item_Noticia
from scrapy.exceptions import CloseSpider
from crawlerPeriodicos.Periodico import Periodico
import re

TAG_RE = re.compile(r'<[^>]+>')

XPATH_NOTICIA_TITULO = '//h1[contains(@class,"articulo-titulo")]/text()'
XPATH_NOTICIA_CATEGORIA_TIER1 = '//a[@class="enlace"]/text()'
XPATH_NOTICIA_CATEGORIA_TIER2 = '//span/a/span[@itemprop="title"]/text()'
XPATH_NOTICIA_RESUMEN = '//h2[@class="articulo-subtitulo"]/text()' 
XPATH_NOTICIA_AUTORES = '//span[@class="autor-nombre"]/a/text()'
XPATH_NOTICIA_LOCALIZACIONES = '//span[@class="articulo-localizaciones"]/span[@class="articulo-localizacion"]/text()'
XPATH_NOTICIA_FECHA_PUBLICACION = '//time/meta[@itemprop="datePublished"]/@content'
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
                                                'elfuturoesapasionante.elpais.com', 'escuela.elpais.com', 'cat.elpais.com'],
                                deny = ["especiales", "tematicos"]), 
                callback='parse_item', 
                follow = False),
        )  

    def __init__(self, anio=None, mes=None, dia=None, strFile=None, *args, **kwargs):

        if anio == None or mes == None:
            self.logger.error(  "Error en los parámetros, pruebe: \n\t" + 
                                "scrapy crawl testPeriodicos -a anio=YYYY -a mes=MM [dia=dd strFile=str]")
            raise CloseSpider("Error de parámetros")

        super(Spider_ElPais, self).__init__(*args, **kwargs)

        self.periodico = Periodico("EL_PAIS", anio, int(mes), dia)

        if strFile == None:
            self.start_urls, self.strFile = self.periodico.crea_StartUrls()
        else:
            self.start_urls, _ = self.periodico.crea_StartUrl()
            self.strFile = strFile
    
    
    def parse_item(self, response):

        item = item_Noticia()

        print(response.xpath(XPATH_NOTICIA_TITULO).extract())

        item['titularNotica'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]

        item['linkNoticia'] = response.url

        item['categoriaNoticia'] = []
        categoriasTier1 = response.xpath(XPATH_NOTICIA_CATEGORIA_TIER1).extract()
        categoriasTier2 = response.xpath(XPATH_NOTICIA_CATEGORIA_TIER2).extract()
        for categoria in categoriasTier1:
            if categoria != "\n" and categoria != "\t\n":
                item['categoriaNoticia'].append(categoria)
        for categoria in categoriasTier2:
            item['categoriaNoticia'].append(categoria)

        try:
            item['resumenNoticia'] = response.xpath(XPATH_NOTICIA_RESUMEN).extract()[0]
        except:
            item['resumenNoticia'] = ""

        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        for autor in autores:
            item['autorNoticia'].append(autor)

        try:
            strLocalizacion = response.xpath(XPATH_NOTICIA_LOCALIZACIONES).extract()[0]
            strLocalizacion = strLocalizacion.replace("\n", "")
            localizaciones = strLocalizacion.split("/ ")
            item['localizacionNoticia'] = []
            for localizacion in localizaciones:
                item['localizacionNoticia'].append(localizacion)
        except:
            item['localizacionNoticia'] = []

        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]

        try:
            item['pieDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()[0]
        except:
            item['pieDeFotoNoticia'] = ""

        try:    
            item['firmaDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_FIRMA).extract()[0]
        except:
            item['firmaDeFotoNoticia'] = ""

        listPartesCuerpo = response.xpath(XPATH_NOTICIA_CUERPO).extract()
        cuerpoNoticia = "".join(listPartesCuerpo)
        cuerpoNoticia = TAG_RE.sub('', cuerpoNoticia)
        item['cuerpoNoticia'] = cuerpoNoticia

        item['tagsNoticia'] = []
        tagsNoticia = response.xpath(XPATH_NOTICIA_TAGS).extract()
        for tag in tagsNoticia:
            item['tagsNoticia'].append(tag)

        #self.newsCount+=1
        if self.newsCount > 10:
            raise CloseSpider("Noticias de test recogidas")

        yield item

    