# coding: utf-8
from scrapy.item import Item, Field


class ImageItem(Item):
    group = Field()
    image_urls = Field()
    images = Field()


class TextItem(Item):
    title = Field()
    texts = Field()
