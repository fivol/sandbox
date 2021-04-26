from pathlib import Path
import os


def create_folders(dirspath):
    """Creates nested folders"""
    if dirspath and isinstance(dirspath, str) and not Path(dirspath).exists():
        os.makedirs(dirspath)

def merge_dicts(dict1, dict2):
    """Deep dicts merge"""
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        raise TypeError('Objects must be dict type: %s, %s' % (dict1, dict2))
    result = dict1
    for key, value in dict2.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_dicts(result[key], value)
        result[key] = value

def generate_settings(spider, **settings):
    return merge_dicts(spider.settings, settings)
