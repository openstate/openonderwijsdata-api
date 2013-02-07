import os

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

from onderwijsscrapers import exporters


class OnderwijsscrapersPipeline(object):
    def __init__(self):
        self.items = {}

    def process_item(self, item, spider):
        # Check if the fields that identify the item are present. If not,
        # log and drop the item.
        id_fields = settings['ELASTIC_SEARCH'][spider.name]['id_fields']
        if not all(field in item for field in id_fields):
            log.msg('Dropped item, not all required fields are present. %s' % item,
                level=log.WARNING, spider=spider)
            raise DropItem
            return

        item_id = '-'.join([str(item[field]) for field in id_fields])
        if item_id not in self.items:
            self.items[item_id] = dict(item)
        else:
            self.items[item_id].update(dict(item))

        return item

    def close_spider(self, spider):
        # Setup the exporter
        if settings['EXPORT_METHOD'] == 'elasticsearch':
            exporter = exporters.ElasticSearchExporter(
                url=settings['ELASTIC_SEARCH'][spider.name]['url'],
                index=settings['ELASTIC_SEARCH'][spider.name]['index'],
                doctype=settings['ELASTIC_SEARCH'][spider.name]['doctype']
            )

        elif settings['EXPORT_METHOD'] == 'file':
            exporter = exporters.FileExporter(os.path.join(
                settings['EXPORT_DIR'], spider.name))

        for item_id, item in self.items.iteritems():
            exporter.save(item_id, item)
