import scrapy
from scrapy import Selector
from movie.items import MovieItem
import pdb


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        # print(response.text)
        counter = 0
        candidates = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        while counter <= 10:
            c_item = candidates[counter]
            item = MovieItem()
            item['name'] = c_item.xpath('./div[1]/span/text()').extract()[0].strip()
            item['category'] = (c_item.xpath('./div[2]/text()').extract()[1]).strip()
            item['release_time'] = (c_item.xpath('./div[4]/text()').extract()[1]).strip()
            # print('-------------------------------------------------------')
            # print(item['name'])
            # print(item['category'])
            # print(item['release_time'])
            counter += 1
            yield item