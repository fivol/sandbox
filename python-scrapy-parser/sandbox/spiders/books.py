import scrapy
from scrapy.http import request
from scrapy.loader import ItemLoader
from sandbox.items import *
from sandbox import pipelines
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'sandbox.pipelines.CleanItemPipline': 100,
            'sandbox.pipelines.UniqueItemsPipline': 200,
            'sandbox.pipelines.SplitExportersPipline': 300,
        },
        'PRIMARY_KEYS': {
            BookItem: 'name',
            CategoryItem: 'name',
        },
        'FEEDS_SPLITTER': {
            'exporter': JsonItemExporter,
            'folder': 'data/books_parser/json',
            'extension': 'json',
            'settings': {
                'indent': 4,
            }
        },
        # 'CLOSESPIDER_PAGECOUNT': 4,
        'LOG_LEVEL': 'WARNING',
        # This is set for testing!!!! Comment out paramener to parse all
        'DEPTH_LIMIT': 2

    }

    def start_requests(self):
        start_url = 'http://books.toscrape.com/'
        yield scrapy.Request(start_url, callback=self.parse_categories)

    def parse_book_page(self, response, category=None, **kwargs):
        info_rows = response.css('table.table tr')
        from scrapy.shell import inspect_response
        # inspect_response(response, self)
        yield BookItem(
            name=response.css('div.product_main h1::text').get(),
            img=response.urljoin(response.css('div.item img::attr(href)').get()),
            price=response.css('p.price_color::text').get(),
            rating=len(response.css('p.star-rating i.icon-star').getall()),
            description=response.css('div#product_description ~ p::text').get(),
            information={
                row.css('th::text').get(): row.css('td::text').get() 
                for row in info_rows
            },
            category=category,
            url=response.url
        )

    def parse_category_books(self, response, category=None, **kwargs):
        books = response.css('article.product_pod h3 a::attr(href)').getall()
        yield from response.follow_all([
            response.urljoin(url)
            for url in books
        ], callback=self.parse_book_page, cb_kwargs={'category': category})
        
        # next_page = response.urljoin(response.css('li.next a::attr(href)').get())
        # if next_page:
        #     yield scrapy.Request(next_page, callback=self.parse_category_books)

    def parse_categories(self, response):
        categories = response.css('ul li ul li a')
        for category in categories:
            url = response.urljoin(category.css('::attr(href)').get())
            name =category.css('::text').get()
            yield CategoryItem(
                name=name,
                url=url
            )
            yield scrapy.Request(url, callback=self.parse_category_books, cb_kwargs={'category': name})

