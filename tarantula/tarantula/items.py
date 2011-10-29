# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TarantulaItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    link = Field()

class TestItem(Item):
    id = Field()
    name = Field()
    description = Field()
