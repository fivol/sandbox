# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import scrapy
import sqlalchemy
from sandbox.models import Session, Author, Quote
import re
from itemadapter import ItemAdapter
from scrapy.crawler import Crawler
from scrapy.exporters import BaseItemExporter
import os
from pathlib import Path, PurePath
import logging
import inflection
from collections import defaultdict
from scrapy.exceptions import DropItem

logger = logging.getLogger('mycustomlogger')


def stripper(text: str, **kwargs) -> str:
    """Leaves only english characters and digits (russion too)"""
    text = re.sub(r'[^ a-zA-Z0-9а-яА-Я]*', '', text)
    text = re.sub(r' |\t', ' ', text)
    return text.strip()


def create_folders(dirspath):
    """Creates nested folders"""
    if not Path(dirspath).exists():
        os.makedirs(dirspath)


class SandboxPipeline:
    def process_item(self, item, spider):
        return item


class SqlitePipeline:
    """Does not work yet"""

    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        try:
            self.session.commit()
            self.session.close()
        except:
            self.session.rollback()
            raise

    def process_item(self, item, spider):
        self.session.add(Quote(**dict(item)))


class ClearItemPipline:
    """This pipeline deletes all not alphabetic chars in Items. 
    Leaves only [a-zA-Z0-9а-яА-Я \n]"""
    @classmethod
    def serialize_value(cls, value):
        """Prettify string values, lists and dicts. Use stripper to .strip str
        And remove non alphabetic symbols"""
        if isinstance(value, str):
            return stripper(value)
        if isinstance(value, list):
            return [cls.serialize_value(item) for item in value]
        if isinstance(value, dict):
            return {
                key: cls.serialize_value(item)
                for key, item in value.items()
            }
        return None

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        serialized_value = self.serialize_value(adapter.asdict())
        return item.__class__(serialized_value)


class SplitExportersPipline:
    """Saves each type of items with own exporter
    Working only with items (not dicts)
    Receives setting FEEDS_SPLITTER in such format: 

    from scrapy.exporters import JsonItemExporter 

    'FEEDS_SPLITTER': {
        'exporter': JsonItemExporter,
        'folder': 'data/quotes_parser',
        'extension': 'json',
        'settings': {
            'indent': 4,
            'overwrite': True
        }
    }

    and do not forget specify

    'ITEM_PIPELINES': {
        ...
        pipelines.SplitExportersPipline: 200
        ...
    },

    It can be in set in global project settings file or in custom_settins in 
    spyder etc
    """

    def __init__(self, exporter=None, settings: dict = None,
                 folder: str = '', extension: str = ''):
        self.exporter_cls = exporter
        self.settings = settings
        if not settings:
            self.settings = {}

        self.folder = folder
        self.extension = extension
        create_folders(folder)
        self.item_class_exporter = {}
        self.item_class_file = {}

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        print('crawler')
        return cls(**crawler.settings.get('FEEDS_SPLITTER'))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for cls in self.item_class_exporter:
            file = self.item_class_file[cls]
            exporter = self.item_class_exporter[cls]
            exporter.finish_exporting()
            file.close()

    def _export_item(self, item, exporter):
        exporter.export_item(item)

    def _get_file(self, item_cls):
        classname = item_cls.__name__
        camelcase_name = classname.lower().replace('item', '')
        filename = inflection.underscore(camelcase_name)
        filename = '{}.{}'.format(filename, self.extension)
        filepath = PurePath(self.folder, filename)
        return open(filepath, 'wb')

    def _get_exporter(self, item_cls):
        if item_cls not in self.item_class_exporter:
            file = self._get_file(item_cls)
            self.item_class_file[item_cls] = file
            exporter = self.exporter_cls(file, **self.settings)
            exporter.start_exporting()
            self.item_class_exporter[item_cls] = exporter

        return self.item_class_exporter[item_cls]

    def process_item(self, item, spider):
        if not isinstance(item, scrapy.Item):
            return item

        item_cls = item.__class__
        exporter = self._get_exporter(item_cls)
        self._export_item(item, exporter)


class UniqueItemsPipline:
    """Removes all not uniqu items from items stream
        Works only with Items (not dicts)
        You have to set setting like this
        'PRIMARY_KEYS': {
            QuoteAuthorItem: ['name', 'sername'],
            TagItem: 'name',
            QuoteItem: 'quote'
        },
        where 
        QuoteAuthorItem is Item object
    """

    def __init__(self, primary_keys: dict = None):
        self.primary_keys = self._normalize_primary_keys(primary_keys)
        self.keys_seen = defaultdict(set)
        logger.debug("PRIMARY KEYS %s", self.primary_keys)
        super().__init__()

    def _normalize_primary_keys(self, primary_keys):
        if not primary_keys:
            return {}

        return {
            item_cls: [key] if isinstance(key, str) else key
            for item_cls, key in (primary_keys.items() or [])
        }

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(primary_keys=settings.get('PRIMARY_KEYS'))

    def _item_hash(self, item):
        keys_names = self.primary_keys.get(item.__class__)
        keys_values = map(lambda key: str(item[key]), keys_names)
        return hash('.'.join(keys_values))

    def process_item(self, item, spider):
        if not isinstance(item, scrapy.Item):
            return item
        item_cls = item.__class__
        if item_cls not in self.primary_keys:
            return item

        item_hash = self._item_hash(item)
        if item_hash in self.keys_seen[item_cls]:
            logging.debug('Drop item %s', item)
            raise DropItem(f"Duplicate item found: {item!r}")
        
        self.keys_seen[item_cls].add(item_hash)
        return item
