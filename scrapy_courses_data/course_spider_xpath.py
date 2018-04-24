# -*- coding:utf-8 -*-

import scrapy

class CourseSpider(scrapy.Spider):
    name = 'shiyanlou-courses'

    @property
    def start_urls(self):
        url_tmp = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmp.format(i) for i in range(1, 25))

    def parse(self, response):
        for course in response.xpath('//div[@class="course-body"]'):
            yield {
                'name': course.xpath('.//div[@class="course-name"]/text()').extract_first(),
                'descript': course.xpath('.//div[@class="course-desc"]/text()').extract_first(),
                'numbers': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d+)[^\d]*')
                }
