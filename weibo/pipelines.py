# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from weibo.items import WeiboItem
import datetime
import time
import re


class WeiboPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            if item.get('content'):
                item['content'] = item['content'].lstrip(':').strip()

            if item.get('posted_at'):
                item['posted_at'] = item['posted_at'].strip()
                item['posted_at'] = self.parse_time(item['posted_at'])

        return item

    def parse_time(self, datetime):
        if re.match('\d+月\d+日', datetime):
            datetime = time.strftime('%Y年', time.localtime()) + datetime
        if re.match('\d+分钟前', datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y年%m月%d日 %H:%M', time.localtime(time.time() - float(minute)*60))
        if re.match('今天.*', datetime):
            datetime_H = re.match('今天(.*)', datetime).group(1).strip()
            datetime = time.strftime('%Y年%m月%d日', time.localtime()) + ' ' + datetime_H

        return datetime

class MongoPipeLine(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)  # 去重
        return item