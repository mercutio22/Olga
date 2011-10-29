# Scrapy settings for tarantula project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'tarantula'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['tarantula.spiders']
NEWSPIDER_MODULE = 'tarantula.spiders'
DEFAULT_ITEM_CLASS = 'tarantula.items.TarantulaItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
