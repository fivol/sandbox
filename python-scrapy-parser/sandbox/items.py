# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from os import truncate
import scrapy
import re


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    quote = scrapy.Field()
    tags = scrapy.Field()


class QuoteAuthorItem(scrapy.Item):
    name = scrapy.Field(strip=True)
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field(strip=True)

class TagItem(scrapy.Item):
    name = scrapy.Field()
    size = scrapy.Field(extract='int')


class BookItem(scrapy.Item):
    name = scrapy.Field(strip=True)
    rating = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field(extract='float', cast=float)
    description = scrapy.Field()
    information = scrapy.Field()
    category = scrapy.Field(strip=True)

class CategoryItem(scrapy.Item):
    name = scrapy.Field(strip=True, only_text=True)
    url = scrapy.Field()