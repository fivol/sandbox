import scrapy
from urllib.parse import quote


class GoogleTranslateSpider(scrapy.Spider):
    name = 'googletranslate'
    allowed_domains = ['translate.google.com']
    start_urls = ['http://translate.google.com/']

    def start_requests(self):
        temp_url = 'https://translate.google.com/?sl={}&tl={}&text={}&op=translate'
        text = 'cat'
        url = temp_url.format('en', 'ru', text)
        yield scrapy.Request(url)

    def parse(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, spider=self)
