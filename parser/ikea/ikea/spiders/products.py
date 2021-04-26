import scrapy
from bs4 import BeautifulSoup


class ProductsSpider(scrapy.Spider):
    name = 'products'
    start_urls = ['https://www.ikea.com/ru/ru/cat/veshalki-napolnye-49769/']

    def parse(self, response):
        html = response.text
        soup = BeautifulSoup(html)
        blocks = soup.find_all('div', class_='plp-fragment-wrapper')
        print("blocks len", len(blocks))
        for block in blocks:
            yield {
                'name': block.find('div', class_='range-revamp-header-section__title--small').get_text(),
                'price': block.find('span', class_='range-revamp-price__integer').get_text(),
                'url': block.find('a').get('href'),
                'img': block.find('img', class_='range-revamp-aspect-ratio-image__image').get('src'),
            }
