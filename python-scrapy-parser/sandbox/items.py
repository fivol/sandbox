# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from sandbox.itemprocessors import *


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    quote = scrapy.Field()
    tags = scrapy.Field()


class QuoteAuthorItem(scrapy.Item):
    name = scrapy.Field(strip=True, primary_key=True)
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field(strip=True)

class TagItem(scrapy.Item):
    name = scrapy.Field(primary_key=True)
    size = scrapy.Field(extract='int')


class BookItem(scrapy.Item):
    name = scrapy.Field(strip=True)
    rating = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field(extract='float', cast=float)
    description = scrapy.Field()
    information = scrapy.Field()
    category = scrapy.Field(strip=True)

class CategoryItem(scrapy.Item):
    name = scrapy.Field(strip=True, only_text=True)
    url = scrapy.Field()


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field(strip=True, cast=int)
    short_desc = scrapy.Field(strip=True)
    warning = scrapy.Field(strip=True)


class WikiPageItem(scrapy.Item):
    name = field(strip, primary_key=True)
    url = field(abs_url)
    links = field(out=Identity())
    desc = field(remove_tags)
    img = field(abs_url)
