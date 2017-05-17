#-*_coding:utf8-*-

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from daomubiji.items import DaomubijiItem

class daomubijiSpider(Spider):
    name = "daomubijiSpider"
    start_urls = ['http://www.daomubiji.com/']

    def parse_detail(self,response): # 提取子网页信息
        selector = Selector(response)
        item = DaomubijiItem()

        book_order_name = selector.xpath('//h1/text()').extract()[0]
        pos = book_order_name.find(u'：')
        book_order = book_order_name[:pos] # 获取书编号
        book_name = book_order_name[pos + 1:] # 获取书名

        chapter_list = selector.xpath('//article[@class="excerpt excerpt-c3"]//text()').extract()
        for each in chapter_list:
            pos_first = each.find(' ')
            pos_last = each.rfind(' ')
            chapter_first = ''
            chapter_mid = ''
            chapter_last = ''
            if pos_first != pos_last:
                chapter_first = each[:pos_first]
                chapter_mid = each[(pos_first + 1): pos_last]
                chapter_last = each[pos_last + 1:]
            else:
                chapter_first = each[:pos_first]
                chapter_last = each[pos_last + 1:]

            # 存储信息
            item['bookOrder'] = book_order
            item['bookName'] = book_name
            item['chapterFirst'] = chapter_first
            item['chapterMid'] = chapter_mid
            item['chapterLast'] = chapter_last
            yield item

    def parse(self, response): # 程序从这个函数开始执行
        selector = Selector(response)

        book_filed = selector.xpath('//article/div') # 抓取书标题

        book_link = selector.xpath('//article/p/a/@href').extract() # 抓取盗墓笔记每本书的链接
        # '//article/p/a/@href'也可以写成('//article//@href')

        link_flag = 0
        for each in book_filed:
            book_name_title = each.xpath('h2/text()').extract()[0]
            pos = book_name_title.find(u'：')
            if pos == -1: # 只抓取符合我们格式规定的书
                continue
            yield Request(book_link[link_flag], callback=self.parse_detail) # 调用parse_detail函数
            link_flag += 1
