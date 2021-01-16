import scrapy
from scrapy.loader import ItemLoader
from sandbox.items import QuoteAuthorItem, QuoteItem, TagItem
from sandbox import pipelines
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']

    custom_settings = {
        'ITEM_PIPELINES': {
            pipelines.ClearItemPipline: 100,
            pipelines.UniqueItemsPipline: 200,
            pipelines.SplitExportersPipline: 300,
        },
        'PRIMARY_KEYS': {
            QuoteAuthorItem: 'name',
            TagItem: 'name',
            QuoteItem: 'quote'
        },
        'FEEDS_SPLITTER': {
            'exporter': CsvItemExporter,
            'folder': 'data/quotes_parser/csv',
            'extension': 'csv',
            'settings': {
                'indent': 4,
            }
        },
        'LOG_LEVEL': 'WARNING',
        'DEPTH_LIMIT': 1

    }

    def start_requests(self):
        start_url = 'http://quotes.toscrape.com/'
        yield scrapy.Request(start_url, callback=self.parse_quotes)

    def parse_quotes(self, response, **kwargs):
        blocks = response.css('div.quote')
        for block in blocks:
            # quote = ItemLoader(QuoteItem(), response)
            yield QuoteItem(
                author = block.css('small.author::text').get(),
                quote = block.css('span.text::text').get(),
                tags=block.css('a.tag::text').getall()
            )
            author_urls = response.css('div.quote span a::attr(href)')
            yield from response.follow_all(author_urls, callback=self.parse_author)

        next_page_url = response.urljoin(response.css('li.next a::attr(href)').get())

        tags_list = response.css('div.tags-box a.tag')
        for tag in tags_list:
            yield TagItem(
                name=tag.css('::text').get(),
                size=tag.css('::attr(style)').get(),
            )

        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse_quotes)

    def parse_author(self, response, item=None):
        born = response.css('div.author-details p')
        yield QuoteAuthorItem(
            name=response.css('h3.author-title::text').get(),
            born_date=born.css('span.author-born-date::text').get(),
            born_location=born.css('span.author-born-location::text').get(),
            description=response.css('div.author-description::text').get()
        )
