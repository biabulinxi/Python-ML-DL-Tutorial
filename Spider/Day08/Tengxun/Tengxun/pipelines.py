# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from .settings import *

class TengxunPipeline(object):
    def process_item(self, item, spider):
        print('*'*50)
        print(item['zhName'])
        print(item['zhType'])
        print(item['zhNum'])
        print(item['zhAddress'])
        print(item['zhTime'])
        print(item['zhLink'])
        print('*'*50)
        return item


class TengxunMongoPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db = self.conn['tengxundb2']
        self.myset = self.db['tengxun']

    def process_item(self,item,spider):
        d = dict(item)
        self.myset.insert_one(d)
        return item



