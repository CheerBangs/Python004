#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
# from bs4 import BeautifulSoup as bs
from scrapy.selector import Selector
from way2_scrapy.items import Way2ScrapyItem
localMaoyanUrl = 'http://localhost:8080/maoyan.htm'
localMaoyanDetailUrl = 'http://localhost:8080/detail.htm'
maoyanUrl = 'http://maoyan.com/films/?showType=3'
useLocal = True

class MoviesSpider(scrapy.Spider):
    # 爬虫名字，不要轻易修改
    name = 'movies'
    # 防止自动爬深时爬到不需要的网站
    allowed_domains = ['maoyan.com', 'localhost']
    start_urls = [localMaoyanUrl] if useLocal == True else [maoyanUrl]

    def parseDetail(self, response):
        container = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        item = Way2ScrapyItem()
        item['title'] = container.xpath('./h1/text()').extract_first()
        item['category'] = ''.join(container.xpath('.//a[@class="text-link"]/text()').extract())
        item['time'] = container.xpath('.//li')[2].xpath('./text()').extract_first()
        yield item

    def parseHome(self, response):
        detailUrls = Selector(response=response).xpath('//a[@data-act="movies-click"]/@href')
        validDetailUrls = detailUrls[0: 10].extract()
        return validDetailUrls

    def parse(self, response):
        validDetailUrls = self.parseHome(response)
        print(validDetailUrls)
        for targetUrl in validDetailUrls:
            print('targetUrl:' + localMaoyanDetailUrl if useLocal else targetUrl)
            yield scrapy.Request(url=localMaoyanDetailUrl if useLocal else targetUrl , meta = {}, callback=self.parseDetail)