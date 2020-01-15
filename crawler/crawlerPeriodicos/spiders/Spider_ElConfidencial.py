# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPeriodicos.items import item_Noticia
from scrapy.exceptions import CloseSpider
from crawlerPeriodicos.Periodico import Periodico
import re

TAG_RE = re.compile(r'<[^>]+>')

XPATH_NOTICIA_TITULO = '//h1/text()'
XPATH_NOTICIA_CATEGORIA = '//strong[@itemprop="title"]/text()'
XPATH_NOTICIA_RESUMEN = '//h2[@class="news-header-opening-txt"]/text()' 
XPATH_NOTICIA_AUTORES = '//a[@class="news-def-author"]/text()'
XPATH_NOTICIA_LOCALIZACIONES = '' # Este periódico no informa de donde procede la noticia
XPATH_NOTICIA_FECHA_PUBLICACION = '//time[@class="news-def-date"]/span[@class="date-act"]/text()'
XPATH_NOTICIA_FOTO_PIE = '//figcaption[@class="news-header-img-caption"]/text()' # Aqui puede haber varias fotos a parte de la principal
XPATH_NOTICIA_FOTO_FIRMA = '' # En este periódico, la firma viene dentro del texto del pie de foto
XPATH_NOTICIA_CUERPO = '//div[contains(@class, "news-body-center")]//p' # Pierdo algunos entre-títulos
XPATH_NOTICIA_TAGS = '//h3[@class="news-def-tags"]/a/text()' # Se podrían sacar más tags de la URL

class Spider_ElMundo(CrawlSpider):

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


    def __init__(self, anio=None, mes=None, dia=None, strFile=None, *args, **kwargs):

        if anio == None or mes == None:
            self.logger.error(  "Error en los parámetros, pruebe: \n\t" + 
                                "scrapy crawl testPeriodicos -a anio=YYYY -a mes=MM [dia=dd strFile=str]")
            raise CloseSpider("Error de parámetros")

        super(Spider_ElMundo, self).__init__(*args, **kwargs)

        self.periodico = Periodico("EL_CONFIDENCIAL", anio, int(mes), dia)

        if strFile == None:
            self.start_urls, self.strFile = self.periodico.crea_StartUrls()
        else:
            self.start_urls, _ = self.periodico.crea_StartUrl()
            self.strFile = strFile
    
    
    def parse_item(self, response):

        item = item_Noticia()

        try:
            item['titularNotica'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]
        except:
            return

        item['linkNoticia'] = response.url
        
        item['categoriaNoticia'] = []
        categoria = response.xpath(XPATH_NOTICIA_CATEGORIA).extract()
        item['categoriaNoticia'] = categoria      
        
        item['resumenNoticia'] = response.xpath(XPATH_NOTICIA_RESUMEN).extract()
        
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        for autor in autores:
                item['autorNoticia'].append(autor)
            
        item['localizacionNoticia'] = []

        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]
        
        try:
            pieDeFoto = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()[0].strip()
            item['pieDeFotoNoticia'] = pieDeFoto.split(". (")[0] + "."
            item['firmaDeFotoNoticia'] = pieDeFoto.split(". (")[1][:-1]
        except:
            item['pieDeFotoNoticia'] = ""
            item['firmaDeFotoNoticia'] = ""
        
        listPartesCuerpo = response.xpath(XPATH_NOTICIA_CUERPO).extract()
        print("\n\n")
        print(listPartesCuerpo)
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

    