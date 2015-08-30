# coding: utf-8
from project.extensions.crawl import DRule
from scrapy.contrib.spiders.crawl import CrawlSpider
from scrapy.contrib.linkextractors.sgml import BaseSgmlLinkExtractor, SgmlLinkExtractor

from project.items import BaseJobItem, BaseComItem
from scrapy.link import Link
from scrapy.utils.response import get_base_url
from scrapy.item import Item, Field
import re

from scrapy.selector import Selector
from ..item import QzoneItem


#rule.link_extractor.extract_links(response)
class MyLinkExtractor(SgmlLinkExtractor):
    def __init__(self):
        SgmlLinkExtractor.__init__(self)

    def extract_links(self, response):
        url = response.url
        hxs = Selector(response)

        #str_tmp = hxs.xpath("//td[@class='textr']/a[@class='bluelink'][last()]/text()").extract()
        str_tmp = hxs.xpath('//*[@id="pagination"]/div/p[1]/a[2]').extract()
        if len(str_tmp) == 0 or str_tmp[0] != u"下一页":
            return []
        try:
            str_tmp = hxs.xpath("//td[@class='textr']/a[@class='bluelink'][last()]/@href").extract()
            p_num = re.search("(?<=turnPage\(').*?(?=')", str_tmp[0]).group(0)
            url = url.split("?")
            if len(url) != 2:
                return []
            paras = url[1].split('&')
            re_url = url[0] + "?"
            pps = []
            for p in paras:
                a = p.split('=')
                if len(a) != 2:
                    continue
                if a[0] == "p":
                    a[1] = p_num
                pps.append("=".join(a))
            re_url += "&".join(pps)
            return [Link(url=re_url)]
        except:
            return []


class Spiderzhaopin(CrawlSpider):
    name = "blog"
    allowed_domains = ["user.qzone.qq.com"]
    start_urls = ["http://user.qzone.qq.com/944350535/infocenter#!app=2"]

    rules = (
        DRule(MyLinkExtractor(), follow=True, stoppage=0),
        DRule(SgmlLinkExtractor(restrict_xpaths='//*[@id="app_mod_blog"]'), callback='parse_detail', follow=True)
    )

    def parse_detail(self, response):
        hxs = Selector(response)
        item = QzoneItem()

        item['title'] = hxs.xpath('//*[@id="paperTitle"]/font/text()').extract()
        item['content'] = hxs.xpath('//*[@id="blogDetailDiv"]/text()').extract()
        item['created'] = hxs.xpath('//*[@id="pubTime"]/text()').extract()
        item['clicks'] = hxs.xpath('//*[@id="readNum"]/text()').extract()
        item['category'] = hxs.xpath('//*[@id="infoBlogCate"]/text()').extract()

        # title = hxs.xpath('//div[@id="positionTitle"]/h1/text()').extract()
        # if title:
        #     item['title'] = title[0].strip()

        return [item]
