# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Way2ScrapyPipeline:
    def process_item(self, item, spider):
        title = item['title']
        category = item['category']
        time = item['time']
        output = f'{title}|\t|{category}\t|{time}|\n\n'
        with open('./maoyanmovie.txt', 'a+', encoding='utf-8') as article:
                article.write(output)
                article.close()
        return item
