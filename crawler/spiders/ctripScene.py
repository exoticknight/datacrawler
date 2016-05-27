# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector

from crawler.items import SceneItem


class CtripSceneSpider(Spider):
    name = 'ctripScene'
    start_urls = [u'http://you.ctrip.com/sight/hangzhou14.html']

    def parse(self, response):
        page_count = response.css('.numpage::text').extract()[0]
        for i in range(1, int(page_count)+1):
            yield Request('http://you.ctrip.com/sight/hangzhou14/s0-p{0}.html'.format(i), self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)

        for result_node in sel.css('.list_mod2 .rdetailbox'):
            item = SceneItem()

            item['cityid'] = 1
            item['name'] = result_node.css('dt a::attr(title)').extract()[0]
            item['address'] = result_node.css('.ellipsis::text')[0].extract().strip()
            item['level'] = result_node.css('dd:nth-of-type(2)::text')[0].extract().strip()
            item['tips'] = u'http://you.ctrip.com' + result_node.css('dt a::attr(href)').extract()[0]

            yield item
