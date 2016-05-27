# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector

from crawler.items import RouteItem


class CtripRouteSpider(Spider):
    name = 'ctripRoute'
    start_urls = [u'http://vacations.ctrip.com/grouptravel/p5893470s32.html']

    # def parse(self, response):
    #     page_count = response.css('.numpage::text').extract()[0]
    #     for i in range(1, int(page_count)+1):
    #         yield Request('http://you.ctrip.com/sight/hangzhou14/s0-p{0}.html'.format(i), self.parse_page)

    def parse(self, response):
        sel = Selector(response)

        item = RouteItem()

        scenes = []
        day = []
        for scene in sel.css('#simple_route_div').css('span, i.day'):
            if scene.css('.day'):
                scenes.append(day)
                day = []
            else:
                day.append(scene.xpath('.//text()').extract()[0])
        if len(day):
            scenes.append(day)

        item['scenes'] = scenes

        return item
