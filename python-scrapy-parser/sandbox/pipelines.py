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


class CleanItemPipline:
    """This pipeline prepares every field in Item
        How to use it?
        ...
        name = scrapy.Field(strip=True, int=False, extract_number=True)
        ....
        Avaliable parameters:
        strip (default True) - remove space symbols from begin and end of string
    
    """

    @staticmethod
    def _handle_field(value, **kwargs):
        for func, arg in kwargs.items():
            if func == 'strip' and arg:
                value = value.strip()
            if func == 'extract':
                extract_schema = {
                    'int': r'\d+',
                    'float': r'\d+(\.|,)\d',
                }
                schema = extract_schema.get(arg)
                if schema:
                    value = re.search(schema, value).group(0)
            if func == 'cast':
                value = arg(value)

        return value

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field in adapter.field_names():
            meta = adapter.get_field_meta(field)
            value = adapter.get(field)
            try:
                adapter[field] = self._handle_field(value, **meta)
            except:
                logger.warn('Fail to prepare field: %s, value: %s', field, value)

        return adapter.item


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
        adapter = ItemAdapter(item)
        if not adapter.is_item(item) or not isinstance(item, scrapy.Item):
            logger.warn('NOT ITEM %s', item)
            return item

        item_cls = item.__class__
        exporter = self._get_exporter(item_cls)
        exporter.export_item(item)


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
