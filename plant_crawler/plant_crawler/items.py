# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlantCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    scientificName = scrapy.Field()
    chineseName = scrapy.Field()
    attribute = scrapy.Field()
    describe = scrapy.Field()
    distribution = scrapy.Field()
    originalName = scrapy.Field()