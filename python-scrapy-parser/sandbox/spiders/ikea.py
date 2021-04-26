import scrapy
from sandbox.items import *


class IkeaSpider(scrapy.Spider):
    name = 'ikea'
    allowed_domains = ['www.ikea.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy.pipelines.images.ImagesPipeline': 40,
            'sandbox.pipelines.CleanItemPipline': 100,
            'sandbox.pipelines.UniqueItemsPipline': 200,
            # 'sandbox.pipelines.SplitExportersPipline': 300,
        },
        'FEEDS': {
            'data/ikea/items.json': {
                'format': 'json',
                'indent': 4,
                'overwrite': True,
            }
        },
        'IMAGES_STORE': 'data/ikea/images'
    }

    def start_requests(self):
        start_url = 'https://www.ikea.com/ru/ru/p/lampan-lampan-lampa-nastolnaya-belyy-40472917/'
        yield scrapy.Request(start_url, callback=self.parse_product)

    def parse_product(self, response):
        yield ProductItem(
            image_urls = response.css('div.range-revamp-media-grid__media-container \
                span.range-revamp-aspect-ratio-image img::attr(src)').getall(),
            name = response.css('h1.range-revamp-header-section div.range-revamp-header-section__title--big::text').get(),
            price=response.css('span.range-revamp-price__integer::text').get(),
            short_desc=response.css('span.range-revamp-header-section__description-text::text').get(),
            warning=response.css('span.range-revamp-sold-separately__text::text').get()
        )

    def parse_products_page(self, response):
        products_urls = response.css('div.plp-product-list__products > div.plp-fragment-wrapper a::attr(href)').getall()
        yield from response.follow_all(products_urls, callback=self.parse_product)