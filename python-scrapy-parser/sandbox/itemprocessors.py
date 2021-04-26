from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

"""
This utils allow you the easy way to create full featured Items
Each field meta data describes and validate value in it

Example
from sandbox.itemprocessors import field

class WikiPageItem(scrapy.Item):
    name = field(strip)
    url = field(strip, abs_url)
    desc = field(remove_tags, strip)

This file contains a lot of processors: simple like strip 
and composite like text_field

To use this items you have to write in spider:

def parse(self, response):
    loader = ItemLoader(WikiPageItem(), reponse=response)
    ...
    loader.add_value('url', response.url)
    loader.add_css('url', response.url)
    ...

Processors avaliable:
strip - removes space sybols from start and end of string
abs_url - make url or list of urls in this field absolute. 
Using loader_context['response']


"""

def strip(x):
    return x.strip()

def normalize(x):
    return x

def normalize(x):
    return x

def abs_url(url, loader_context):
    return loader_context['response'].urljoin(url)


class FieldGenerator():
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args
        super().__init__()

    def _get_input_processor(self):
        return self.kwargs.pop('in', MapCompose(*self.args))

    def _get_output_processor(self):
        return self.kwargs.pop('out', TakeFirst())

    def _get_scrapy_field(self):
        input_processor = self._get_input_processor()
        output_processor = self._get_output_processor()
        return scrapy.Field(
            input_processor=input_processor,
            output_processor=output_processor,
            **self.kwargs
        )

    @classmethod
    def generate_field(cls, *args, **kwargs):
        return cls(*args, **kwargs)._get_scrapy_field()


field = FieldGenerator.generate_field
