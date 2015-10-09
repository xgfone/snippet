# coding: utf-8
from scrapy.item import Item, Field


class ImgItem(Item):
    group = Field()
    image_urls = Field()
    images = Field()
