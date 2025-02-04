# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TengxunItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    zhName = scrapy.Field()
    # 职位类别
    zhType = scrapy.Field()
    # 招聘人数
    zhNum = scrapy.Field()
    # 招聘地址
    zhAddress = scrapy.Field()
    # 招聘时间
    zhTime = scrapy.Field()
    # 招聘连接
    zhLink = scrapy.Field()


