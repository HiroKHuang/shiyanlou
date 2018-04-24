#-*- coding: utf-8 -*-
import scrapy

class MultipageCourseItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()

