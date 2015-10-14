# coding: utf-8
from __future__ import unicode_literals, print_function

from scrapy.selector import Selector
from crawler.items import TextItem
from crawler.spiders.base import BaseSpider


class TextSpider(BaseSpider):
    name = "text"
    custom_settings = {
        "ITEM_PIPELINES": {
            'crawler.pipelines.TextPipeline': 2,
        }
    }

    def handle_page(self, response):
        hxs = Selector(response)
        # text_css = self.css_selector["text_css"]
        # title_css = self.css_selector["title_css"]
        text_css = self.get_css("text_css")
        title_css = self.get_css("title_css")
        if not text_css or not title_css:
            return []
        item = TextItem()

        try:
            item["title"] = hxs.css(title_css).xpath('text()').extract()[0]
        except Exception:
            return []

        item["texts"] = hxs.css(text_css).xpath('text()').extract()
        if not item["texts"]:
            return []

        return [item]
