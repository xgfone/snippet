# coding: utf-8

import os
import os.path
import hashlib

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from scrapy.utils.misc import md5sum
from scrapy.utils.misc import arg_to_iter
from twisted.internet.defer import DeferredList

from crawler.utils import URL, to_str
from crawler import settings


class GroupDownPipelineMinix(object):
    DEFAULT_EXT = ''
    URLS_NAME = None

    def file_path(self, request, response=None, info=None):
        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url

        group = getattr(request, "group", None)
        try:
            if group:
                filename = "{0}{1}".format(group["urls"][request.url], self.DEFAULT_EXT)
                path = os.path.join(group["name"], filename)
            else:
                url = URL(url)
                url.scheme = ''
                _, ext = os.path.splitext(url.path.split('/')[-1])
                if not ext:
                    url.path = url.path.strip('/') + self.DEFAULT_EXT
                path = url.geturl()
        except Exception:
            path = os.path.join("err", hashlib.sha1(url).hexdigest() + self.DEFAULT_EXT)

        if request.spider.subdir:
            path = os.path.join(request.spider.subdir, path)
        return path

    def image_downloaded(self, response, request, info):
        buf = BytesIO(response.body)
        path = self.file_path(request, response=response, info=info)
        self.store.persist_file(path, buf, info)
        buf.seek(0)
        checksum = md5sum(buf)
        return checksum

    def process_item(self, item, spider):
        info = self.spiderinfo
        requests = arg_to_iter(self.get_media_requests(item, info))
        dlist = [self._process_request(r, info, item, spider) for r in requests]
        dfd = DeferredList(dlist, consumeErrors=1)
        return dfd.addCallback(self.item_completed, item, info)

    def _process_request(self, request, info, item=None, spider=None):
        if item:
            group = {
                "urls": {},
                "name": item.get("group")
            }
            for n, url in enumerate(item[self.URLS_NAME], 1):
                group["urls"][url] = n
            request.group = group
        if spider:
            request.spider = spider

        return super(GroupDownPipelineMinix, self)._process_request(request, info)

    def item_completed(self, results, item, info):
        result = {}
        for n, r in enumerate(results):
            ok, x = r
            if ok:
                result[x["url"]] = x["path"]
            else:
                result[item[self.URLS_NAME][n]] = x.getErrorMessage()
        # TODO: Save the result

        # file_paths = [x['path'] for ok, x in results if ok]
        # if not file_paths:
        #     raise DropItem("Item contains no files")
        # item['image_paths'] = file_paths
        # return item

        return super(GroupDownPipelineMinix, self).item_completed(results, item, info)


class FileGroupPipeline(GroupDownPipelineMinix, FilesPipeline):
    DEFAULT_EXT = '.txt'
    URLS_NAME = 'file_urls'


class ImageGroupPipeline(GroupDownPipelineMinix, ImagesPipeline):
    DEFAULT_EXT = '.jpg'
    URLS_NAME = 'image_urls'


class TextPipeline(object):
    def _get_dirname(self, spider):
        if spider.subdir:
            path = os.path.join(settings.TEXTS_STORE, spider.subdir)
        else:
            path = settings.TEXTS_STORE

        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def filter(self, path, item, spider):
        if spider.file_min_size:
            size = os.stat(path).st_size
            if size < spider.file_min_size * 1024:
                os.remove(path)

    def process_item(self, item, spider):
        dirname = self._get_dirname(spider)
        path = os.path.join(dirname, item["title"] + ".txt")
        with open(path, "w") as f:
            for i in item["texts"]:
                f.write(to_str(i))

        self.filter(path, item, spider)

        raise DropItem
