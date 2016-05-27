# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector

from crawler.items import SceneItem


class LotourSceneSpider(Spider):
    name = 'lotourScene'
    start_urls = [u'http://hangzhou.lotour.com/jingqu/']

    def parse(self, response):
        page_count = response.css('.bd_page a:nth-last-of-type(1)::text').extract()[0]
        for i in range(1, int(page_count)+1):
            yield Request('http://hangzhou.lotour.com/jingqu-' + str(i), self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)

        for result_node in sel.css('.jq-list-con'):
            item = SceneItem()

            item['cityid'] = 1
            item['name'] = result_node.css('.jq-name > a::text').extract()[0]
            item['tips'] = result_node.css('.jq-name > a::attr(href)').extract()[0]

            yield item
