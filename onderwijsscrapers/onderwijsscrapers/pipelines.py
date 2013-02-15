import glob
import os
from datetime import datetime
import pytz
import shutil
import tarfile

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

# from onderwijsscrapers import exporters
from onderwijsscrapers.item_enrichment import bag42_geocode


class OnderwijsscrapersPipeline(object):
    def __init__(self):
        self.scrape_started = datetime.utcnow().replace(tzinfo=pytz.utc)\
            .strftime('%Y-%m-%dT%H:%M:%SZ')
        self.items = {}
        self.universal_items = {}

    def process_item(self, item, spider):
        # Check if the fields that identify the item are present. If not,
        # log and drop the item.
        id_fields = settings['EXPORT_SETTINGS'][spider.name]['id_fields']
        if not all(field in item for field in id_fields):
            log.msg('Dropped item, not all required fields are present. %s'
                % item, level=log.WARNING, spider=spider)
            raise DropItem
            return

        item_id = '-'.join([str(item[field]) for field in id_fields])

        if item_id not in self.items:
            self.items[item_id] = dict(item)
        else:
            self.items[item_id].update(dict(item))

        # Check if this item should be included into all related items
        # of the same spider (e.g. ignore reference year)
        universal_item = False
        if 'ignore_id_fields' in item:
            for field in item['ignore_id_fields']:
                item[field] = None

            del item['ignore_id_fields']
            universal_item = True

        item_id = '-'.join([str(item[field]) for field in id_fields])
        if universal_item:
            self.universal_items[item_id] = dict(item).copy()

        return item

    def close_spider(self, spider):
        # Setup the exporters
        for export_method, export in settings.get('EXPORT_METHODS').items():
            export_settings = {
                'scrape_started_at': self.scrape_started,
                'spider': spider.name,
                'config': settings['EXPORT_SETTINGS'][spider.name],
                'url': settings['EXPORT_SETTINGS'][spider.name]['url'],
                'index': settings['EXPORT_SETTINGS'][spider.name]['index'],
                'doctype': settings['EXPORT_SETTINGS'][spider.name]['doctype']
            }
            if export_method == 'file':
                export_settings['path'] = os.path.join(settings['EXPORT_DIR'],
                    spider.name)

            exporter = export['exporter'](**export_settings)

            id_fields = settings['EXPORT_SETTINGS'][spider.name]['id_fields']
            for item_id, item in self.items.iteritems():
                universal_item = 'None-%s' % '-'.join([str(item[field]) for field in \
                    id_fields[1:]])
                if universal_item in self.universal_items:
                    universal_item = self.universal_items[universal_item]
                    if 'reference_year' in universal_item:
                        del universal_item['reference_year']
                    item.update(universal_item)

                if 'ignore_id_fields' in item:
                    del item['ignore_id_fields']

                item['meta'] = {
                    'scrape_started_at': self.scrape_started,
                    'item_scraped_at': datetime.utcnow().replace(tzinfo=pytz.utc)\
                        .strftime('%Y-%m-%dT%H:%M:%SZ')
                }

                # Geocode if enabled for this index
                if settings['EXPORT_SETTINGS'][spider.name]['geocode']:
                    for address_field in settings['EXPORT_SETTINGS'][spider.name]['geocode_fields']:
                        if address_field in item:
                            geocoded = bag42_geocode(item[address_field])
                            if geocoded:
                                item[address_field].update(geocoded)

                exporter.save(item_id, item)

        # Tar files
        if export['options']['tar']:
            log.msg('Tarring JSON files', level=log.INFO, spider=spider)
            # Tar the JSON files
            scrape_started = datetime.strptime(self.scrape_started,
                '%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d%H%M%S')
            with tarfile.open('%s/%s-%s.tar.gz' % (settings['TAR_LOCATION'],\
                spider.name, scrape_started), 'w:gz') as tar:
                for f in glob.glob('%s/*.json' % (spider.name)):
                    tar.add(f)

        # Remove files
        if export['exporter']['options']['remove_json']:
            shutil.rmtree('%s/%s' % (settings['EXPORT_DIR'], spider.name))
