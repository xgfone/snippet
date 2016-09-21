# encoding: utf-8
import os.path

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "Scrapy/VERSION (+http://scrapy.org)"

# #### Custom Start
# The site that the spider want to crawl. If not given, it could be passed by
# the command line argument, `site=XXX`, for example,
#   $ scrapy crawl text -a site=1bboo
# If you don't set it here or pass it by the command line, for the spiders of
# `image` and `text`, the starting urls will be empty, that's, a empty list.
# If you set it through the two ways meanwhile, use the command line first.
# SPIDER_SITE = "1bboo"

# Its value is a dict, which the key is the spider name, and the value a other
# dict which contains all the starting URLs of the site the spider wants to
# crawl. And the key is the site name, which is the same as `SPIDER_SITE`, and
# the value is a list, whose elements are the starting URLs.
START_URLS = {
    "image": {  # Spider Name
        "1bboo": [  # Site Name
        ],
        "1seke": [
        ]
    },
    "text": {  # Spider Name
        "1bboo": [
        ],
        "1seke": [
        ]
    }
}

# Its value is a dict, which the key is the spider name, and the value a other
# dict which contains all the CSS selectors of the site the spider wants to
# crawl. And the key is the site name, which is the same as `SPIDER_SITE`, and
# the value is a dict, too. According to the different spider, the content of
# this dict is different, too. The spider of `image` contains four Key-Value
# pairs, which the keys are "list_css", "next_css", "image_css", "group_css",
# and the values are the CSS selectors. The spider of `text` also contains four
# Key-Value pairs, which the keys are "list_css", "next_css", "text_css",
# "title_css", and the values are also the CSS selectors.
#
# "list_css" is used to extract some URLs of which the sites contain the images.
# "next_css" is used to extract the URL of the next web page.
# Notice: "list_css" and "next_css" extract the URLs from the same web page.
#
# "image_css" is used to extract some URLs of the images.
# "group_css" is used to extract the title of the images, which images are
# packed into a group.
#
# "text_css" is used to extract the content of the text.
# "title_css" is used to extract the title of the text.
CSS_SELECTORS = {
    "image": {
        "1bboo": {
            "list_css": '#ks_xp .listtitletxt a[href]',
            "next_css": '#pagelist .next',

            "image_css": '#MyContent a img[src]',
            "group_css": '#ks_xp .title'
        },
        "1seke": {
            "list_css": '#new ul li a[target="_blank"]',
            "next_css": '#new .green-black .pagegbk',

            "image_css": '#new .newtxr img[src]',
            "group_css": '#new .content h1'
        },
    },
    "text": {
        "1bboo": {
            "list_css": '#ks_xp .listtitletxt a[href]',
            "next_css": '#pagelist .next',

            "text_css": '#MyContent',
            "title_css": '#ks_xp .title'
        },
        "4xbxb": {
            "list_css": ".zuo li a[href]",
            "next_css": ".zuo div.pagination22 a.pagelink_a[href]",

            "text_css": "div.content",
            "title_css": "div.page_title",
        },
    }
}
FILE_MIN_SIZE = 30  # The unit is KB.
ALLOWED_DOMAINS = [
]
# #### Custom End

DEPTH_LIMIT = 0
DEPTH_STATS_VERBOSE = True

# ITEM_PIPELINES = {}
_IMAGES_STORE = '~/images'
IMAGES_STORE = os.path.abspath(os.path.expanduser(_IMAGES_STORE))

# Text
_TEXTS_STORE = "~/texts"
TEXTS_STORE = os.path.abspath(os.path.expanduser(_TEXTS_STORE))

# ### Logging
LOG_FILE = None
LOG_LEVEL = 'INFO'  # Also 'DEBUG', 'WARNING', 'ERROR'
# If True, all standard output (and error) of your process will be redirected
# to the log. For example if you print 'hello' it will appear in the Scrapy log.
# LOG_STDOUT = False

# ### Memory
# MEMUSAGE_ENABLED = False
# MEMUSAGE_LIMIT_MB = 0
# MEMUSAGE_NOTIFY_MAIL = ['user@example.com']
# MEMUSAGE_REPORT = False
# MEMUSAGE_WARNING_MB = 0

# SPIDER_LOADER_CLASS = 'scrapy.spiderloader.SpiderLoader'
# SPIDER_MIDDLEWARES = {}  # See SPIDER_MIDDLEWARES_BASE
# SCHEDULER = 'scrapy.core.scheduler.Scheduler'
#
# ROBOTSTXT_OBEY = False

# ### Download
# DOWNLOAD_MAXSIZE = 1073741824  # 1024MB
# DOWNLOADER = 'scrapy.core.downloader.Downloader'
# DOWNLOADER_MIDDLEWARES = {}
# DOWNLOAD_HANDLERS = {}  # See DOWNLOAD_HANDLERS_BASE
# URLLENGTH_LIMIT = 2083
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
# }
DOWNLOAD_TIMEOUT = 30
