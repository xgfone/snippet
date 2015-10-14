# encoding: utf-8
from __future__ import unicode_literals, print_function

from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from scrapy.selector import Selector

from crawler.utils import URL
# from crawler import settings

NEXT = ["next", "下一页"]


class NextLinkExtractor(LinkExtractor):
    def __init__(self, spider, *args, **kwargs):
        super(NextLinkExtractor, self).__init__(*args, **kwargs)
        self.spider = spider

    @property
    def css_selector(self):
        return self.spider.css_selector

    def get_css(self, css_name, default=None):
        return self.spider.get_css(css_name, default)

    def extract_next_links(self, response):
        hxs = Selector(response)
        next_css = self.get_css("next_css")
        if not next_css:
            return []

        _next = hxs.css(next_css)
        for n in _next:
            nl = n.xpath('text()').extract()[0].lower()
            if nl in NEXT:
                url = n.xpath('@href').extract()[0]
                return [url]
        return []

    def extract_links(self, response):
        hxs = Selector(response)
        list_css = self.get_css("list_css")
        if not list_css:
            return []

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
