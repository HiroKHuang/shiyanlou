# -*- coding:utf-8 -*-

import scrapy

class RepositorySpider(scrapy.Spider):
    name = "repository_spider"

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.xpath('//li[contains(@class, "public")]'):
            yield {
                    'name': response.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('\n\s*(.*)'),
                    'update_time': response.xpath('.//relative-time/@datetime').extract_first()
                    }
