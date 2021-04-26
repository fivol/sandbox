import scrapy


class DigikeySpider(scrapy.Spider):
    name = 'digikey'
    allowed_domains = ['www.digikey.com']
    start_urls = ['https://www.digikey.com/en/products/detail/avx-corporation/06032U3R9BAT2A/6796754']

    def parse(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response)
