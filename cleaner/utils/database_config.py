# -*- coding: utf-8 -*-
from data_handler import Model, Field


class Scene(Model):
    db_table = 'scenelist'
    id = Field()
    name = Field()
    lat = Field()
    lng = Field()
    des = Field()
    fee = Field()
    province = Field()
    cityid = Field()
    district = Field()
    street = Field()
    address = Field()
    tags = Field()
    keywords = Field()
    level = Field()
    isblock = Field()
    tips = Field()


CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'passwd': 'usbw',
    'db': 'travelagent',
    'charset': 'utf8'
}