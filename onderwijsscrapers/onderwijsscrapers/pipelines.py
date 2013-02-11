import os
from datetime import datetime
import pytz

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

from onderwijsscrapers import exporters


class OnderwijsscrapersPipeline(object):
    def __init__(self):
        self.scrape_started = datetime.utcnow().replace(tzinfo=pytz.utc)\
            .strftime('%Y-%m-%dT%H:%M:%SZ')
        self.items = {}
        self.universal_items = {}

    def process_item(self, item, spider):
        # Check if this item should be included into all related items
        # of the same spider (e.g. ignore reference year)
        universal_item = False
        if 'ignore_id_fields' in item:
            for field in item['ignore_id_fields']:
                item[field] = None

            del item['ignore_id_fields']
            universal_item = True

        # Check if the fields that identify the item are present. If not,
        # log and drop the item.
        id_fields = settings['ELASTIC_SEARCH'][spider.name]['id_fields']
        if not all(field in item for field in id_fields):
            log.msg('Dropped item, not all required fields are present. %s'
                % item, evel=log.WARNING, spider=spider)
            raise DropItem
            return

        item_id = '-'.join([str(item[field]) for field in id_fields])
        if universal_item:
            item_stack = self.universal_items
        else:
            item_stack = self.items

        if item_id not in item_stack:
            item_stack[item_id] = dict(item)
        else:
            item_stack[item_id].update(dict(item))

        return item

    def close_spider(self, spider):
        # Setup the exporter
        if settings['EXPORT_METHOD'] == 'elasticsearch':
            exporter = exporters.ElasticSearchExporter(
                scrape_started_at=self.scrape_started,
                spider=spider.name,
                config=settings['ELASTIC_SEARCH'][spider.name],
                url=settings['ELASTIC_SEARCH'][spider.name]['url'],
                index=settings['ELASTIC_SEARCH'][spider.name]['index'],
                doctype=settings['ELASTIC_SEARCH'][spider.name]['doctype'],
            )

        elif settings['EXPORT_METHOD'] == 'file':
            exporter = exporters.FileExporter(
                scrape_started_at=self.scrape_started,
                spider=spider.name,
                config=settings['ELASTIC_SEARCH'][spider.name],
                url=settings['ELASTIC_SEARCH'][spider.name]['url'],
                index=settings['ELASTIC_SEARCH'][spider.name]['index'],
                doctype=settings['ELASTIC_SEARCH'][spider.name]['doctype'],
                path=os.path.join(settings['EXPORT_DIR'], spider.name),
            )

        id_fields = settings['ELASTIC_SEARCH'][spider.name]['id_fields']
        for item_id, item in self.items.iteritems():
            universal_item = 'None-%s' % '-'.join([str(item[field]) for field in \
                id_fields[1:]])
            if universal_item in self.universal_items:
                universal_item = self.universal_items[universal_item]
                if 'reference_year' in universal_item:
                    del universal_item['reference_year']
                item.update(universal_item)

            item['meta'] = {
                'scrape_started_at': self.scrape_started,
                'item_scraped_at': datetime.utcnow().replace(tzinfo=pytz.utc)\
                    .strftime('%Y-%m-%dT%H:%M:%SZ')
            }

            exporter.save(item_id, item)
