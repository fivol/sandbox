import scrapy


class RatesSpider(scrapy.Spider):
    name = 'rates'
    allowed_domains = ['dollara.ru']
    start_urls = ['http://dollara.ru/']

    def parse(self, response):
        table = response.xpath('//table[@class="maintablalala"]')
        print("TABLE IS", table)
        for item in table.xpath('tr/td/span[0]'):
            yield {
                'mark': item.xpath('/span[0]').get()
            }