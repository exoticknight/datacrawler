# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class CtripAirlineItem(Item):
    airline = Field()
    dcode = Field()
    dport = Field()
    dtime = Field()
    acode = Field()
    aport = Field()
    atime = Field()
    ltime = Field()
    price = Field()


class CtripTrainItem(Item):
    train = Field()
    dname = Field()
    dport = Field()
    dtime = Field()
    aname = Field()
    aport = Field()
    atime = Field()
    ltime = Field()
    price = Field()


class SceneItem(Item):
    cityid = Field()
    name = Field()
    tips = Field()
    lat = Field()
    lon = Field()
    des = Field()
    fee = Field()
    province = Field()
    district = Field()
    street = Field()
    address = Field()
    tags = Field()
    keywords = Field()
    level = Field()
    is_block = Field()

class RouteItem(Item):
    scenes = Field()