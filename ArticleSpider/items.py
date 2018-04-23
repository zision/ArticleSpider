# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    creat_data = scrapy.Field()
    url = scrapy.Field()
    dianzan_nums = scrapy.Field()
    shoucang_nums = scrapy.Field()
    pinglun_nums = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
    url_object_id = scrapy.Field()

