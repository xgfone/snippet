# coding: utf-8
from scrapy.item import Item, Field


class QzoneItem(Item):
    title = Field()
    content = Field()
    created = Field()
    clicks = Field()
    category = Field()
