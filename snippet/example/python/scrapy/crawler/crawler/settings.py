# encoding: utf-8
import os.path

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "Scrapy/VERSION (+http://scrapy.org)"

# #### Custom Start
# START_URLS = [
#     # 'http://www.1seke.com/8seke/index.html',  # It's only a test url.
#     # 'http://1bboo.com/article/list_568.html',  # It's only a test url.
# ]
# SPIDER_ENABLE = "1seke"
# IMG_CSS = {
#     "1bboo": {
#         "list_css": '#ks_xp .listtitletxt a[href]',
#         "next_css": '#pagelist .next',
#         "image_css": '#MyContent a img[src]',
#         "group_css": '#ks_xp .title'
#     },
#     "1seke": {
#         "list_css": '#new ul li a[target="_blank"]',
#         "next_css": '#new .green-black .pagegbk',
#         "image_css": '#new .newtxr img[src]',
#         "group_css": '#new .content h1'
#     },
# }
# IMG_SITE = SPIDER_ENABLE
# ALLOWED_DOMAINS = [
# ]
# #### Custom End

DEPTH_LIMIT = 0
DEPTH_STATS_VERBOSE = True

ITEM_PIPELINES = {
    'crawler.pipelines.ImageGroupPipeline': 2,
}
_IMAGES_STORE = '~/images'
IMAGES_STORE = os.path.abspath(os.path.expanduser(_IMAGES_STORE))

# ### Logging
LOG_FILE = None
LOG_LEVEL = 'DEBUG'
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
