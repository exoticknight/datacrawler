# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector

from crawler.items import CtripTrainItem

from crawler.metadata.cityTrain import citys

from datetime import date

url_template = u'http://english.ctrip.com/trains/List/Index?DepartureCity=&ArrivalCity=&TrainNo=&DepartureCityPinyin=&ArrivalCityPinyin=&DepartureStation={0}&ArrivalStation={1}&DepartDate={2}&searchboxArg='

def make_urls(go_date,back_date,start=u'广州'):
    urls = []

    dcity = citys.get(start)
    for k,v in citys.items():
        if k != start:
          urls.append(url_template.format(dcity[u'cnName'],v[u'cnName'],go_date.strftime('%m-%d-%Y')))
          urls.append(url_template.format(v[u'cnName'],dcity[u'cnName'],back_date.strftime('%m-%d-%Y')))

    return urls

go = {
   'year': 2016,
   'month': 5,
   'date': 1
}

back = {
   'year': 2016,
   'month': 5,
   'date': 10
}

class CtripTrainSpider(Spider):
    name = 'ctripTrain'
    go_date = date(go['year'],go['month'],go['date'])
    back_date = date(back['year'],back['month'],back['date'])
    start_urls = make_urls(start=u'广州',go_date=go_date,back_date=back_date)

    def __init__(self):
        self.download_delay = 3  # delay between each request

    def parse(self, response):
        sel = Selector(response)
        items = []

        import urlparse
        codes = urlparse.parse_qs(response.url)
        dname = codes['DepartureStation']
        aname = codes['ArrivalStation']

        for result_node in sel.css('.result-item'):
            item = CtripTrainItem()

            item['train'] = result_node.css('.train-num::text').extract()[0]
            item['dname'] = dname
            item['aname'] = aname
            item['dtime'] = result_node.css('.time-start::text').extract()[0]
            item['atime'] = result_node.css('.time-end::text').extract()[0]
            item['dport'] = result_node.css('.station-from::text').extract()[0]
            item['aport'] = result_node.css('.station-to::text').extract()[0]
            item['ltime'] = result_node.css('.train-duration::text').extract()[0]


            item['price'] = []
            for li in result_node.css('.train-seat').xpath('.//li'):
                item['price'].append(''.join(li.css('.c-price').xpath('.//text()').extract()[::2]))

            items.append(item)

        return items
