import requests
from joblib import Memory
import json
from scrapy import Selector
import os
from pathlib import Path
from config import *

memory = Memory(CACHE_LOCATION, verbose=0)


@memory.cache
def get_html(url, session=None, **kwargs):
    """Just make request on internet by url"""
    response = requests.get(url, **kwargs)
    return response.text


def save_response(text, filename):
    with open(filename, 'w') as f:
        f.write(text)


def get_request_info(filename):
    """Returns simple dict object that represents .har file requests
        Get only first entity (should be saved only one request)
        return  {
            headers: all headers without cookie and chrome staff
            cookie: cookie header
            method: request metthos
            _: all provided headers in file
        }
    """
    with open(filename, 'r') as f:
        har_json = json.load(f)
    har_headers = har_json['log']['entries'][0]['request']['headers']
    har_headers = {
            header['name']: header['value']
            for header
            in har_headers
        }
    headers = {name: value for (name, value) in har_headers.items() if not name.startswith(':')}
    headers.pop('cookie')
    return {
        'headers': headers,
        'method': har_headers[':method'],
        'cookie': har_headers['cookie'],
        '_': har_headers
    }


def headers_from_str(headers):
    return {
        item.split(': ')[0].strip(): item.split(': ')[1]
        for item in headers.strip().split('\n') if (':' in item)
    }


def get_page(url, **kwargs):
    """Returns scrapy selector object by url."""
    return Selector(text=get_html(url, **kwargs))


@memory.cache
def create_folders(dirspath):
    """Creates nested folders"""
    if not Path(dirspath).exists():
        os.makedirs(dirspath)


def save_dicts(dicts, filepath):
    """dicts is List of dicts variable"""
    create_folders(os.path.dirname(filepath))
    ext = filepath.split('.')[-1]
    with open(filepath, 'w') as f:
        if ext == 'jl':
            for item in dicts:
                json.dump(item, f)
                f.write('\n')
        elif ext == 'json':
            json.dump(dicts, f, indent=4)
