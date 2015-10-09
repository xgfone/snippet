# coding: utf-8
from __future__ import unicode_literals, print_function

from scrapy.spiders.crawl import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from scrapy.selector import Selector
from scrapy.spiders import Rule

from crawler import settings
from crawler.utils import URL
from crawler.items import ImgItem

NEXT = ["next", "下一页"]


class NextLinkExtractor(LinkExtractor):
    def __init__(self, spider, *args, **kwargs):
        super(NextLinkExtractor, self).__init__(*args, **kwargs)
        self.spider = spider

    def extract_next_links(self, response):
        hxs = Selector(response)
        next_css = settings.IMG_CSS[settings.IMG_SITE]["next_css"]
        _next = hxs.css(next_css)
        for n in _next:
            nl = n.xpath('text()').extract()[0].lower()
            if nl in NEXT:
                url = n.xpath('@href').extract()[0]
                return [url]
        return []

    def extract_links(self, response):
        hxs = Selector(response)
        list_css = settings.IMG_CSS[settings.IMG_SITE]["list_css"]
        urls = []
        try:
            links = hxs.css(list_css).xpath('@href').extract()
            for url in links:
                urls.append(url)
            next_url = self.extract_next_links(response)
            urls.extend(next_url)
        except Exception as err:
            self.logger.error("%s" % err)

        rtn = []
        for url in urls:
            url = URL.s_get_full_url(URL(url), URL(response.url))
            if url:
                rtn.append(Link(url=url))

        return rtn


class ImageSpider(CrawlSpider):
    name = "image"

    def __init__(self, *args, **kwargs):
        self.rules = (
            Rule(NextLinkExtractor(self), callback="handle_page", follow=True),
        )

        start_urls = getattr(self, "start_urls", None)
        if not start_urls:
            start_urls = getattr(settings, "START_URLS", [])
        self.start_urls = start_urls

        allowed_domains = getattr(self, "allowed_domains", None)
        if not allowed_domains:
            allowed_domains = getattr(settings, "ALLOWED_DOMAINS", [])
        self.allowed_domains = allowed_domains

        super(ImageSpider, self).__init__(*args, **kwargs)

    def handle_page(self, response):
        hxs = Selector(response)
        css = settings.IMG_CSS[settings.IMG_SITE]
        image_css = css["image_css"]
        group_css = css["group_css"]

        item = ImgItem()
        item["image_urls"] = hxs.css(image_css).xpath('@src').extract()
        if not item["image_urls"]:
            return []

        try:
            item["group"] = hxs.css(group_css).xpath('text()').extract()[0]
        except Exception:
            item["group"] = None

        return [item]

    def parse_start_url(self, response):
        return self.handle_page(response)
