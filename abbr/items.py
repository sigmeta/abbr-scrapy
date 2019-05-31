# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AbbrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    abbr = scrapy.Field()
    desc = scrapy.Field()
    classes = scrapy.Field()
    #cate = scrapy.Field()

class AbbrOrderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    abbr = scrapy.Field()
    desc = scrapy.Field()
    raw_abbr = scrapy.Field()
    #cate = scrapy.Field()


class VoaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    mp3name = scrapy.Field()
