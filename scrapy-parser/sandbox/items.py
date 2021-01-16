# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re

def get_int(text):
    """Returns int value from any string
    Removes all over chars"""
    return int(re.sub('\D', '', text))


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    quote = scrapy.Field()
    tags = scrapy.Field()


class QuoteAuthorItem(scrapy.Item):
    name = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()

class TagItem(scrapy.Item):
    name = scrapy.Field()
    size = scrapy.Field(serializer=get_int)
