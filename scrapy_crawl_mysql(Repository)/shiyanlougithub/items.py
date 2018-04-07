# -*- coding: utf-8 -*-

import scrapy

class ShiyanlougithubItem(scrapy.Item):
    name = scrapy.Field()
    update_time = scrapy.Field()
   
