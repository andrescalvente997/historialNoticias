# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class item_Noticia(scrapy.Item):
    
    titularNoticia = scrapy.Field()
    linkNoticia = scrapy.Field()
    keywordsNoticia = scrapy.Field()
    resumenNoticia = scrapy.Field()
    autorNoticia = scrapy.Field()
    localizacionNoticia = scrapy.Field()
    fechaPublicacionNoticia = scrapy.Field()
    pieDeFotoNoticia = scrapy.Field()
    firmaDeFotoNoticia = scrapy.Field()
    cuerpoNoticia = scrapy.Field()
    tagsNoticia = scrapy.Field()