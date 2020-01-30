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
XPATH_NOTICIA_RESUMEN = '//p[@class="ue-c-article__standfirst"]/text()' 
XPATH_NOTICIA_AUTORES = '//div[@class="ue-c-article__byline-name"]/text()'
XPATH_NOTICIA_LOCALIZACIONES = '//div[@class="ue-c-article__byline-location"]/text()'
XPATH_NOTICIA_FECHA_PUBLICACION = '//head/meta[@name="date"]/@content'
XPATH_NOTICIA_FOTO_PIE = '//span[@class="ue-c-article__media-description"]'
XPATH_NOTICIA_FOTO_FIRMA = '//span[@class="ue-c-article__media-source"]//text()'
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
            
            self.periodico = Periodico( periodico = "EL_MUNDO", anio = anio, 
                                        mes = mes, dia = dia,
                                        fechaIni = fechaIni, fechaFin = fechaFin)

            if strFile == None:
                self.start_urls, self.strFile = self.periodico.crea_StartUrls()
            else:
                self.start_urls, _ = self.periodico.crea_StartUrl()
                self.strFile = strFile

        super(Spider_ElMundo, self).__init__(*args, **kwargs)
    
    
    def parse_item(self, response):

        item = item_Noticia()

        # TITULAR
        item['titularNotica'] = response.xpath(XPATH_NOTICIA_TITULO).extract()[0]

        # LINK
        item['linkNoticia'] = response.url

        # KEYWORDS
        # Las keywords se ponen con el formato "A, B, C"
        # Keywords del tipo "A/B" -> ["A", "B"]
        # Keywords del tipo "A - B" -> ["A", "B"]
        # Keywords del tipo "A y B" -> ["A", "B"]
        item['keywordsNoticia'] = []
        keywords = response.xpath(XPATH_NOTICIA_KEYWORDS).extract()[0].split(",")
        for keyword in keywords:
            if keyword == "":
                continue
            elif "/" not in keyword and " - " not in keyword and " y " not in keyword:
                item['keywordsNoticia'].append(keyword.strip())
            else:
                print("n\n\n\n"+keyword)
                if "/" in keyword:
                    lkeyword = keyword.split("/")
                elif " - " in keyword:
                    lkeyword = keyword.split(" - ")
                elif " y " in keyword:
                    lkeyword = keyword.split(" y ")
                for k in lkeyword:
                    item['keywordsNoticia'].append(k.strip())
                   
        
        # DESCRIPCIÓN
        # Alguna noticia puede no tener resumen
        item['resumenNoticia'] = response.xpath(XPATH_NOTICIA_RESUMEN).extract()
        if not item['resumenNoticia']:
            item['resumenNoticia'] = ""
        
        # AUTORES
        # Lo obtenemos del <body> y si hay, está en tags separados
        # Si no hay autor, ponemos EL_MUNDO como default
        item['autorNoticia'] = []
        autores = response.xpath(XPATH_NOTICIA_AUTORES).extract()
        if not autores:
            item['autorNoticia'] = ["EL_MUNDO"]
        else:
            for autor in autores:
                item['autorNoticia'].append(autor)
            
        # LOCALIZACIONES
        # Lo obtenemos del <body> y si hay, está en tags separados
        item['localizacionNoticia'] = []
        localizaciones = response.xpath(XPATH_NOTICIA_LOCALIZACIONES).extract()
        for localizacion in localizaciones:
            item['localizacionNoticia'].append(localizacion)

        # FECHA
        # Se encuentra en el interior de la noticia como "YYYY-MM-ddThh:mm:ssZ"
        item['fechaPublicacionNoticia'] = response.xpath(XPATH_NOTICIA_FECHA_PUBLICACION).extract()[0]
        
        # PIE DE FOTO
        # Algunas noticias no tienen foto
        listPartesPie = response.xpath(XPATH_NOTICIA_FOTO_PIE).extract()
        pieDeFoto = "".join(listPartesPie)
        pieDeFoto = TAG_RE.sub('', pieDeFoto)
        pieDeFoto = pieDeFoto.replace("\n", "")
        item['pieDeFotoNoticia'] = pieDeFoto
        
        # FIRMA DE FOTO
        # Algunas fotos no tienen firma 
        try:
            item['firmaDeFotoNoticia'] = response.xpath(XPATH_NOTICIA_FOTO_FIRMA).extract()[0].strip()
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

    