# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector

from crawler.items import CtripAirlineItem

from crawler.metadata.cityAirline import citys

from datetime import date

round_url = u'http://english.ctrip.com/chinaflights/guangzhou-to-shanghai/tickets-can-sha/?flighttype=d&dcity=can&acity=sha&startdate=2016-06-01&returndate=2016-06-10&searchboxArg=t'

single_url_template = u'http://english.ctrip.com/chinaflights/{0}-to-{1}/tickets-{2}-{3}/?flighttype=s&dcity={2}&acity={3}&startdate={6}&searchboxArg=t#dname={4}/#aname={5}'

def make_urls(go_date,back_date,start=u'广州'):
    urls = []

    dcity = citys.get(start)
    for k,v in citys.items():
        if k != start:
            urls.append(single_url_template.format(dcity[u'enName'],v[u'enName'],dcity[u'code'],v[u'code'],dcity[u'cnName'],v[u'cnName'],go_date.strftime('%Y-%m-%d')))
            urls.append(single_url_template.format(v[u'enName'],dcity[u'enName'],v[u'code'],dcity[u'code'],v[u'cnName'],dcity[u'cnName'],back_date.strftime('%Y-%m-%d')))

    return urls

go = {
   'year': 2016,
    'month': 6,
   'date': 1
}

back = {
   'year': 2016,
   'month': 6,
   'date': 10
}

class CtripAirlineSpider(Spider):
    name = 'ctripAirline'
    go_date = date(go['year'],go['month'],go['date'])
    back_date = date(back['year'],back['month'],back['date'])
    start_urls = make_urls(start=u'广州',go_date=go_date,back_date=back_date)

    def parse(self, response):
        sel = Selector(response)
        items = []

        for result_table_node in sel.css('table.result_table'):
            item = CtripAirlineItem()

            detail = result_table_node.css('.flightDt_box')
            item['airline'] = ' '.join([x.strip() for x in detail.xpath('div[@class="col_hd"]/span[@class="s_airlines"]//text()').extract()])

            bd = detail.xpath('div[@class="col_bd "]')
            item['dtime'],item['atime'] = bd.xpath('p/span[contains(@class,"column01")]/text()').extract()
            item['dcode'],item['acode'] = bd.xpath('p/span[contains(@class,"column02")]/text()').extract()
            item['dport'],item['aport'] = bd.xpath('p/span[contains(@class,"column03")]/text()').extract()
            item['ltime'] = bd.xpath('span[@class="surplus"]/text()').extract()[0]

            item['price'] = ' '.join(result_table_node.css('th.col_05 a.price').xpath('.//text()').extract())

            items.append(item)

        return items
