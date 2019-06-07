# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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
