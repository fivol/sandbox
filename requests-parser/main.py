import urllib
from sandbox_parser_utils import *
from config import *
from time import time
from http.cookies import SimpleCookie
import requests_cache

requests_cache.install_cache('.requests_cache')

# CURRENT TESTS AND EXPERIMENTS CONFIG
URL = 'http://quotes.toscrape.com/'
PROJECT_NAME = 'quotes'


def urljoin(relative_url):
    return urllib.parse.urljoin(URL, relative_url)


def save(dicts, new_file=True, ext='json'):
    """Saves data in format: List OF Dicts"""
    filename = f'{PROJECT_NAME}-{time()}' if new_file else PROJECT_NAME
    temp_string = '{data_folder}/{project_folder}/{filename}.{ext}'

    filepath = temp_string.format(data_folder=DATA_DIRECTORY,
                                  project_folder=PROJECT_NAME,
                                  filename=filename,
                                  ext=ext)
    save_dicts(dicts, filepath)


def get_cookie_dict(cookie_str: str) -> dict:
    cookie = SimpleCookie()
    cookie.load(cookie_str)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies


headers_str = """
Host: www.digikey.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: 
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache
TE: Trailers
"""
headers = headers_from_str(headers_str)
print(headers)

def main():
    url = 'https://www.digikey.com/en/products/detail/kemet/T520B337M2R5ATE045/1001041'
    requests.get(url, headers=headers).raise_for_status()


def test():
    price_headers = get_request_info('data/www.digikey.com.har')['headers']
    # print(price_headers)


if __name__ == '__main__':
    main()
    # test()
