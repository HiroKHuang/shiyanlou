# -*- coding: utf-8 -*-
import scrapy

class CourseImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()



