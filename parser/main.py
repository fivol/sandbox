import csv
import requests
from bs4 import BeautifulSoup, Tag
import abc
from fake_useragent import UserAgent
import os
from pathlib import Path, PurePath
from jsonschema import validate
from hashlib import sha1
import pandas as pd
import logging
from grab import Grab

logging.basicConfig()


class ClientSession:
    def __init__(self, proxy=None, headers=None):
        self.session = requests.session()

    def get(self, url):
        return self.session.get(url)


class ParsingSession:
    """This class accept many parsers. And run them together. Can do some sequential tasks. Parse many pages etc"""

    def __init__(self, handlers, **kwargs):
        pass


class ClientParser:
    """This class represent one bot (or one human with browser), who do some staff. Get information
    switches pages etc"""

    def __init__(self, *args, config=None, session: ClientSession, **kwargs):
        self.config = self._init_config()
        self.config.update(self.get_config())
        if config:
            self.config.update(config)

        self._verify_config()
        self.session = requests.session()
        if session:
            self.session = session
        self.folder = Path(self.config['parser_name'])
        self.cache_folder = self.folder / '.cached'
        self._create_folder(self.folder)
        self._create_folder(self.cache_folder)

    def _create_folder(self, folder):
        if not folder.exists():
            os.mkdir(folder)

    def _verify_config(self):
        config_schema = {
            'type': 'object',
            'properties': {
                'config_parser': {'type': 'string'},
                'headers': {'type': 'object'}
            }
        }
        validate(instance=self.config, schema=config_schema)

    @staticmethod
    def _hash_url(url: str):
        return sha1(url.encode()).hexdigest()[:10]

    def _get_html(self, url):
        filename = f'{self._hash_url(url)}.html'

        if Path(filename).exists():
            with open(filename, 'r') as f:
                return f.read()

        response = self.session.get(url=url, headers=self.config['headers'])
        # Raise exception if status code not starting with 2**
        response.raise_for_status()

        html = response.text
        with open(filename, 'w') as f:
            f.write(html)

        return html

    def _get_soup(self, url):
        return BeautifulSoup(self._get_html(url), 'lxml')

    @staticmethod
    def _init_config():
        ua = UserAgent()

        return {
            'headers': {
                'user-agent': ua.chrome
            },
        }

    @staticmethod
    def get_config():
        return {}


class BlocksListParser(ClientParser):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def _get_page(self, url):
        """Getting page html"""
        return

    def _add_object(self):
        pass

    @staticmethod
    def object_from_block(block: Tag):
        """Gives one block on page. This function should return python dict object from Tag"""
        raise NotImplementedError

    @staticmethod
    def get_blocks(soup: BeautifulSoup):
        """Returns list with necessary blocks. Each have Tag type"""
        raise NotImplementedError

    def run(self):
        """Main function. Execute parsing with config provided"""
        url = self.config.get('url')
        soup = self._get_soup(url)
        try:
            blocks = self.get_blocks(soup)
        except:
            logging.warning("Fair to get blocks. Url: %s", url)

        objects = [
            self.object_from_block(block)
            for block in blocks
        ]
        df = pd.DataFrame(objects)
        df.to_csv(self.config['csv_filename'])


class UkraineCurrencyParser(BlocksListParser):
    @staticmethod
    def get_config():
        return {
            'parser_name': 'ukraine_usd_currency',
            'url': 'https://finance.i.ua/',
            'csv_filename': 'usd_currency',
        }

    @staticmethod
    def get_blocks(soup: BeautifulSoup):
        return soup.find('tbody', class_='bank_rates_usd').contents

    @staticmethod
    def object_from_block(block: Tag):
        title = block.find('th', class_='td-title')
        return {
            'bank_name': title.a.get_text(strip=True),
            'page_url': title.get('href'),
            'buy_rate': block.find('td', class_='buy_rate').get_text(),
            'sell_rate': block.find('td', class_='sell_rate').get_text()
        }


def main():
    parser = UkraineCurrencyParser()
    parser.run()


if __name__ == '__main__':
    main()
