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
XPATH_NOTICIA_CATEGORIA_TIER1 = '//li[@class="selected"]/a/span/text()'
XPATH_NOTICIA_CATEGORIA_TIER2 = '//li[contains(@class,"selected")]/h1/a/text()'
XPATH_NOTICIA_RESUMEN = '//div[@class="article-intro "]/div/ul/li' 
XPATH_NOTICIA_AUTORES = '//span[@class="article-author"]//text()'
XPATH_NOTICIA_LOCALIZACIONES = ''   # En este periódico no viene la localización de donde proviene la noticia
XPATH_NOTICIA_FECHA_PUBLICACION = '//span[@class="article-date"]/a/text()'
XPATH_NOTICIA_FOTO_PIE = '//figure[@class="image"]/div/figcaption/text()' 
XPATH_NOTICIA_FOTO_FIRMA = '//figure[@class="image"]/div/span[@class="author "]/text()'
XPATH_NOTICIA_CUERPO = '//div[@class="article-text"]/p'
XPATH_NOTICIA_TAGS_TIER1 = '//ul[@class="section-menu section-menu-small"]/li[@itemprop="name"][not(@class="selected")]//text()'
XPATH_NOTICIA_TAGS_TIER2 = '//li[@class="tag"]//text()'

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

    def __init__(self, anio=None, mes=None, dia=None, strFile=None, *args, **kwargs):

        if anio == None or mes == None:
            self.logger.error(  "Error en los parámetros, pruebe: \n\t" + 
                                "scrapy crawl testPeriodicos -a anio=YYYY -a mes=MM [dia=dd strFile=str]")
            raise CloseSpider("Error de parámetros")

        super(Spider_20Minutos, self).__init__(*args, **kwargs)

        self.periodico = Periodico("20_MINUTOS", anio, int(mes), dia)

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
            if categoria != "\n" and categoria != "\t\n":
                item['categoriaNoticia'].append(categoria)
        try:        
            categoriasTier2 = response.xpath(XPATH_NOTICIA_CATEGORIA_TIER2).extract()
            for categoria in categoriasTier2:
                item['categoriaNoticia'].append(categoria)
        except:
            pass
        
        listPartesResumen = response.xpath(XPATH_NOTICIA_RESUMEN).extract()
        strResumen = "".join(listPartesResumen)
        strResumen = TAG_RE.sub('', strResumen)
        item['resumenNoticia'] = strResumen
        
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        for autor in autores:
            item['autorNoticia'].append(autor)
        
        item['localizacionNoticia'] = []

        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]
        
        try:
            item['pieDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()[0]
            item['firmaDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_FIRMA).extract()[0]
        except:
            item['pieDeFotoNoticia'] = ""
            item['firmaDeFotoNoticia'] = ""

        listPartesCuerpo = response.xpath(XPATH_NOTICIA_CUERPO).extract()
        cuerpoNoticia = "\r\n".join(listPartesCuerpo)
        cuerpoNoticia = TAG_RE.sub('', cuerpoNoticia)
        item['cuerpoNoticia'] = cuerpoNoticia

        item['tagsNoticia'] = []
        tagsNoticia = response.xpath(XPATH_NOTICIA_TAGS_TIER1).extract()
        for tag in tagsNoticia:
            if "más" not in tag.encode('utf-8'):
                item['tagsNoticia'].append(tag)

        tagsRelativosNoticia = response.xpath(XPATH_NOTICIA_TAGS_TIER2).extract()
        for tag in tagsRelativosNoticia:
            item['tagsNoticia'].append(tag.strip())
        
        #self.newsCount+=1
        if self.newsCount > 10:
            raise CloseSpider("Noticias de test recogidas")

        yield item

    