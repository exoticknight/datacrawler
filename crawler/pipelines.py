# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
import logging

SETTINGS = get_project_settings()


def airlineHandler(tx, item):
    result = tx.execute(
    u"""INSERT INTO airline (no,dcode,dport,dtime,acode,aport,atime,ltime,price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    (item['airline'],
    item['dcode'],
    item['dport'],
    item['dtime'],
    item['acode'],
    item['aport'],
    item['atime'],
    item['ltime'],
    item['price'])
    )
    if result > 0:
        logging.log(logging.INFO, "add one airline")


def trainHandler(tx, item):
    pass


def sceneHandler(tx, item):
    result = tx.execute(
    u"""INSERT INTO scenelist (cityid,name,tips,address,level) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name),tips=VALUES(tips),address=VALUES(address),level=VALUES(level)""",
    (item['cityid'],
    item['name'],
    item['tips'],
    item['address'],
    item['level']),
    )
    if result > 0:
        logging.log(logging.INFO, u"add one scene, {0}".format(item['name']))


def sceneInfoHandler(tx, item):
    pass


def defaultHandler():
    pass


def error_handler(e):
    logging.log(logging.ERROR, e)


HANDLER_MAP = {
    'CtripAirlineItem': airlineHandler,
    'CtripTrainItem': trainHandler,
    'SceneItem': sceneHandler,
    'SceneInfoItem': sceneInfoHandler
}


class MySQLPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        #Instantiate DB
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = SETTINGS['DB_HOST'],
            user = SETTINGS['DB_USER'],
            passwd = SETTINGS['DB_PASSWD'],
            port = SETTINGS['DB_PORT'],
            db = SETTINGS['DB_DB'],
            charset = 'utf8',
            use_unicode = True,
            cursorclass = MySQLdb.cursors.DictCursor
        )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        handler = HANDLER_MAP.get(item.__class__.__name__, defaultHandler)
        query = self.dbpool.runInteraction(handler, item)
        query.addErrback(error_handler)
        return item