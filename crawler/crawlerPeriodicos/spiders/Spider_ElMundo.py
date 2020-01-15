# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPeriodicos.items import item_Noticia
from scrapy.exceptions import CloseSpider
from crawlerPeriodicos.Periodico import Periodico
import re

TAG_RE = re.compile(r'<[^>]+>')

XPATH_NOTICIA_TITULO = '//h1[contains(@class,"js-headline")]/text()'
XPATH_NOTICIA_CATEGORIA_TIER1 = '//div[@class="ue-c-article__kicker"]//text()'
XPATH_NOTICIA_CATEGORIA_TIER2 = '//li[@itemprop="itemListElement"]//span[@itemprop="name"]/text()'
XPATH_NOTICIA_RESUMEN = '//p[@class="ue-c-article__standfirst"]/text()' 
XPATH_NOTICIA_AUTORES = '//div[@class="ue-c-article__byline-name"]/text()'
XPATH_NOTICIA_LOCALIZACIONES = '//div[@class="ue-c-article__byline-location"]/text()'
XPATH_NOTICIA_FECHA_PUBLICACION = '//div//time/@datetime'
XPATH_NOTICIA_FOTO_PIE = '//span[@class="ue-c-article__media-description"]/text()'
XPATH_NOTICIA_FOTO_FIRMA = '//span[@class="ue-c-article__media-author"]/text()'
XPATH_NOTICIA_CUERPO = '//div[@class="ue-l-article__body ue-c-article__body"]/p'
XPATH_NOTICIA_TAGS = '//li[@class="ue-c-article__tags-item"]//text()'

class Spider_ElMundo(CrawlSpider):

    name = 'Spider_ElMundo'
    newsCount = 0
    allowed_domains = ['www.elmundo.es']
    rules = (
            Rule(
                LinkExtractor(  allow = (), 
                                restrict_xpaths = '//header[contains(@class,"head")]/a',
                                deny=([ "[A-Za-z-0-9]*/en-directo", "papel", "album", "loc",
                                        "metropoli", "blogs"])), 
                callback='parse_item', 
                follow = False),
        )  

    def __init__(self, anio=None, mes=None, dia=None, strFile=None, *args, **kwargs):

        if anio == None or mes == None:
            self.logger.error(  "Error en los parámetros, pruebe: \n\t" + 
                                "scrapy crawl testPeriodicos -a anio=YYYY -a mes=MM [dia=dd strFile=str]")
            raise CloseSpider("Error de parámetros")

        super(Spider_ElMundo, self).__init__(*args, **kwargs)

        self.periodico = Periodico("EL_MUNDO", anio, int(mes), dia)

        if strFile == None:
            self.start_urls, self.strFile = self.periodico.crea_StartUrls()
        else:
            self.start_urls, _ = self.periodico.crea_StartUrl()
            self.strFile = strFile
    
    
    def parse_item(self, response):

        item = item_Noticia()

        item['titularNotica'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]

        item['linkNoticia'] = response.url

        item['categoriaNoticia'] = []
        categoriasTier1 = response.xpath(XPATH_NOTICIA_CATEGORIA_TIER1).extract()
        for categoria in categoriasTier1:
            item['categoriaNoticia'].append(categoria.strip())
        categoriasTier2 = response.xpath(XPATH_NOTICIA_CATEGORIA_TIER2).extract()[1:]
        for categoria in categoriasTier2:
            item['categoriaNoticia'].append(categoria)        
        
        item['resumenNoticia'] = response.xpath(XPATH_NOTICIA_RESUMEN).extract()
        if not item['resumenNoticia']:
            item['resumenNoticia'] = ""
        
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        if not autores:
            item['autorNoticia'] = ["EL_MUNDO"]
        else:
            for autor in autores:
                item['autorNoticia'].append(autor)
            
        item['localizacionNoticia'] = []
        localizaciones = response.xpath(XPATH_NOTICIA_LOCALIZACIONES).extract()
        for localizacion in localizaciones:
            item['localizacionNoticia'].append(localizacion)

        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]
        
        try:
            item['pieDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()[0].strip()
            item['firmaDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_FIRMA).extract()[0].strip()
        except:
            item['pieDeFotoNoticia'] = ""
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

    