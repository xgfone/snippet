# coding: utf-8
from __future__ import unicode_literals, print_function

from scrapy.selector import Selector
from crawler.items import ImageItem
from crawler.spiders.base import BaseSpider


class ImageSpider(BaseSpider):
    name = "image"
    custom_settings = {
        "ITEM_PIPELINES": {
            'crawler.pipelines.ImageGroupPipeline': 2,
        }
    }

    def handle_page(self, response):
        hxs = Selector(response)
        image_css = self.get_css("image_css")
        group_css = self.get_css("group_css")
        if not group_css or not image_css:
            return []
        return self.extract_item(hxs, image_css, group_css)

    def extract_item(self, hxs, file_css, group_css):
        item = ImageItem()
        item["image_urls"] = hxs.css(file_css).xpath('@src').extract()
        if not item["image_urls"]:
            return []

        try:
            item["group"] = hxs.css(group_css).xpath('text()').extract()[0]
        except Exception:
            item["group"] = None

        return [item]
