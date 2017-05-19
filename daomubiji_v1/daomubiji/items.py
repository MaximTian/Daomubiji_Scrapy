# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DaomubijiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookOrder = scrapy.Field() # 书编号
    bookName = scrapy.Field() # 书标题
    chapterFirst = scrapy.Field() # 章节类别
    chapterMid = scrapy.Field() # 章节序号
    chapterLast = scrapy.Field()  # 章节名称
    content = scrapy.Field()  # 章节内容
