import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.exporters import JsonItemExporter, JsonLinesItemExporter
from scrapy import Request
from sandbox.items import *
from itemloaders import ItemLoader
import logging
logger = logging.getLogger()


class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)']

    custom_settings = {
        'SPLIT_EXPORTERS_PIPELINE': {
            'exporter': JsonLinesItemExporter,
            'folder': 'data/wiki/json',
            'extension': 'json',
            'settings': {
                'indent': 0,
            }
        },
        # This is set for testing!!!! Comment out paramener to parse all
        'DEPTH_LIMIT': 1,
        'HTTPCACHE_ENABLED': True,
        'IMAGES_STORE': 'data/books/images'
    }
    link_extractor = LinkExtractor(
        unique=True,
        strip=True,
        allow=r'wikipedia.org/wiki/',
        deny=[r'#', '/wiki/.+:'],
        allow_domains=['en.wikipedia.org'],
        tags='a',
        restrict_css='div.mw-body-content'
    )

    def parse(self, response):
        loader = ItemLoader(WikiPageItem(), response, response=response)
        loader.add_css('name', 'h1.firstHeading::text')
        loader.add_value('url', response.url)
        loader.add_css('img', 'td a.image img::attr(src)')
        links = self.link_extractor.extract_links(response)
        links_items = [
            {'url': link.url, 'text': link.text} 
            for link in links
        ]
        loader.add_value('links', links_items)
        yield from response.follow_all([link.url for link in links])
        yield loader.load_item()
        
