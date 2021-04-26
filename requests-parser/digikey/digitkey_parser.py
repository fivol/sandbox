import re
import requests
import logging
from urllib import parse

logging.basicConfig(level=logging.DEBUG)
logger = logging

request_headers = {'Host': 'www.digikey.com', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Cookie': '', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'TE': 'Trailers'}

price_headers = {'Host': 'www.digikey.com',
                 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
                 'Accept': '*/*', 'Accept-Language': 'en-us', 'Accept-Encoding': 'gzip, deflate, br',
                 'Referer': 'https://www.digikey.com/en/products/detail/avx-corporation/06032U3R9BAT2A/6796754',
                 'x-currency': 'USD', 'x-request-id': '8d58efea-cb8f-44a1-a0eb-6ab924a37ca2',
                 'Connection': 'keep-alive', 'Cookie': '', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                 'TE': 'Trailers'}

price_search_pattern = r'https://www.digikey.com/.+?/products/detail/.+?/{}/(\d+)"'
price_url_template = 'https://www.digikey.com/products/api/v2/pricing/{}'


class Proxy:
    protocol = {
        'socks5': 'https',
        'socks4': 'https',
        'https': 'https',
        'http': 'http'
    }

    ping_url = 'https://google.com'
    my_ip_url = 'http://plain-text-ip.com/'

    def __init__(self, proxy_url: str):
        self.proxy_url = proxy_url
        self.proxy_obj = parse.urlparse(proxy_url)

    def get_proxy_dict(self):
        return {
            'http': self.proxy_url,
            'https': self.proxy_url
        }

    @property
    def ip(self):
        return self.proxy_obj.hostname

    def get_my_ip(self):
        return requests.get(self.my_ip_url, proxies=self.get_proxy_dict()).text.strip()

    def is_valid(self):
        resp = requests.get(self.ping_url, proxies=self.get_proxy_dict())
        return resp.status_code == 200

    def assert_valid(self):
        assert self.is_valid()

    def __repr__(self):
        return self.proxy_url


# proxy = Proxy('socks5://neafiol:IxTuXG@207.244.246.95:20082')
proxy = Proxy('https://185.189.14.93:9999')
proxy.assert_valid()
logger.info('my ip: %s', proxy.get_my_ip())


def load_digitkey_page(url):
    """
    Returns tuple (main page html, pricing json)
    Function use requests.raise_for_status() method to raise HTTPError
    if status_code is not 200
    """

    requests_session = requests.Session()
    resp = requests_session.get(url, headers=request_headers, proxies=proxy.get_proxy_dict())
    big_product_id = url.strip('/').split('/')[-2]

    resp.raise_for_status()

    pattern = price_search_pattern.format(big_product_id)
    search_result = re.search(pattern, resp.text)
    if search_result:
        small_id = search_result.group(1)
        logger.debug('find small id %s', small_id)
        price_url = price_url_template.format(small_id)
        price_resp = requests_session.get(price_url, headers=price_headers, proxies=proxy.get_proxy_dict())
        price_resp.raise_for_status()
        logger.debug('Price url %s', price_url)
        logger.debug('Getting price status code %s', price_resp.status_code)

    else:
        logger.debug('Does not find id, pattern %s', pattern)
        raise Exception("Can't find id to do query. (Reason may be changing site body)")

    return resp.text, price_resp.json()


def test():
    """Raise exception if something fail.
    With contained() func check
    if necessary values contained in load_digitkey_page() response"""

    def contained(obj, *patterns):
        return all(pattern in str(obj) for pattern in patterns)

    assert contained(
        load_digitkey_page('https://www.digikey.com/en/products/detail/avx-corporation/06032U3R9BAT2A/6796754'),
        '06032U3R9BAT2A', '$0.37000', '$89.17', 'Description', '53,351'
    )

    assert contained(
        load_digitkey_page('https://www.digikey.com/en/products/detail/avx-corporation/F380J226MMAAH3/5730797'),
        'F380J226MMAAH3', '$144.64', '20,433'
    )

    assert contained(
        load_digitkey_page('https://www.digikey.com/en/products/detail/knowles-voltronics/JR300/6021637'),
        'JR300', '20,601', '$854.12', 'Description', '17'
    )

    logger.info('All test passed')


if __name__ == '__main__':
    """RUN THIS FILE TO CHECK ALL WORKS
    pip install requests pysocks
    """
    test()
