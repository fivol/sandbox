# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from typing import Type
import scrapy
import sqlalchemy
from sandbox.models import Session, Author, Quote
import re
from itemadapter import ItemAdapter, adapter
from scrapy.crawler import Crawler
from scrapy.exporters import BaseItemExporter
import os
from pathlib import Path, PurePath
import logging
import inflection
from collections import defaultdict
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from sandbox.utils import *
from typing import List

logger = logging.getLogger('mycustomlogger')


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
        class QuoteItem(scrapy.Item):
            ...
            name = scrapy.Field(strip=True, int=False, extract_number=True)
            ....
        Avaliable parameters:

        strip (default True) - remove space symbols from begin and end of string
        extract (default None): 
            'int' - extract integer number from string
            'float' - extract float point number from string
            r'<regex>' - re.search(r'<regex>', value)
        cast (default None) - transform value to proper type. For example int(value)
    """

    default_args = {
        'strip': True,
        'extract': None,
        'cast': None
    }

    @staticmethod
    def _handle_field(value, **kwargs):
        for func, arg in kwargs.items():
            if not arg:
                continue

            if func == 'strip':
                if isinstance(value, str):
                    value = value.strip()
                if isinstance(value, List[str]):
                    value = map(lambda x: x.strip(), value)

            if func == 'extract':
                extract_schema = {
                    'int': r'\d+',
                    'float': r'\d+((\.|,)\d+)?',
                }
                schema = extract_schema.get(arg)
                if not schema:
                    schema = arg
                value = re.search(schema, value).group(0)

            if func == 'cast':
                value = arg(value)

        return value

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field in adapter.field_names():
            meta = adapter.get_field_meta(field) or self.default_args
            value = adapter.get(field)
            try:
                adapter[field] = self._handle_field(value, **meta)
            except:
                logger.warn('Fail to prepare field %s, value: %s', field, value)

        return adapter.item


class SplitExportersPipline:
    """Saves each type of items with own exporter
    Working only with items (not dicts)
    Receives setting FEEDS_SPLITTER in such format: 

    from scrapy.exporters import JsonItemExporter 

    'SPLIT_EXPORTERS_PIPELINE': {
        'exporter': JsonItemExporter,
        'folder': 'data/quotes_parser',
        'extension': 'json',
        'settings': {
            'indent': 4,
            'overwrite': True
        }
    }

    and do not forget to specify

    'ITEM_PIPELINES': {
        ...
        pipelines.SplitExportersPipline: 200
        ...
    },

    It can be in set in global project settings file or in custom_settins in 
    spyder etc
    """

    def __init__(self, exporter=None, settings: dict = None,
                 folder: str = '', extension: str = '', ignore_pipeline=True):
        self.ignore_pipeline = ignore_pipeline
        if ignore_pipeline:
            return
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
        pipeline_settings = crawler.settings.get('SPLIT_EXPORTERS_PIPELINE')
        if not pipeline_settings:
            return cls()
        return cls(**pipeline_settings, ignore_pipeline=False)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        if self.ignore_pipeline:
            return
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
        if self.ignore_pipeline:
            return item
        adapter = ItemAdapter(item)
        if not adapter.is_item(item) or not isinstance(item, scrapy.Item):
            logger.warn('NOT ITEM %s', item)
            return item

        item_cls = item.__class__
        exporter = self._get_exporter(item_cls)
        exporter.export_item(item)


class UniqueItemsPipline:
    """Removes all not unique items from items stream
        Works only with Items class (not dicts etc)
        You have to set Field metadate primary_key=True

        class TagItem(scrapy.Item):
            name = scrapy.Field(primary_key=True)
            description = scrapy.Field()

        Then this field will be unique in output.
        Duplicates will be removed.
        There may be several fields with primary_key option
    """

    def __init__(self, primary_keys: dict = None):
        self.keys_seen = defaultdict(set)
        super().__init__()

    def _item_hash(self, item, keys):
        key_values = map(lambda key: str(item[key]), keys)
        return hash('.'.join(key_values))

    @staticmethod
    def _get_primary_keys(adapter):
        return [
            key for key in adapter.keys()
            if adapter.get_field_meta(key).get('primary_key')
        ]

    def process_item(self, item, spider):
        if not isinstance(item, scrapy.Item):
            return item
        adapter = ItemAdapter(item)
        item_cls = item.__class__
        primary_keys = self._get_primary_keys(adapter)

        item_hash = self._item_hash(item, primary_keys)
        if item_hash in self.keys_seen[item_cls]:
            logging.debug('Drop item %s', item)
            raise DropItem(f"Duplicate item found: {item!r}")
        
        self.keys_seen[item_cls].add(item_hash)
        return item
